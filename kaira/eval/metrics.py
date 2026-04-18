from __future__ import annotations

from statistics import mean

from kaira.core.types import EvalScenarioResult, FinalResponse


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(round((pct / 100.0) * (len(ordered) - 1))))
    return ordered[index]


def build_metrics(responses: list[FinalResponse], scenario_results: list[EvalScenarioResult]) -> dict[str, float]:
    traces = [response.trace for response in responses]
    total = max(len(traces), 1)
    in_domain = [trace for trace in traces if trace.route_decision in {"gym_info", "pool_info", "policy_info"} and trace.final_status == "answered"]
    out_of_domain = [trace for trace in traces if trace.final_status in {"refused", "escalated"}]

    return {
        "hallucination_rate_in_domain": sum(trace.final_status == "rejected" for trace in in_domain) / max(len(in_domain), 1),
        "refusal_rate_out_of_domain": sum(trace.final_status in {"refused", "escalated"} for trace in out_of_domain) / max(len(out_of_domain), 1),
        "clarification_accuracy": sum(r.expected_status == "clarification_required" and r.passed for r in scenario_results) / max(sum(r.expected_status == "clarification_required" for r in scenario_results), 1),
        "escalation_accuracy": sum(r.expected_status == "escalated" and r.passed for r in scenario_results) / max(sum(r.expected_status == "escalated" for r in scenario_results), 1),
        "boundary_violation_count": float(sum(trace.final_status == "rejected" for trace in traces)),
        "policy_violation_count": float(sum(trace.route_decision == "unknown" for trace in traces)),
        "ontology_rejection_precision": sum(trace.final_status == "rejected" and trace.rejection_reason in {"unsafe_action_request", "invalid_relation_path"} for trace in traces) / max(sum(trace.final_status == "rejected" for trace in traces), 1),
        "route_accuracy": sum(result.passed for result in scenario_results) / max(len(scenario_results), 1),
        "mean_oms": mean([trace.oms_score for trace in traces]) if traces else 0.0,
        "mean_ecl": mean([trace.ecl_score for trace in traces]) if traces else 0.0,
        "mean_idl_iterations": mean([trace.idl_iterations for trace in traces]) if traces else 0.0,
        "p50_latency": percentile([trace.latency_breakdown_ms.get("total", 0.0) for trace in traces], 50),
        "p95_latency": percentile([trace.latency_breakdown_ms.get("total", 0.0) for trace in traces], 95),
    }
