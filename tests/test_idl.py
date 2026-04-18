from __future__ import annotations

import unittest

from kaira.core.types import RuntimeState, UserInput
from kaira.runtime.generator import DemoGenerator
from tests._helpers import make_controller


class TestIDL(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = make_controller()

    def test_idl_accepts_in_domain_answer(self) -> None:
        route = self.controller.router.route("What time does the gym open?")
        draft, validation, oms, iterations, _latency = self.controller.idl.run(
            UserInput(query="What time does the gym open?"),
            RuntimeState(session_id="idl"),
            route,
            DemoGenerator(),
        )
        self.assertIsNotNone(draft)
        self.assertTrue(validation.passed)
        self.assertGreaterEqual(oms, 0.85)
        self.assertEqual(iterations, 1)


if __name__ == "__main__":
    unittest.main()
