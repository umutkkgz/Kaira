# Architecture

KAIRA is a bounded deployment stack built around a small number of explicit control surfaces:

1. **Epistemic Control Layer (ECL)** decides whether the system should proceed, clarify, refuse, or escalate.
2. **Policy Router** maps admissible requests into allowed, approval-required, forbidden, or unknown actions.
3. **Internal Deliberation Loop (IDL)** iteratively validates drafts against ontology and policy constraints.
4. **Ontology Validator** checks lexical grounding and relational consistency.
5. **Meaning-Gated Memory** governs whether accepted outputs are committed to persistent memory, cached episodically, or dropped.

The central implementation path is:

- [kaira/runtime/controller.py](../kaira/runtime/controller.py)
- [kaira/runtime/ecl.py](../kaira/runtime/ecl.py)
- [kaira/runtime/idl.py](../kaira/runtime/idl.py)
- [kaira/ontology/validator.py](../kaira/ontology/validator.py)

This repository intentionally keeps the architecture explicit rather than heavily abstracted. The goal is auditability.
