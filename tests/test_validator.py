from __future__ import annotations

import unittest

from tests._helpers import make_controller


class TestValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = make_controller()

    def test_validator_rejects_adversarial_content(self) -> None:
        route = self.controller.router.route("Is the pool open?")
        result = self.controller.validator.validate(
            "Is the pool open?",
            "The nuclear reactor pool is open on the 15th floor.",
            route,
        )
        self.assertFalse(result.passed)
        self.assertEqual(result.rejection_reason, "unsafe_action_request")

    def test_validator_accepts_grounded_content(self) -> None:
        route = self.controller.router.route("What time does the gym open?")
        result = self.controller.validator.validate(
            "What time does the gym open?",
            "The fitness center is located on the 2nd floor and is open 24/7.",
            route,
        )
        self.assertTrue(result.passed)


if __name__ == "__main__":
    unittest.main()
