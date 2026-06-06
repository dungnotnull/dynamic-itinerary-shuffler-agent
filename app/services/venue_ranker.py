from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.config import settings
import logging

logger = logging.getLogger("VenueRanker")

class VenueRanker:
    """
    Professional Semantic Ranker. 
    Fuses Embedding Similarity with LLM Reasoning.
    """
    def __init__(self):
        # Local SLM for fast embedding calculations
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def calculate_similarity(self, user_pref_vec: List[float], candidate_vecs: List[List[float]]) -> List[float]:
        """Computes cosine similarity between user preference and candidate venues."""
        u = np.array(user_pref_vec)
        c_matrix = np.array(candidate_vecs)
        
        # Cosine similarity: (A dot B) / (||A|| * ||B||)
        dot_product = np.dot(c_matrix, u)
        norms = np.linalg.norm(c_matrix, axis=1) * np.linalg.norm(u)
        return (dot_product / norms).tolist()

    async def get_llm_decision(self, prompt: str, provider: str = "anthropic") -> str:
        """
        Pluggable LLM Chain: Claude -> GPT-4o -> Ollama.
        """
        # Implementation of the API call sequence
        try:
            if provider == "anthropic":
                # async with httpx.AsyncClient() as client:
                #     res = await client.post("https://api.anthropic.com/v1/messages", ...)
                return "Mocked Claude Decision: Venue B is better because it's indoors and matches the 'Arts' preference."
            elif provider == "openai":
                return "Mocked GPT-4o Decision: Venue A is the closest substitute."
            else:
                return "Mocked Ollama Decision: local reasoning selected Venue C."
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return "Fallback: Defaulting to highest embedding score."

    async def rank_alternatives(self, 
                                 user_profile: Dict[str, Any], 
                                 candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Full pipeline: Embeddings -> Top K -> LLM Final Selection.
        """
        # 1. Convert user profile to a preference vector (simplified for this implementation)
        # In real run: combine embeddings of liked venues and preference keywords
        user_pref_text = f"{user_profile.get('vibe', '')} {user_profile.get('interests', '')}"
        user_vec = self.embedder.encode(user_pref_text).tolist()
        
        # 2. Calculate similarities for all candidates
        cand_vecs = [c['embedding'] for c in candidates]
        similarities = self.calculate_similarity(user_vec, cand_vecs)
        
        # 3. Filter top 3 candidates
        top_indices = np.argsort(similarities)[-3:][::-1]
        top_candidates = [candidates[i] for i in top_indices]
        
        # 4. LLM Contextual Reasoning
        prompt = f"User profile: {user_profile}. Candidates: {top_candidates}. Select the best one and provide rationale."
        decision = await self.get_llm_decision(prompt)
        
        return {
            "selected_venue": top_candidates[0], # In real run, parse the decision string
            "rationale": decision,
            "all_scores": similarities
        }
