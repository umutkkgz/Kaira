from __future__ import annotations

from kaira.core.types import MemoryRecord


class SemanticCoreMemory:
    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    def append(self, record: MemoryRecord) -> None:
        self._records.append(record)

    def list_records(self) -> list[MemoryRecord]:
        return list(self._records)

    def size(self) -> int:
        return len(self._records)

