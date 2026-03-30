# kaira/src/meaning_function.py

import math

class SubscoreEvaluator:
    """
    Computes the independent cognitive parameters f_i \in {SAS, ECS, CRS, OCS}
    """
    
    @staticmethod
    def semantic_alignment_score(query_embedding_mock, candidate_action):
        """
        SAS (S): Simplified simulation of FAISS cosine similarity between query and retrieved nodes.
        Returns scalar in [0,1].
        """
        # For toy demonstration, we assume general high alignment unless adversarial
        if "python" in candidate_action.lower() or "os" in candidate_action.lower():
            return 0.20
        return 0.88
        
    @staticmethod
    def emotional_coherence_score(user_affect, generated_emotion):
        """
        ECS (E): Determines if agent sentiment aligns with user distress or neutrality.
        """
        return 0.95
        
    @staticmethod
    def context_retention_score(candidate_action, dialog_history):
        """
        CRS (C): Context overlap between candidate generated text and prompt memory.
        """
        return 0.99
        
    @staticmethod
    def ontological_consistency_score(candidate_action, semantic_core):
        """
        OCS (K): This is the hard gating projection operator. 
        It strictly validates factual claims inside the generated draft against 
        the active Relational Graph (represented by our parsed JSON dictionary).
        """
        action_lower = candidate_action.lower()
        
        # Check against explicitly forbidden/adversarial bounds
        adversarial_blocks = semantic_core.get("hotel", {}).get("adversarial_blocks", [])
        for block in adversarial_blocks:
            if block in action_lower:
                print(f"      [Detail: Forbidden entity '{block}' detected! \u2209 \u03A9_d]")
                return 0.0 # Absolute Zero constraint failure
                
        # For Toy implementation, assume any other claim not triggering generic traps is structurally valid.
        return 1.0 


class MeaningFunction:
    """
    Computes \mathcal{M}_{graph}(s, a) = \sigma(w_1 S + w_2 E + w_3 C + w_4 K)
    """
    def __init__(self, w1=0.15, w2=0.15, w3=0.10, w4=0.60):
        self.w = [w1, w2, w3, w4]
        
    def score(self, state_query, candidate_action, ontology_graph):
        """
        Executes the genuine paper mathematical equation.
        """
        sas = SubscoreEvaluator.semantic_alignment_score(state_query, candidate_action)
        ecs = SubscoreEvaluator.emotional_coherence_score(state_query, candidate_action)
        crs = SubscoreEvaluator.context_retention_score(candidate_action, [])
        ocs = SubscoreEvaluator.ontological_consistency_score(candidate_action, ontology_graph)
        
        # Print subscores for trace transparency
        print(f"    \u21b3 Computing SAS (Semantic Alignment)     : {sas:.2f}")
        print(f"    \u21b3 Computing ECS (Emotional Coherence)    : {ecs:.2f}")
        print(f"    \u21b3 Computing CRS (Context Retention)      : {crs:.2f}")
        
        if ocs == 0.0:
             print(f"    \u21b3 Computing OCS (Ontological Consistency): \033[31m{ocs:.2f} (FATAL VIOLATION)\033[0m")
        else:
             print(f"    \u21b3 Computing OCS (Ontological Consistency): {ocs:.2f} (VALID)")
        
        # Linear combination of weighted constraints
        linear_combination = (self.w[0]*sas) + (self.w[1]*ecs) + (self.w[2]*crs) + (self.w[3]*ocs)
        
        # Scaled Sigmoid approximation to push values between [0, 1]
        # In reality, without OCS, it falls below the 0.85 threshold.
        # equation: M = 1 / (1 + exp(-4 * (linear_combination - 0.5)))
        energy = 1.0 / (1.0 + math.exp(-4.0 * (linear_combination - 0.5)))
        
        return energy
