from __future__ import annotations

from collections import defaultdict

from kaira.core.types import MemoryRecord, RuntimeState


class EpisodicMemory:
    def __init__(self) -> None:
        self._records: dict[str, list[MemoryRecord]] = defaultdict(list)

    def get_state(self, session_id: str) -> RuntimeState:
        records = self._records.get(session_id, [])
        return RuntimeState(
            session_id=session_id,
            turn_index=len(records),
            history=[record.content for record in records[-5:]],
            episodic_memory_size=len(records),
        )

    def append(self, record: MemoryRecord) -> None:
        self._records[record.session_id].append(record)

    def list_records(self, session_id: str) -> list[MemoryRecord]:
        return list(self._records.get(session_id, []))

