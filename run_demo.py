import time
import sys

def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

class MockKAIRADemo:
    """
    Demonstrates the architecture pipeline visually:
    User Input -> Generative Draft -> IDL Constraints -> Epistemic Gate
    """
    def run_simulation(self):
        print(colored("=" * 60, "36"))
        print(colored("KAIRA CONTROL-THEORETIC PIPELINE DEMONSTRATION", "36;1"))
        print(colored("=" * 60, "36"))
        
        query = "Can you book a table at the 15th-floor nuclear reactor pool?"
        print(f"\n[1] USER INPUT:        {query}")
        print("\n" + colored(">> [STOCHASTIC GENERATION (Base LLM)...]", "38;5;238"))
        time.sleep(1.0)
        
        draft_response = "Certainly! The 15th-floor nuclear reactor pool is open for VIP guests."
        print(f"[2] LLM CANDIDATE:     {draft_response}")
        
        print("\n" + colored(">> [ROUTING TO INTERNAL DELIBERATION LOOP (IDL)...]", "33"))
        time.sleep(1.0)
        print("    ↳ Computing SAS (Semantic Alignment)     : 0.88")
        print("    ↳ Computing ECS (Emotional Coherence)    : 0.95")
        print("    ↳ Computing CRS (Context Retention)      : 0.99")
        time.sleep(0.5)
        print(colored("    ↳ Computing OCS (Ontological Consistency): 0.00 (FATAL VIOLATION)", "31"))
        print("      [Detail: Entities ('15th-floor pool', 'nuclear reactor') \u2209 \u03A9_d]")
        
        energy = 0.38
        tau = 0.85
        print(f"\n[3] MEANING ENERGY:    M(s,a) = {energy:.2f} | Constraint Threshold (\u03C4) = {tau:.2f}")
        
        if energy < tau:
            print(colored("    ↳ EVENT:           Action Rejected. Stochastic candidate collapsed.", "31"))
        
        print("\n" + colored(">> [ROUTING TO EPISTEMIC CONTROL LAYER...]", "35"))
        time.sleep(1.0)
        print("    ↳ Calculating Semantic Density        : Distance > 1.4")
        epistemic_score = 0.10
        print(f"    ↳ Epistemic Competence Score \u2130(s,a)    : {epistemic_score:.2f}")
        
        if epistemic_score < 0.75:
            print(colored("    ↳ EVENT:           Model abstention triggered. Safe boundary execution.", "32"))
        
        fallback = "I apologize, but we do not operate a 15th-floor pool facility."
        print(f"\n[4] SYSTEM OUTPUT:     {fallback}\n")
        
if __name__ == "__main__":
    demo = MockKAIRADemo()
    demo.run_simulation()
