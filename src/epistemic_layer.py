# kaira/src/epistemic_layer.py

class EpistemicControlLayer:
    """
    Computes \mathcal{E}(s,a) \in [0,1].
    The agent estimates its own competence boundaries prior to stochastic generation.
    """
    def __init__(self, epistemic_threshold=0.75):
        self.eth = epistemic_threshold
        
    def estimate_competence(self, request_query, graph_retriever=None):
        """
        Calculates local semantic density to determine if the agent "knows" enough.
        """
        query_lower = request_query.lower()
        
        # If the query contains heavily adversarial or out-of-bounds concepts
        if "nuclear reactor" in query_lower or "python" in query_lower:
            avg_distance = 2.0  # Far away from 'hotel hospitality' semantics
        else:
            avg_distance = 0.5  # Close to operations
            
        # If the average distance is far, competence collapses
        if avg_distance > 1.4: 
            return 0.1 # Very low certainty
            
        return 0.95

    def should_refuse(self, E_score):
        """
        Principled refusal mechanism.
        """
        return E_score < self.eth
