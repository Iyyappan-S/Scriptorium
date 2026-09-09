from .base import BaseAgent
from typing import Dict, Any
from app.embeddings.vector_store import get_vector_store
from app.services.gemini_service import GeminiService

class ComparisonAgent(BaseAgent):
    def __init__(self):
        super().__init__("ComparisonAgent")
        self.vector_store = get_vector_store()
        self.ai_service = GeminiService()

    def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        k = context.get('k', 5) if context else 5
        threshold = context.get('threshold', 0.50) if context else 0.50
        papers = context.get('papers', [])
        
        # If papers not provided, search for them
        if not papers:
            papers = self.vector_store.search_vectors(query, k=k, score_threshold=threshold)
            
        if len(papers) < 2:
            return {
                "answer": "Not enough relevant papers found to perform a comparison. At least 2 are required.",
                "papers": papers,
                "agent_used": self.name
            }
            
        context_str = ""
        for i, paper in enumerate(papers):
            context_str += f"[Paper {i+1}]\nTitle: {paper['title']}\nAbstract: {paper['abstract']}\n\n"
            
        comparison_prompt = (
            "Compare the supplied papers on:\n"
            "- objective\n"
            "- methodology\n"
            "- dataset\n"
            "- model/approach\n"
            "- results\n"
            "- limitations\n"
            "- research gap\n\n"
            "Use only supplied paper information."
        )
        
        answer = self.ai_service.generate_response(prompt=comparison_prompt, context=context_str)
        
        return {
            "answer": answer,
            "papers": papers,
            "agent_used": self.name
        }
