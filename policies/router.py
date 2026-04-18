from __future__ import annotations

from kaira.core.types import RoutingDecision
from kaira.policies.permissions import PolicyConfig


class ToolRouter:
    def __init__(self, ontology: dict, policy: PolicyConfig):
        self.ontology = ontology
        self.policy = policy
        self.routes = ontology.get("tool_policy", {}).get("routes", {})
        self.default_route = ontology.get("tool_policy", {}).get("default_action", {})

    def route(self, query: str) -> RoutingDecision:
        lowered = query.lower()
        for action, config in self.routes.items():
            if any(keyword in lowered for keyword in config.get("keywords", [])):
                status = self.policy.status_for(action)
                return RoutingDecision(
                    action=action,
                    policy_permit=status not in {"forbidden", "out_of_domain", "unknown"},
                    human_approval_required=status == "approval_required" or config.get("human_approval_required", False),
                    reason=config.get("reason", "Matched policy route."),
                    route_status=status,
                )
        return RoutingDecision(
            action=self.default_route.get("action", "unknown"),
            policy_permit=False,
            human_approval_required=False,
            reason=self.default_route.get("reason", "No allowed workflow mapping for this request."),
            route_status="unknown",
        )

