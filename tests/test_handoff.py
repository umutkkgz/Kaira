from __future__ import annotations

import unittest

from kaira.core.types import RuntimeState, UserInput
from tests._helpers import make_controller


class TestHandoff(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = make_controller()

    def test_route_handoff_required(self) -> None:
        route = self.controller.router.route("I want to reserve a room for tonight.")
        handoff = self.controller.handoff.from_route(route)
        self.assertTrue(handoff.required)

    def test_epistemic_handoff_required(self) -> None:
        decision = self.controller.ecl.assess(
            UserInput(query="Can you diagnose my medical issue?"),
            RuntimeState(session_id="handoff"),
        )
        handoff = self.controller.handoff.from_epistemic(decision)
        self.assertTrue(handoff.required)


if __name__ == "__main__":
    unittest.main()
