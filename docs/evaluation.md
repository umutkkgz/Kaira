# Evaluation

The current evaluation harness is deliberately small but reproducible.

Scenario categories:

- in-domain factual QA
- ontology boundary tests
- adversarial semantic traps
- clarification-needed cases
- mandatory escalation cases
- approval-required tool cases

Metrics exported in JSON and CSV:

- `hallucination_rate_in_domain`
- `refusal_rate_out_of_domain`
- `clarification_accuracy`
- `escalation_accuracy`
- `boundary_violation_count`
- `policy_violation_count`
- `ontology_rejection_precision`
- `route_accuracy`
- `mean_oms`
- `mean_ecl`
- `mean_idl_iterations`
- `p50_latency`
- `p95_latency`

Artifacts are written to [eval/results](../eval/results).
