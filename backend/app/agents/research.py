from .base import BaseAgent
from typing import Dict, Any
from app.embeddings.vector_store import get_vector_store
from app.services.gemini_service import GeminiService

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("ResearchAgent")
        self.vector_store = get_vector_store()
        self.ai_service = GeminiService()

    def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        k = context.get('k', 5) if context else 5
        threshold = context.get('threshold', 0.50) if context else 0.50
        
        # 1. Retrieve papers
        papers = self.vector_store.search_vectors(query, k=k, score_threshold=threshold)
        
        if not papers:
            return {
                "answer": "No sufficiently relevant research papers were found for this query. Please try a more specific academic query.",
                "papers": [],
                "agent_used": self.name
            }
            
        # 2. Build Context
        context_str = ""
        for i, paper in enumerate(papers):
            context_str += f"[Paper {i+1}]\n"
            context_str += f"Title: {paper['title']}\n"
            context_str += f"Authors: {paper['authors']}\n"
            context_str += f"Year: {paper['publication_year']}\n"
            context_str += f"Abstract: {paper['abstract']}\n"
            context_str += f"DOI: {paper.get('doi', 'Not available')}\n\n"
            
        # 3. Handle low confidence flag
        warning = ""
        if len(papers) <= 2:
            warning = "Only small number of relevant papers retrieved. Keep conclusions conservative.\n"
            
        prompt = warning + query

        # 4. Generate Answer
        answer = self.ai_service.generate_response(prompt=prompt, context=context_str)
        
        # 5. Append Sources automatically if prompt did not format perfectly
        if "Sources:" not in answer and "Sources\n" not in answer:
            answer += "\n\n### Sources\n"
            for i, p in enumerate(papers):
                doi_str = p.get('doi', 'Not available')
                answer += f"[Paper {i+1}] {p['title']} — {p['authors']} — {p['publication_year']} — DOI: {doi_str}\n"

        return {
            "answer": answer,
            "papers": papers,
            "agent_used": self.name
        }
