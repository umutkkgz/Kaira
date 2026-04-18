from __future__ import annotations

import unittest

from tests._helpers import make_controller


class TestRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = make_controller()

    def test_router_allows_gym_info(self) -> None:
        route = self.controller.router.route("What time does the gym open?")
        self.assertEqual(route.action, "gym_info")
        self.assertTrue(route.policy_permit)

    def test_router_requires_approval_for_booking(self) -> None:
        route = self.controller.router.route("I want to reserve a room for tonight.")
        self.assertEqual(route.action, "booking_request")
        self.assertTrue(route.human_approval_required)


if __name__ == "__main__":
    unittest.main()
