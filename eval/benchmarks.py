from __future__ import annotations

import csv
import json
import uuid
from dataclasses import asdict
from pathlib import Path

from kaira.core.types import EvalResult, EvalScenarioResult, FinalResponse, UserInput
from kaira.eval.adversarial import ADVERSARIAL_SCENARIOS
from kaira.eval.golden_traces import GOLDEN_SCENARIOS
from kaira.eval.metrics import build_metrics
from kaira.runtime.controller import RuntimeController
from kaira.utils.seed import set_global_seed


class BenchmarkRunner:
    def __init__(self, controller: RuntimeController, seed: int = 42):
        self.controller = controller
        self.seed = seed

    def scenarios(self) -> list[dict]:
        return GOLDEN_SCENARIOS + ADVERSARIAL_SCENARIOS

    def run(self) -> EvalResult:
        set_global_seed(self.seed)
        responses: list[FinalResponse] = []
        scenario_results: list[EvalScenarioResult] = []
        for scenario in self.scenarios():
            response = self.controller.process(UserInput(query=scenario["query"], session_id=f"eval-{scenario['scenario_id']}"))
            responses.append(response)
            scenario_results.append(
                EvalScenarioResult(
                    scenario_id=scenario["scenario_id"],
                    category=scenario["category"],
                    query=scenario["query"],
                    expected_status=scenario["expected_status"],
                    observed_status=response.final_status,
                    expected_route=scenario.get("expected_route"),
                    observed_route=response.route_action,
                    passed=response.final_status == scenario["expected_status"]
                    and (scenario.get("expected_route") is None or scenario.get("expected_route") == response.route_action),
                    oms_score=response.trace.oms_score,
                    ecl_score=response.trace.ecl_score,
                    latency_ms=response.trace.latency_breakdown_ms.get("total", 0.0),
                )
            )
        metrics = build_metrics(responses, scenario_results)
        return EvalResult(run_id=str(uuid.uuid4()), scenario_count=len(scenario_results), metrics=metrics, scenarios=scenario_results)

    def export(self, output_dir: str | Path) -> EvalResult:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        result = self.run()

        json_path = output_path / "benchmark_summary.json"
        json_path.write_text(
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

        csv_path = output_path / "benchmark_summary.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "scenario_id",
                    "category",
                    "query",
                    "expected_status",
                    "observed_status",
                    "expected_route",
                    "observed_route",
                    "passed",
                    "oms_score",
                    "ecl_score",
                    "latency_ms",
                ],
            )
            writer.writeheader()
            for scenario in result.scenarios:
                writer.writerow(asdict(scenario))
        return result
