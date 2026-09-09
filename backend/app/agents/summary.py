from .base import BaseAgent
from typing import Dict, Any
from app.embeddings.vector_store import get_vector_store
from app.services.gemini_service import GeminiService

class SummaryAgent(BaseAgent):
    def __init__(self):
        super().__init__("SummaryAgent")
        self.vector_store = get_vector_store()
        self.ai_service = GeminiService()

    def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        k = context.get('k', 1) if context else 1
        threshold = context.get('threshold', 0.50) if context else 0.50
        papers = context.get('papers', [])
        
        if not papers:
            papers = self.vector_store.search_vectors(query, k=k, score_threshold=threshold)
            
        if not papers:
            return {
                "answer": "No sufficiently relevant research papers were found to summarize.",
                "papers": [],
                "agent_used": self.name
            }
            
        paper = papers[0]
        context_str = f"Title: {paper['title']}\nAbstract: {paper['abstract']}\n"
        
        summary_prompt = (
            "Generate a structured summary from this paper text:\n"
            "Summary\n"
            "Problem\n"
            "Methodology\n"
            "Dataset\n"
            "Main Findings\n"
            "Limitations\n"
            "Research Gap\n"
            "Never invent information absent from the paper."
        )
        
        answer = self.ai_service.generate_response(prompt=summary_prompt, context=context_str)
        
        return {
            "answer": answer,
            "papers": papers,
            "agent_used": self.name
        }
