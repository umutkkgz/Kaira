# Legacy Compatibility Layer

The `src/` directory is retained only as a backward-compatible shim for earlier demos and notebooks.

Canonical implementation now lives under:

- `kaira/runtime/`
- `kaira/ontology/`
- `kaira/policies/`
- `kaira/memory/`
- `kaira/eval/`

New code should import from `kaira/`, not from `src/`.
