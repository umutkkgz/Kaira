from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class UserInput:
    query: str
    session_id: str = "demo-session"
    user_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now_iso)


@dataclass(slots=True)
class RuntimeState:
    session_id: str
    turn_index: int = 0
    history: list[str] = field(default_factory=list)
    semantic_memory_size: int = 0
    episodic_memory_size: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DraftResponse:
    text: str
    generator_name: str
    iteration: int
    latency_ms: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EpistemicDecision:
    score: float
    decision: str
    reason: str
    signals: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class ValidationResult:
    passed: bool
    lexical_only: bool
    coverage: float
    extracted_concepts: list[str]
    ontology_hits: list[str]
    node_hit_ratio: float
    relation_validity_ratio: float
    rejection_reason: str | None = None
    explanation: str | None = None


@dataclass(slots=True)
class RoutingDecision:
    action: str
    policy_permit: bool
    human_approval_required: bool
    reason: str
    route_status: str


@dataclass(slots=True)
class HandoffDecision:
    required: bool
    reason: str
    queue: str = "human-operations"


@dataclass(slots=True)
class MemoryRecord:
    content: str
    session_id: str
    source_type: str
    provenance: str
    trust_score: float
    timestamp: str = field(default_factory=utc_now_iso)
    commit_rationale: str = ""


@dataclass(slots=True)
class RuntimeTrace:
    trace_id: str
    query: str
    ecl_score: float
    ecl_reason: str
    ecl_decision: str
    idl_iterations: int
    validator_status: str
    ontology_hits: list[str]
    route_decision: str
    handoff_decision: str
    final_status: str
    memory_action: str
    latency_breakdown_ms: dict[str, float]
    oms_score: float = 0.0
    rejection_reason: str | None = None
    output_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class FinalResponse:
    text: str
    final_status: str
    trace: RuntimeTrace
    handoff_required: bool
    route_action: str
    memory_action: str


@dataclass(slots=True)
class EvalScenarioResult:
    scenario_id: str
    category: str
    query: str
    expected_status: str
    observed_status: str
    expected_route: str | None
    observed_route: str
    passed: bool
    oms_score: float
    ecl_score: float
    latency_ms: float


@dataclass(slots=True)
class EvalResult:
    run_id: str
    scenario_count: int
    metrics: dict[str, float]
    scenarios: list[EvalScenarioResult]

