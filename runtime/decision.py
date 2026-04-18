from __future__ import annotations

from enum import StrEnum


class ECLAction(StrEnum):
    PROCEED = "proceed"
    CLARIFY = "clarify"
    REFUSE = "refuse"
    ESCALATE = "escalate"


class FinalStatus(StrEnum):
    ANSWERED = "answered"
    CLARIFICATION_REQUIRED = "clarification_required"
    REFUSED = "refused"
    ESCALATED = "escalated"
    APPROVAL_REQUIRED = "approval_required"
    REJECTED = "rejected"


class MemoryAction(StrEnum):
    COMMIT_PERSISTENT = "commit_persistent"
    CACHE_EPISODIC = "cache_episodic"
    REJECT_WRITE = "reject_write"

