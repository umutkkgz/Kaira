from __future__ import annotations

from dataclasses import dataclass

from kaira.core.types import RoutingDecision, ValidationResult
from kaira.ontology.graph_ops import extract_concepts, relation_validity_ratio


@dataclass(slots=True)
class OntologyStats:
    coverage: float
    node_hit_ratio: float
    relation_validity_ratio: float


class OntologyValidator:
    def __init__(self, ontology: dict, lexical_threshold: float = 0.25, relational_threshold: float = 0.5):
        self.ontology = ontology
        self.lexical_threshold = lexical_threshold
        self.relational_threshold = relational_threshold

    def validate(self, query: str, candidate: str, route: RoutingDecision) -> ValidationResult:
        query_concepts = extract_concepts(query, self.ontology)
        candidate_concepts = extract_concepts(candidate, self.ontology)
        ontology_hits = sorted(set(query_concepts + candidate_concepts))
        blocked = [pattern for pattern in self.ontology.get("adversarial_blocks", []) if pattern in candidate.lower()]

        if blocked:
            return ValidationResult(
                passed=False,
                lexical_only=False,
                coverage=0.0,
                extracted_concepts=candidate_concepts,
                ontology_hits=ontology_hits,
                node_hit_ratio=0.0,
                relation_validity_ratio=0.0,
                rejection_reason="unsafe_action_request",
                explanation=f"Blocked pattern detected: {blocked[0]}",
            )

        if not candidate_concepts:
            return ValidationResult(
                passed=False,
                lexical_only=True,
                coverage=0.0,
                extracted_concepts=[],
                ontology_hits=ontology_hits,
                node_hit_ratio=0.0,
                relation_validity_ratio=0.0,
                rejection_reason="no_concept_match",
                explanation="Candidate response does not ground to ontology concepts.",
            )

        node_hit_ratio = min(1.0, len(candidate_concepts) / max(len(query_concepts), 1))
        relational_ratio = relation_validity_ratio(candidate_concepts, self.ontology)
        coverage = len(ontology_hits) / max(len(set(query_concepts + candidate_concepts)), 1)

        if coverage < self.lexical_threshold:
            return ValidationResult(
                passed=False,
                lexical_only=True,
                coverage=coverage,
                extracted_concepts=candidate_concepts,
                ontology_hits=ontology_hits,
                node_hit_ratio=node_hit_ratio,
                relation_validity_ratio=relational_ratio,
                rejection_reason="weak_concept_support",
                explanation="Lexical support is too weak for bounded release.",
            )

        if relational_ratio < self.relational_threshold:
            return ValidationResult(
                passed=False,
                lexical_only=False,
                coverage=coverage,
                extracted_concepts=candidate_concepts,
                ontology_hits=ontology_hits,
                node_hit_ratio=node_hit_ratio,
                relation_validity_ratio=relational_ratio,
                rejection_reason="invalid_relation_path",
                explanation="Concepts do not form a valid relation path inside the ontology.",
            )

        if route.route_status == "forbidden":
            return ValidationResult(
                passed=False,
                lexical_only=False,
                coverage=coverage,
                extracted_concepts=candidate_concepts,
                ontology_hits=ontology_hits,
                node_hit_ratio=node_hit_ratio,
                relation_validity_ratio=relational_ratio,
                rejection_reason="policy_misalignment",
                explanation="Candidate route conflicts with policy configuration.",
            )

        return ValidationResult(
            passed=True,
            lexical_only=False,
            coverage=coverage,
            extracted_concepts=candidate_concepts,
            ontology_hits=ontology_hits,
            node_hit_ratio=node_hit_ratio,
            relation_validity_ratio=relational_ratio,
            explanation="Candidate is admissible under lexical and relational validation.",
        )
