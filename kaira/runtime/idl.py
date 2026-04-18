from __future__ import annotations

import time

from kaira.core.interfaces import Generator
from kaira.core.types import DraftResponse, RoutingDecision, RuntimeState, UserInput, ValidationResult
from kaira.ontology.validator import OntologyValidator


class InternalDeliberationLoop:
    def __init__(self, validator: OntologyValidator, max_iterations: int = 3, commit_threshold: float = 0.85):
        self.validator = validator
        self.max_iterations = max_iterations
        self.commit_threshold = commit_threshold

    def score_operational_meaning(self, validation: ValidationResult) -> float:
        if not validation.passed:
            return max(0.0, 0.35 * validation.coverage)
        weighted = (0.2 * validation.coverage) + (0.3 * validation.node_hit_ratio) + (0.5 * validation.relation_validity_ratio)
        return min(1.0, weighted)

    def run(
        self,
        user_input: UserInput,
        state: RuntimeState,
        route: RoutingDecision,
        generator: Generator,
    ) -> tuple[DraftResponse | None, ValidationResult, float, int, dict[str, float]]:
        last_validation = ValidationResult(
            passed=False,
            lexical_only=True,
            coverage=0.0,
            extracted_concepts=[],
            ontology_hits=[],
            node_hit_ratio=0.0,
            relation_validity_ratio=0.0,
            rejection_reason="no_attempt",
            explanation="No draft was evaluated.",
        )
        latency_ms = {"generation": 0.0, "validation": 0.0}
        for iteration in range(1, self.max_iterations + 1):
            generation_start = time.perf_counter()
            draft = generator.generate(user_input, state, iteration)
            latency_ms["generation"] += (time.perf_counter() - generation_start) * 1000

            validation_start = time.perf_counter()
            validation = self.validator.validate(user_input.query, draft.text, route)
            latency_ms["validation"] += (time.perf_counter() - validation_start) * 1000
            oms_score = self.score_operational_meaning(validation)
            last_validation = validation
            if validation.passed and oms_score >= self.commit_threshold:
                return draft, validation, oms_score, iteration, latency_ms
        return None, last_validation, self.score_operational_meaning(last_validation), self.max_iterations, latency_ms
