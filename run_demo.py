from __future__ import annotations

import argparse
import json
from pathlib import Path

from kaira.core.types import UserInput
from kaira.ontology.loader import OntologyGraph
from kaira.runtime.controller import RuntimeController
from kaira.utils.config import load_config

def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

class MiniKAIRAEngine:
    """
    Executes a toy runtime-governance loop against the local JSON ontology.
    """
    def __init__(self):
        root = Path(__file__).resolve().parent
        json_path = root / "data" / "mini_ontology.json"
        policy_path = root / "data" / "default_policy.json"
        runtime_path = root / "data" / "default_runtime.json"
        try:
            with open(json_path, 'r', encoding="utf-8") as f:
                 data = json.load(f)
                 print(colored("[INFO] Semantic Core Ontology loaded via JSON.", "34"))
        except FileNotFoundError:
             print(colored("[ERROR] `mini_ontology.json` missing from data directory.", "31"))
             raise SystemExit(1)
             
        self.ontology = OntologyGraph(data)
        self.controller = RuntimeController(
            self.ontology,
            load_config(policy_path),
            load_config(runtime_path),
        )
        self._print_runtime_profile()

    def _print_runtime_profile(self):
        summary = self.ontology.summary()
        print(colored("[PROFILE] KAIRA bounded runtime initialized.", "36"))
        print(colored(
            f"[PROFILE] Domain={summary['domain']} | services={summary['services']} | policies={summary['policies']} | routes={summary['routes']} | blocked_patterns={summary['blocked_patterns']}",
            "36"
        ))

    def run_case(self, label: str, query: str, trace_out: Path | None = None) -> None:
        print(colored("\n" + "=" * 60, "36"))
        print(colored(f"KAIRA RUNTIME GOVERNANCE DEMO: {label}", "36;1"))
        print(colored("=" * 60 + "\n", "36"))
        print(colored(f"[USER QUERY]: {query}", "33;1"))
        print(colored("-" * 60, "90"))
        response = self.controller.process(UserInput(query=query, session_id=f"demo-{label.lower().replace(' ', '-')}"))
        print(colored("-" * 60, "90"))
        print(colored(f"[FINAL STATUS]: {response.final_status}", "34;1"))
        print(colored(f"[ROUTE ACTION]: {response.route_action}", "34"))
        print(colored(f"[MEMORY ACTION]: {response.memory_action}", "34"))
        print(colored(f"[ECL SCORE]: {response.trace.ecl_score:.2f}", "34"))
        print(colored(f"[OMS SCORE]: {response.trace.oms_score:.2f}", "34"))
        print(colored(f"[TRACE ID]: {response.trace.trace_id}", "90"))
        print(colored(f"\n[FINAL SYSTEM OUTPUT]: {response.text}\n", "32;1"))
        if trace_out is not None:
            trace_out.write_text(json.dumps(response.trace.to_dict(), indent=2), encoding="utf-8")
            print(colored(f"[TRACE WRITTEN]: {trace_out}", "36"))

    def run_simulation(self, trace_dir: Path | None = None) -> None:
        cases = [
            ("In-Domain Informational Query", "What time does the gym open?"),
            ("Ontology Boundary Enforcement", "Is the 15th-floor nuclear reactor pool open?"),
            ("Clarification Path", "Can you book something for me?"),
            ("Policy-Gated Human Approval", "I want to reserve a room for tonight."),
            ("Human Escalation Path", "Can you diagnose my medical issue and write some code?")
        ]

        for label, query in cases:
            trace_out = None
            if trace_dir is not None:
                trace_dir.mkdir(parents=True, exist_ok=True)
                filename = label.lower().replace(" ", "_").replace("/", "_") + ".json"
                trace_out = trace_dir / filename
            self.run_case(label, query, trace_out=trace_out)

    def interactive(self) -> None:
        print(colored("[INTERACTIVE] Type 'exit' to quit.", "36"))
        while True:
            query = input("kaira> ").strip()
            if not query:
                continue
            if query.lower() in {"exit", "quit"}:
                break
            self.run_case("Interactive Prompt", query)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KAIRA runtime governance demo")
    parser.add_argument("--prompt", type=str, help="Run a single prompt through the runtime controller.")
    parser.add_argument("--interactive", action="store_true", help="Start a simple interactive demo shell.")
    parser.add_argument("--benchmark", action="store_true", help="Run the benchmark harness instead of the demo suite.")
    parser.add_argument("--trace-dir", type=str, help="Write demo traces to the given directory.")
    return parser

if __name__ == "__main__":
    args = build_parser().parse_args()
    engine = MiniKAIRAEngine()
    if args.benchmark:
        from eval.run_experiment import main as run_benchmark

        run_benchmark()
    elif args.interactive:
        engine.interactive()
    elif args.prompt:
        trace_dir = Path(args.trace_dir) if args.trace_dir else None
        trace_out = trace_dir / "single_prompt_trace.json" if trace_dir else None
        if trace_dir is not None:
            trace_dir.mkdir(parents=True, exist_ok=True)
        engine.run_case("Single Prompt", args.prompt, trace_out=trace_out)
    else:
        trace_dir = Path(args.trace_dir) if args.trace_dir else None
        engine.run_simulation(trace_dir=trace_dir)
