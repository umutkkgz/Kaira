# Evaluation Surface

The canonical benchmark entry point is:

- [run_experiment.py](run_experiment.py)

Artifacts are exported to:

- `eval/results/benchmark_summary.json`
- `eval/results/per_case_results.jsonl`
- `eval/results/confusion_like_summary.json`
- `eval/results/refusal_escalation_traces.json`
- `eval/results/latency_summary.json`
- `eval/results/sample_traces.json`
- `eval/results/metrics_table.md`

The notebooks in this directory are retained as exploratory analysis artifacts. The benchmark harness in `kaira/eval/` is the canonical implementation.
