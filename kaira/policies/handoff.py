from __future__ import annotations

from kaira.core.types import EpistemicDecision, HandoffDecision, RoutingDecision


class HandoffPolicy:
    def from_epistemic(self, decision: EpistemicDecision) -> HandoffDecision:
        if decision.decision == "escalate":
            return HandoffDecision(required=True, reason=decision.reason)
        return HandoffDecision(required=False, reason="No human handoff required.")

    def from_route(self, route: RoutingDecision) -> HandoffDecision:
        if route.human_approval_required:
            return HandoffDecision(required=True, reason=route.reason, queue="approval-queue")
        return HandoffDecision(required=False, reason="Route can proceed without human approval.")

