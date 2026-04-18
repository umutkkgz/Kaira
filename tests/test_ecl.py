from __future__ import annotations

import unittest

from kaira.core.types import RuntimeState, UserInput
from tests._helpers import make_controller


class TestECL(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = make_controller()
        self.state = RuntimeState(session_id="test")

    def test_in_domain_proceeds(self) -> None:
        decision = self.controller.ecl.assess(UserInput(query="What time does the gym open?"), self.state)
        self.assertEqual(decision.decision, "proceed")

    def test_ambiguous_clarifies(self) -> None:
        decision = self.controller.ecl.assess(UserInput(query="Can you book something for me?"), self.state)
        self.assertEqual(decision.decision, "clarify")

    def test_high_risk_escalates(self) -> None:
        decision = self.controller.ecl.assess(UserInput(query="Can you diagnose my medical issue?"), self.state)
        self.assertEqual(decision.decision, "escalate")


if __name__ == "__main__":
    unittest.main()
