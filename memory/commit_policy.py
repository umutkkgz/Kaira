from __future__ import annotations

from kaira.core.types import MemoryRecord
from kaira.runtime.decision import MemoryAction as MemoryActionEnum


class MeaningGatedCommitPolicy:
    def __init__(self, commit_threshold: float = 0.85, cache_threshold: float = 0.60):
        self.commit_threshold = commit_threshold
        self.cache_threshold = cache_threshold

    def decide(self, oms_score: float, record: MemoryRecord) -> tuple[str, MemoryRecord]:
        if oms_score >= self.commit_threshold:
            record.commit_rationale = "OMS exceeded persistent commit threshold."
            return MemoryActionEnum.COMMIT_PERSISTENT.value, record
        if oms_score >= self.cache_threshold:
            record.commit_rationale = "OMS below persistent commit threshold but sufficient for episodic cache."
            return MemoryActionEnum.CACHE_EPISODIC.value, record
        record.commit_rationale = "OMS insufficient for any memory write."
        return MemoryActionEnum.REJECT_WRITE.value, record
