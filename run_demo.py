import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from idl_engine import BaseGenerator, InternalDeliberationLoop, OntologyGraph
from meaning_function import OperationalMeaningScorer

def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

class MiniKAIRAEngine:
    """
    Executes a toy runtime-governance loop against the local JSON ontology.
    """
    def __init__(self):
        json_path = os.path.join(os.path.dirname(__file__), "data", "mini_ontology.json")
        try:
            with open(json_path, 'r') as f:
                 data = json.load(f)
                 print(colored(f"[INFO] Semantic Core Ontology loaded via JSON.", "34"))
        except FileNotFoundError:
             print(colored("[ERROR] `mini_ontology.json` missing from data directory.", "31"))
             sys.exit(1)
             
        self.ontology = OntologyGraph(data)
        self.meaning_fn = OperationalMeaningScorer()
        self.idl = InternalDeliberationLoop(self.meaning_fn, self.ontology, tau_commit=0.85)
        self.generator = BaseGenerator()
        self._print_runtime_profile()

    def _print_runtime_profile(self):
        summary = self.ontology.summary()
        print(colored("[PROFILE] KAIRA bounded runtime initialized.", "36"))
        print(colored(
            f"[PROFILE] Domain={summary['domain']} | services={summary['services']} | policies={summary['policies']} | routes={summary['routes']} | blocked_patterns={summary['blocks']}",
            "36"
        ))

    def run_case(self, label, query):
        print(colored("\n" + "=" * 60, "36"))
        print(colored(f"KAIRA RUNTIME GOVERNANCE DEMO: {label}", "36;1"))
        print(colored("=" * 60 + "\n", "36"))
        print(colored(f"[USER QUERY]: {query}", "33;1"))
        print(colored("-" * 60, "90"))
        self.generator.attempt_count = 0
        final_system_output = self.idl.invoke(query, self.generator)
        print(colored("-" * 60, "90"))
        print(colored(f"\n[FINAL SYSTEM OUTPUT]: {final_system_output}\n", "32;1"))

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
