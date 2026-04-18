from __future__ import annotations

import time
import uuid

from kaira.core.types import FinalResponse, MemoryRecord, RuntimeTrace, UserInput
from kaira.memory.commit_policy import MeaningGatedCommitPolicy
from kaira.memory.episodic import EpisodicMemory
from kaira.memory.semantic_core import SemanticCoreMemory
from kaira.ontology.loader import OntologyGraph
from kaira.ontology.validator import OntologyValidator
from kaira.policies.handoff import HandoffPolicy
from kaira.policies.permissions import PolicyConfig
from kaira.policies.router import ToolRouter
from kaira.runtime.decision import FinalStatus
from kaira.runtime.ecl import EpistemicControlLayer
from kaira.runtime.generator import DemoGenerator
from kaira.runtime.idl import InternalDeliberationLoop


class RuntimeController:
    def __init__(self, ontology: OntologyGraph, policy_config: dict, runtime_config: dict | None = None):
        self.ontology = ontology
        self.policy = PolicyConfig.from_dict(policy_config)
        runtime = (runtime_config or {}).get("runtime", {})
        epistemic_threshold = runtime.get("epistemic_threshold", 0.75)
        commit_threshold = runtime.get("commit_threshold", 0.85)
        cache_threshold = runtime.get("cache_threshold", 0.60)
        max_idl_iterations = runtime.get("max_idl_iterations", 3)
        self.episodic_memory = EpisodicMemory()
        self.semantic_core = SemanticCoreMemory()
        self.commit_policy = MeaningGatedCommitPolicy(
            commit_threshold=commit_threshold,
            cache_threshold=cache_threshold,
        )
        self.ecl = EpistemicControlLayer(ontology.data, threshold=epistemic_threshold)
        self.router = ToolRouter(ontology.data, self.policy)
        self.handoff = HandoffPolicy()
        self.validator = OntologyValidator(ontology.data)
        self.idl = InternalDeliberationLoop(
            self.validator,
            max_iterations=max_idl_iterations,
            commit_threshold=commit_threshold,
        )
        self.generator = DemoGenerator()

    def process(self, user_input: UserInput) -> FinalResponse:
        trace_id = str(uuid.uuid4())
        start = time.perf_counter()
        latency: dict[str, float] = {}

        state_start = time.perf_counter()
        state = self.episodic_memory.get_state(user_input.session_id)
        state.semantic_memory_size = self.semantic_core.size()
        latency["state_lookup"] = (time.perf_counter() - state_start) * 1000

        ecl_start = time.perf_counter()
        ecl_decision = self.ecl.assess(user_input, state)
        latency["ecl"] = (time.perf_counter() - ecl_start) * 1000

        if ecl_decision.decision in {"clarify", "refuse", "escalate"}:
            final_status = {
                "clarify": FinalStatus.CLARIFICATION_REQUIRED.value,
                "refuse": FinalStatus.REFUSED.value,
                "escalate": FinalStatus.ESCALATED.value,
            }[ecl_decision.decision]
            text = {
                "clarify": "Before I answer, could you clarify which service or policy you mean?",
                "refuse": "I do not have enough grounded support to answer that within my bounded domain.",
                "escalate": "This request falls outside my bounded operational scope and should be handled by a human operator.",
            }[ecl_decision.decision]
            handoff = self.handoff.from_epistemic(ecl_decision)
            trace = RuntimeTrace(
                trace_id=trace_id,
                query=user_input.query,
                ecl_score=ecl_decision.score,
                ecl_reason=ecl_decision.reason,
                ecl_decision=ecl_decision.decision,
                idl_iterations=0,
                validator_status="not_run",
                ontology_hits=[],
                route_decision="not_run",
                handoff_decision="required" if handoff.required else "not_required",
                final_status=final_status,
                memory_action="reject_write",
                latency_breakdown_ms={**latency, "total": (time.perf_counter() - start) * 1000},
                rejection_reason=ecl_decision.reason,
                output_text=text,
            )
            return FinalResponse(text=text, final_status=final_status, trace=trace, handoff_required=handoff.required, route_action="none", memory_action="reject_write")

        route_start = time.perf_counter()
        route = self.router.route(user_input.query)
        latency["routing"] = (time.perf_counter() - route_start) * 1000

        if not route.policy_permit:
            trace = RuntimeTrace(
                trace_id=trace_id,
                query=user_input.query,
                ecl_score=ecl_decision.score,
                ecl_reason=ecl_decision.reason,
                ecl_decision=ecl_decision.decision,
                idl_iterations=0,
                validator_status="blocked",
                ontology_hits=[],
                route_decision=route.action,
                handoff_decision="not_required",
                final_status=FinalStatus.REJECTED.value,
                memory_action="reject_write",
                latency_breakdown_ms={**latency, "total": (time.perf_counter() - start) * 1000},
                rejection_reason=route.reason,
                output_text="I cannot map this request to an allowed workflow within my bounded deployment policy.",
            )
            return FinalResponse(text=trace.output_text, final_status=trace.final_status, trace=trace, handoff_required=False, route_action=route.action, memory_action="reject_write")

        route_handoff = self.handoff.from_route(route)
        if route_handoff.required:
            trace = RuntimeTrace(
                trace_id=trace_id,
                query=user_input.query,
                ecl_score=ecl_decision.score,
                ecl_reason=ecl_decision.reason,
                ecl_decision=ecl_decision.decision,
                idl_iterations=0,
                validator_status="not_run",
                ontology_hits=[],
                route_decision=route.action,
                handoff_decision="required",
                final_status=FinalStatus.APPROVAL_REQUIRED.value,
                memory_action="reject_write",
                latency_breakdown_ms={**latency, "total": (time.perf_counter() - start) * 1000},
                rejection_reason=route.reason,
                output_text="This request requires human approval before I can proceed.",
            )
            return FinalResponse(text=trace.output_text, final_status=trace.final_status, trace=trace, handoff_required=True, route_action=route.action, memory_action="reject_write")

        draft, validation, oms_score, iterations, idl_latency = self.idl.run(user_input, state, route, self.generator)
        latency.update({f"idl_{k}": v for k, v in idl_latency.items()})

        if draft is None or not validation.passed:
            text = "I am unable to provide a verified response to that query within my operational bounds."
            trace = RuntimeTrace(
                trace_id=trace_id,
                query=user_input.query,
                ecl_score=ecl_decision.score,
                ecl_reason=ecl_decision.reason,
                ecl_decision=ecl_decision.decision,
                idl_iterations=iterations,
                validator_status="rejected",
                ontology_hits=validation.ontology_hits,
                route_decision=route.action,
                handoff_decision="not_required",
                final_status=FinalStatus.REJECTED.value,
                memory_action="reject_write",
                latency_breakdown_ms={**latency, "total": (time.perf_counter() - start) * 1000},
                oms_score=oms_score,
                rejection_reason=validation.rejection_reason,
                output_text=text,
            )
            return FinalResponse(text=text, final_status=trace.final_status, trace=trace, handoff_required=False, route_action=route.action, memory_action="reject_write")

        record = MemoryRecord(
            content=draft.text,
            session_id=user_input.session_id,
            source_type="runtime_output",
            provenance=trace_id,
            trust_score=oms_score,
        )
        memory_action, record = self.commit_policy.decide(oms_score, record)
        if memory_action == "commit_persistent":
            self.semantic_core.append(record)
        elif memory_action == "cache_episodic":
            self.episodic_memory.append(record)

        text = draft.text
        trace = RuntimeTrace(
            trace_id=trace_id,
            query=user_input.query,
            ecl_score=ecl_decision.score,
            ecl_reason=ecl_decision.reason,
            ecl_decision=ecl_decision.decision,
            idl_iterations=iterations,
            validator_status="passed",
            ontology_hits=validation.ontology_hits,
            route_decision=route.action,
            handoff_decision="not_required",
            final_status=FinalStatus.ANSWERED.value,
            memory_action=memory_action,
            latency_breakdown_ms={**latency, "total": (time.perf_counter() - start) * 1000},
            oms_score=oms_score,
            output_text=text,
        )
        return FinalResponse(text=text, final_status=trace.final_status, trace=trace, handoff_required=False, route_action=route.action, memory_action=memory_action)
