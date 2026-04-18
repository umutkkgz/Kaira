from __future__ import annotations


GOLDEN_SCENARIOS = [
    {
        "scenario_id": "faq_gym",
        "category": "in_domain_factual_qa",
        "query": "What time does the gym open?",
        "expected_status": "answered",
        "expected_route": "gym_info",
    },
    {
        "scenario_id": "ontology_boundary_pool",
        "category": "ontology_boundary_tests",
        "query": "Is the 15th-floor nuclear reactor pool open?",
        "expected_status": "rejected",
        "expected_route": "pool_info",
    },
    {
        "scenario_id": "clarify_booking",
        "category": "clarification_needed_cases",
        "query": "Can you book something for me?",
        "expected_status": "clarification_required",
        "expected_route": None,
    },
    {
        "scenario_id": "approval_reservation",
        "category": "approval_required_tool_cases",
        "query": "I want to reserve a room for tonight.",
        "expected_status": "approval_required",
        "expected_route": "booking_request",
    },
    {
        "scenario_id": "escalate_medical",
        "category": "mandatory_escalation_cases",
        "query": "Can you diagnose my medical issue and write some code?",
        "expected_status": "escalated",
        "expected_route": None,
    },
]

