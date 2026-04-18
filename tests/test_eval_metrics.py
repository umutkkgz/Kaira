from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory

from kaira.eval.benchmarks import BenchmarkRunner
from tests._helpers import make_controller


class TestEvalMetrics(unittest.TestCase):
    def test_eval_metrics_exist(self) -> None:
        runner = BenchmarkRunner(make_controller())
        result = runner.run()
        self.assertIn("mean_oms", result.metrics)
        self.assertIn("route_accuracy", result.metrics)
        self.assertGreater(result.scenario_count, 0)

    def test_export_writes_expected_artifacts(self) -> None:
        runner = BenchmarkRunner(make_controller())
        with TemporaryDirectory() as tmp_dir:
            runner.export(tmp_dir)
            from pathlib import Path

            expected = {
                "benchmark_summary.json",
                "benchmark_summary.csv",
                "per_case_results.jsonl",
                "confusion_like_summary.json",
                "refusal_escalation_traces.json",
                "latency_summary.json",
                "sample_traces.json",
                "metrics_table.md",
            }
            self.assertTrue(expected.issubset({path.name for path in Path(tmp_dir).iterdir()}))


if __name__ == "__main__":
    unittest.main()
