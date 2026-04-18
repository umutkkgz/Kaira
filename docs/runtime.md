# Runtime

`RuntimeController.process()` orchestrates the full bounded deployment loop:

1. Load runtime state from episodic memory
2. Compute epistemic decision
3. Return clarification, refusal, or escalation if support is insufficient
4. Route the request through the bounded policy layer
5. Trigger approval-required handoff when needed
6. Generate candidate drafts through the demo generator
7. Validate drafts through the ontology validator
8. Score admissibility through the Operational Meaning Score
9. Commit or cache accepted output using the memory commit policy
10. Return a structured final response and trace

Returned traces include:

- ECL score and reason
- route action and route status
- validator status and ontology hits
- IDL iteration count
- memory action
- final status
- latency breakdown
