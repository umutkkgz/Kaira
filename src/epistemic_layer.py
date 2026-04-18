from dataclasses import dataclass


@dataclass
class EpistemicAssessment:
    score: float
    decision: str
    rationale: str


class EpistemicControlLayer:
    """
    Toy implementation of the Epistemic Control Layer (ECL).
    The layer decides whether the system should proceed, ask for clarification,
    refuse, or escalate to a human operator.
    """

    def __init__(self, epistemic_threshold=0.75):
        self.eth = epistemic_threshold
        self.in_domain_terms = set()
        self.high_risk_terms = set()
        self.ambiguous_terms = set()

    def configure(self, ontology):
        control = ontology.get("epistemic_control", {})
        self.in_domain_terms = set(control.get("in_domain_terms", []))
        self.high_risk_terms = set(control.get("high_risk_terms", []))
        self.ambiguous_terms = set(control.get("ambiguous_terms", []))

    def assess(self, request_query, graph_retriever=None):
        query = request_query.lower()

        if any(term in query for term in self.high_risk_terms):
            return EpistemicAssessment(
                score=0.18,
                decision="escalate",
                rationale="Request is outside the bounded operational domain or requires human approval."
            )

        if any(term in query for term in self.ambiguous_terms) and not any(
            term in query for term in self.in_domain_terms
        ):
            return EpistemicAssessment(
                score=0.58,
                decision="clarify",
                rationale="Request may be in scope, but operational details are too ambiguous to answer safely."
            )

        if any(term in query for term in self.in_domain_terms):
            return EpistemicAssessment(
                score=0.93,
                decision="proceed",
                rationale="Query appears to be within the bounded service ontology."
            )

        return EpistemicAssessment(
            score=0.22,
            decision="refuse",
            rationale="Insufficient grounded support for a bounded-domain answer."
        )

    def should_refuse(self, assessment):
        return assessment.decision in {"refuse", "escalate"}
