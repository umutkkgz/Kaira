# CHANGELOG

## 0.3.0

- Refactored the repository into a typed `kaira/` package layout
- Added a runtime controller with explicit ECL, routing, IDL, validation, and memory stages
- Replaced ad hoc dictionaries with structured dataclasses for all runtime stages
- Added policy config, ontology graph utilities, validator rejection reasons, and meaning-gated memory records
- Added benchmark harness, golden scenarios, metrics export, and example artifacts
- Added FastAPI server and lightweight dashboard surface
- Added tests, docs, CI, Makefile, pyproject, and pre-commit configuration
- Rewrote the README to align with the runtime-governance framing of the paper
