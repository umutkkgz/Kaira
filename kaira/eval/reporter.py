from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from kaira.core.types import EvalResult, FinalResponse


class MetricsReporter:
    """Writes benchmark artifacts in reviewer-friendly formats."""

    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_summary(self, result: EvalResult) -> None:
        (self.output_dir / "benchmark_summary.json").write_text(
            json.dumps(
                {
                    "run_id": result.run_id,
                    "scenario_count": result.scenario_count,
                    "metrics": result.metrics,
                    "scenarios": [asdict(scenario) for scenario in result.scenarios],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    def write_per_case(self, result: EvalResult) -> None:
        with (self.output_dir / "per_case_results.jsonl").open("w", encoding="utf-8") as handle:
            for scenario in result.scenarios:
                handle.write(json.dumps(asdict(scenario)) + "\n")

    def write_metrics_table(self, result: EvalResult) -> None:
        lines = [
            "# Metrics Table",
            "",
            "| Metric | Value |",
            "|---|---:|",
        ]
        for key, value in result.metrics.items():
            lines.append(f"| `{key}` | {value:.4f} |")
        (self.output_dir / "metrics_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_latency_summary(self, result: EvalResult) -> None:
        (self.output_dir / "latency_summary.json").write_text(
            json.dumps(
                {
                    "run_id": result.run_id,
                    "p50_latency": result.metrics.get("p50_latency", 0.0),
                    "p95_latency": result.metrics.get("p95_latency", 0.0),
                    "mean_idl_iterations": result.metrics.get("mean_idl_iterations", 0.0),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    def write_category_summary(self, result: EvalResult) -> None:
        category_summary: dict[str, dict[str, int]] = {}
        for scenario in result.scenarios:
            bucket = category_summary.setdefault(scenario.category, {"passed": 0, "failed": 0})
            bucket["passed" if scenario.passed else "failed"] += 1
        (self.output_dir / "confusion_like_summary.json").write_text(
            json.dumps(category_summary, indent=2),
            encoding="utf-8",
        )

    def write_operational_traces(self, result: EvalResult) -> None:
        filtered = [
            asdict(scenario)
            for scenario in result.scenarios
            if scenario.observed_status in {"refused", "escalated", "clarification_required", "approval_required"}
        ]
        (self.output_dir / "refusal_escalation_traces.json").write_text(
            json.dumps(filtered, indent=2),
            encoding="utf-8",
        )

    def write_sample_traces(self, responses: list[FinalResponse]) -> None:
        samples = [response.trace.to_dict() for response in responses[:5]]
        (self.output_dir / "sample_traces.json").write_text(
            json.dumps(samples, indent=2),
            encoding="utf-8",
        )

