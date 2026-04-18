# Memory

KAIRA implements meaning-gated memory behavior:

- Persistent commit when the Operational Meaning Score exceeds the commit threshold
- Episodic cache when a response is usable but not strong enough for persistent storage
- No write when the response is unsupported

Relevant files:

- [kaira/memory/episodic.py](../kaira/memory/episodic.py)
- [kaira/memory/semantic_core.py](../kaira/memory/semantic_core.py)
- [kaira/memory/commit_policy.py](../kaira/memory/commit_policy.py)

Each memory record carries:

- session id
- provenance
- trust score
- source type
- timestamp
- commit rationale
