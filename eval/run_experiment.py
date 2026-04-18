from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kaira.eval.benchmarks import BenchmarkRunner
from kaira.ontology.loader import OntologyGraph
from kaira.runtime.controller import RuntimeController
from kaira.utils.config import load_config


def main() -> None:
    controller = RuntimeController(
        OntologyGraph.from_file(ROOT / "data" / "mini_ontology.json"),
        load_config(ROOT / "data" / "default_policy.json"),
        load_config(ROOT / "data" / "default_runtime.json"),
    )
    result = BenchmarkRunner(controller).export(ROOT / "eval" / "results")
    print(f"KAIRA benchmark run complete: {result.scenario_count} scenarios")
    for key, value in result.metrics.items():
        print(f"- {key}: {value:.4f}")


if __name__ == "__main__":
    main()
