from __future__ import annotations

from kaira.core.types import EpistemicDecision, RuntimeState, UserInput
from kaira.runtime.decision import ECLAction


class EpistemicControlLayer:
    def __init__(self, ontology: dict, threshold: float = 0.75):
        control = ontology.get("epistemic_control", {})
        self.threshold = threshold
        self.in_domain_terms = set(control.get("in_domain_terms", []))
        self.high_risk_terms = set(control.get("high_risk_terms", []))
        self.ambiguous_terms = set(control.get("ambiguous_terms", []))
        self.refusal_terms = set(control.get("refusal_terms", []))

    def assess(self, user_input: UserInput, state: RuntimeState) -> EpistemicDecision:
        query = user_input.query.lower()
        in_domain_hits = sum(term in query for term in self.in_domain_terms)
        high_risk_hits = sum(term in query for term in self.high_risk_terms)
        ambiguous_hits = sum(term in query for term in self.ambiguous_terms)
        continuity_signal = 1.0 if state.history else 0.5

        semantic_support = min(1.0, 0.3 + 0.2 * in_domain_hits)
        risk_penalty = min(1.0, 0.35 * high_risk_hits)
        ambiguity_penalty = min(1.0, 0.25 * ambiguous_hits)
        score = max(0.0, min(1.0, semantic_support + 0.15 * continuity_signal - risk_penalty - 0.5 * ambiguity_penalty))

        signals = {
            "semantic_support": semantic_support,
            "risk_penalty": risk_penalty,
            "ambiguity_penalty": ambiguity_penalty,
            "continuity_signal": continuity_signal,
        }

        if high_risk_hits:
            return EpistemicDecision(score=score, decision=ECLAction.ESCALATE.value, reason="Request falls outside bounded operational policy or requires human review.", signals=signals)
        if any(term in query for term in self.refusal_terms):
            return EpistemicDecision(score=score, decision=ECLAction.REFUSE.value, reason="Request attempts to push the system outside its bounded role or ontology.", signals=signals)
        if ambiguous_hits and not in_domain_hits:
            return EpistemicDecision(score=score, decision=ECLAction.CLARIFY.value, reason="Request may be in scope but lacks enough detail for safe execution.", signals=signals)
        if in_domain_hits:
            return EpistemicDecision(score=max(score, self.threshold + 0.1), decision=ECLAction.PROCEED.value, reason="Query appears to be supported by the bounded ontology.", signals=signals)
        return EpistemicDecision(score=score, decision=ECLAction.REFUSE.value, reason="Insufficient grounded support for a bounded-domain answer.", signals=signals)
