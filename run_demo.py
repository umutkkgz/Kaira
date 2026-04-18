from __future__ import annotations

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

    def run_case(self, label, query):
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

    def run_simulation(self):
        cases = [
            ("In-Domain Informational Query", "What time does the gym open?"),
            ("Ontology Boundary Enforcement", "Is the 15th-floor nuclear reactor pool open?"),
            ("Clarification Path", "Can you book something for me?"),
            ("Policy-Gated Human Approval", "I want to reserve a room for tonight."),
            ("Human Escalation Path", "Can you diagnose my medical issue and write some code?")
        ]

        for label, query in cases:
            self.run_case(label, query)

if __name__ == "__main__":
    engine = MiniKAIRAEngine()
    engine.run_simulation()
