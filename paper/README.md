# Paper Mapping

This repository mirrors the paper's runtime-governance framing.

- Paper introduction and architecture framing -> [../docs/architecture.md](../docs/architecture.md)
- Epistemic Control Layer (ECL) -> [../kaira/runtime/ecl.py](../kaira/runtime/ecl.py)
- Internal Deliberation Loop (IDL) -> [../kaira/runtime/idl.py](../kaira/runtime/idl.py)
- Runtime controller and final trace object -> [../kaira/runtime/controller.py](../kaira/runtime/controller.py)
- Semantic validation and ontology checks -> [../kaira/ontology/validator.py](../kaira/ontology/validator.py)
- Tool routing and human handoff -> [../kaira/policies/router.py](../kaira/policies/router.py), [../kaira/policies/handoff.py](../kaira/policies/handoff.py)
- Meaning-gated memory -> [../kaira/memory/commit_policy.py](../kaira/memory/commit_policy.py)
- Evaluation harness and golden traces -> [../kaira/eval/benchmarks.py](../kaira/eval/benchmarks.py), [../kaira/eval/golden_traces.py](../kaira/eval/golden_traces.py)

The paper itself remains in this directory as `kaira_arxiv.tex`, `kaira_refs.bib`, and `kaira_arxiv.pdf`.

Canonical runtime configuration used by the repo lives in `data/default_policy.json` and `data/default_runtime.json`.
