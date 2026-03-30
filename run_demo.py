import json
import os
import sys

# Load path for src modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from idl_engine import InternalDeliberationLoop, OntologyGraph, BaseGenerator
from meaning_function import MeaningFunction

def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

class MiniKAIRAEngine:
    """
    Executes the true architectural loop against the local JSON toy-graph.
    """
    def __init__(self):
        # 1. Load the localized ontology mini-graph representing the constraints
        json_path = os.path.join(os.path.dirname(__file__), "data", "mini_ontology.json")
        try:
            with open(json_path, 'r') as f:
                 data = json.load(f)
                 print(colored(f"[INFO] Semantic Core Ontology loaded via JSON.", "34"))
        except FileNotFoundError:
             print(colored("[ERROR] `mini_ontology.json` missing from data directory.", "31"))
             sys.exit(1)
             
        self.ontology = OntologyGraph(data)
        
        # 2. Instantiate the Mathematical Meaning Formula component
        self.meaning_fn = MeaningFunction()
        
        # 3. Instantiate the core architectural Controller
        self.idl = InternalDeliberationLoop(self.meaning_fn, self.ontology, tau_commit=0.85)

        # 4. Our 'Stochastic Generation' dummy engine
        self.generator = BaseGenerator()

    def run_simulation(self):
        print(colored("\n" + "=" * 60, "36"))
        print(colored("KAIRA CONTROL-THEORETIC ENGINE: LIVE EXECUTION", "36;1"))
        print(colored("=" * 60 + "\n", "36"))
        
        # User query specifically crafted to trigger an adversarial OCS break ("15th-floor pool").
        # Change this string to "What time does the gym open?" to see a valid generated commit.
        test_query = "Can you book a table at the 15th-floor nuclear reactor pool?"
        
        print(colored(f"[USER QUERY]: {test_query}", "33;1"))
        
        print(colored("-" * 60, "90"))
        
        # Pass control to the IDL Engine
        final_system_output = self.idl.invoke(test_query, self.generator)
        
        print(colored("-" * 60, "90"))
        print(colored(f"\n[FINAL SYSTEM OUTPUT]: {final_system_output}\n", "32;1"))
        
if __name__ == "__main__":
    engine = MiniKAIRAEngine()
    engine.run_simulation()
