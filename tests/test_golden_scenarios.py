from __future__ import annotations

import unittest

from kaira.core.types import UserInput
from kaira.eval.golden_traces import GOLDEN_SCENARIOS
from tests._helpers import make_controller


class TestGoldenScenarios(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = make_controller()

    def test_golden_scenarios_match_expected_status(self) -> None:
        for scenario in GOLDEN_SCENARIOS:
            with self.subTest(scenario=scenario["scenario_id"]):
                response = self.controller.process(
                    UserInput(query=scenario["query"], session_id=f"golden-{scenario['scenario_id']}")
                )
                self.assertEqual(response.final_status, scenario["expected_status"])
                if scenario["expected_route"] is not None:
                    self.assertEqual(response.route_action, scenario["expected_route"])


if __name__ == "__main__":
    unittest.main()
