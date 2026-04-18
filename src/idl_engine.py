import time
from meaning_function import OperationalMeaningScorer
from epistemic_layer import EpistemicControlLayer

class BaseGenerator:
    """Toy stochastic generator used only for architectural demonstration."""
    def __init__(self, fallback_mode=False):
         self.attempt_count = 0
         self.fallback = fallback_mode
         
    def generate(self, query):
         self.attempt_count += 1
         query_lower = query.lower()

         if "15th-floor" in query.lower():
             if self.attempt_count == 1:
                 return "Certainly! The 15th-floor nuclear reactor pool is open for VIP guests."
             elif self.attempt_count == 2:
                 return "Yes, we have a wonderful 15th-floor pool available."
             return "I cannot verify a 15th-floor pool within the available hotel information."

         if "gym" in query_lower:
             return "The fitness center is located on the 2nd floor and is open 24/7."

         if "check-in" in query_lower or "check in" in query_lower:
             return "Check-in time is 3:00 PM."

         if "smoking" in query_lower:
             return "Smoking is prohibited inside the building."

         return "I need a little more detail before I can answer that safely."

class OntologyGraph:
    """
    Interface to the parsed JSON mini-ontology.
    """
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def summary(self):
        hotel = self.data_dict.get("hotel", {})
        service_catalog = hotel.get("service_catalog", {})
        policies = hotel.get("policies", {})
        routes = self.data_dict.get("tool_policy", {}).get("routes", {})
        return {
            "domain": self.data_dict.get("metadata", {}).get("domain", "unknown"),
            "services": len(service_catalog),
            "policies": len(policies),
            "routes": len(routes),
            "blocks": len(self.data_dict.get("adversarial_blocks", []))
        }


class ToolRouter:
    """
    Toy policy-constrained router.

    T_allowed(s) = {u in U | P(u, s)=1 and H(u, s)=0}
    where P is the policy permit flag and H indicates that human approval is required.
    """

    def __init__(self, ontology):
        tool_policy = ontology.get("tool_policy", {})
        self.routes = tool_policy.get("routes", {})
        self.default_action = tool_policy.get("default_action", {
            "action": "unknown",
            "policy_permit": False,
            "human_approval_required": False,
            "reason": "No allowed workflow mapping for this request."
        })

    def route(self, query):
        query_lower = query.lower()

        for action, config in self.routes.items():
            if any(keyword in query_lower for keyword in config.get("keywords", [])):
                return {
                    "action": action,
                    "policy_permit": config.get("policy_permit", False),
                    "human_approval_required": config.get("human_approval_required", False),
                    "reason": config.get("reason", "Matched ontology route.")
                }

        return self.default_action


class InternalDeliberationLoop:
    """
    Generate-criticize-validate loop for bounded deployment demonstration.
    """
    def __init__(self, meaning_fn: OperationalMeaningScorer, ontology: OntologyGraph, tau_commit=0.85, max_iter=3):
        self.scorer = meaning_fn
        self.graph = ontology.data_dict
        self.ontology = ontology
        self.tau = tau_commit
        self.max_iter = max_iter
        self.epistemic = EpistemicControlLayer()
        self.epistemic.configure(self.graph)
        self.router = ToolRouter(self.graph)
        
    def invoke(self, query, generator_model):

        # 1. Epistemic verification first.
        print("\033[35m\n>> [ROUTING TO EPISTEMIC CONTROL LAYER...]\033[0m")
        time.sleep(0.5)
        assessment = self.epistemic.assess(query, None)
        print(f"    \u21b3 Epistemic Competence Score \u2130(s,a)    : {assessment.score:.2f}")
        print(f"    \u21b3 Decision                              : {assessment.decision}")
        print(f"    \u21b3 Rationale                             : {assessment.rationale}")

        if assessment.decision == "clarify":
            return "Before I answer, could you clarify which service or policy you mean?"

        if assessment.decision == "refuse":
            print("\033[32m    \u21b3 EVENT:           Refusal triggered. Unsupported boundary state.\033[0m")
            return "I apologize, but I do not have sufficient operational knowledge to safely answer that."

        if assessment.decision == "escalate":
            print("\033[32m    \u21b3 EVENT:           Human handoff triggered.\033[0m")
            return "This request falls outside my bounded operational scope and should be handled by a human operator."

        # 2. Tool routing before free-form response release.
        print("\033[35m\n>> [ROUTING TO POLICY-CONSTRAINED TOOL LAYER...]\033[0m")
        route = self.router.route(query)
        print(f"    \u21b3 Routed Action                         : {route['action']}")
        print(f"    \u21b3 Policy Permit                         : {route['policy_permit']}")
        print(f"    \u21b3 Human Approval Required               : {route['human_approval_required']}")
        print(f"    \u21b3 Routing Rationale                     : {route['reason']}")

        if not route["policy_permit"]:
            return "I cannot map this request to an allowed workflow within my bounded deployment policy."

        if route["human_approval_required"]:
            return "This request requires human approval before I can proceed."

        # 3. Iterative generation constraint loop.
        for iteration in range(1, self.max_iter + 1):
            print(f"\n\033[34m=== IDL ITERATION {iteration} / {self.max_iter} ===\033[0m")

            action = generator_model.generate(query)
            print(f"    [Candidate Draft]: {action}")
            time.sleep(0.5)

            energy = self.scorer.score(query, action, self.graph)

            print(f"\n[OPERATIONAL MEANING SCORE]: OMS(s,a) = {energy:.2f} | Constraint Threshold (\u03C4) = {self.tau:.2f}")

            if energy >= self.tau:
                 print("\033[32m    \u21b3 EVENT:           Candidate committed. Constraint passed.\033[0m")
                 return action

            print("\033[31m    \u21b3 EVENT:           Candidate rejected. Validation boundary enforced.\033[0m")
            time.sleep(0.5)

        return "I am unable to provide a verified response to that query within my operational bounds."
