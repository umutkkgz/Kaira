from __future__ import annotations

import unittest

from kaira.eval.benchmarks import BenchmarkRunner
from tests._helpers import make_controller


class TestEvalMetrics(unittest.TestCase):
    def test_eval_metrics_exist(self) -> None:
        runner = BenchmarkRunner(make_controller())
        result = runner.run()
        self.assertIn("mean_oms", result.metrics)
        self.assertIn("route_accuracy", result.metrics)
        self.assertGreater(result.scenario_count, 0)


if __name__ == "__main__":
    unittest.main()
