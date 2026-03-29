# kaira/src/epistemic_layer.py

class EpistemicControlLayer:
    """
    Computes \mathcal{E}(s,a) \in [0,1].
    The agent estimates its own competence boundaries prior to stochastic generation.
    """
    def __init__(self, epistemic_threshold=0.75):
        self.eth = epistemic_threshold
        
    def estimate_competence(self, request_query, graph_retriever):
        """
        Calculates local semantic density to determine if the agent "knows" enough.
        """
        # Node density retrieved via FAISS vector distance vs semantic core
        retrieved_nodes, avg_distance = graph_retriever.search(request_query)
        
        # If the average distance is far, competence collapses
        if avg_distance > 1.4: 
            return 0.1 # Very low certainty
            
        # If there are dense supporting graph relationships, competence is high
        if len(retrieved_nodes) >= 3:
            return 0.95
            
        return 0.5

    def should_refuse(self, E_score):
        """
        Principled refusal mechanism blocking hallucination before LLM token generation begins.
        """
        return E_score < self.eth
