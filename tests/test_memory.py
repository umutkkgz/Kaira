from __future__ import annotations

import unittest

from kaira.core.types import MemoryRecord
from kaira.memory.commit_policy import MeaningGatedCommitPolicy


class TestMemoryCommitPolicy(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = MeaningGatedCommitPolicy()

    def test_commit_persistent(self) -> None:
        action, record = self.policy.decide(
            0.9,
            MemoryRecord(
                content="The fitness center is open 24/7.",
                session_id="memory",
                source_type="runtime_output",
                provenance="trace-1",
                trust_score=0.9,
            ),
        )
        self.assertEqual(action, "commit_persistent")
        self.assertIn("persistent", record.commit_rationale)

    def test_reject_low_trust_write(self) -> None:
        action, _record = self.policy.decide(
            0.2,
            MemoryRecord(
                content="Unverified response",
                session_id="memory",
                source_type="runtime_output",
                provenance="trace-2",
                trust_score=0.2,
            ),
        )
        self.assertEqual(action, "reject_write")


if __name__ == "__main__":
    unittest.main()
