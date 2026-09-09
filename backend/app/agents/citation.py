from .base import BaseAgent
from typing import Dict, Any

class CitationAgent(BaseAgent):
    def __init__(self):
        super().__init__("CitationAgent")

    def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        papers = context.get('papers', []) if context else []
        style = context.get('style', 'IEEE').upper() if context else 'IEEE'
        
        if not papers:
            return {
                "answer": "No papers provided for citation generation.",
                "papers": [],
                "agent_used": self.name
            }
            
        citations = []
        for i, paper in enumerate(papers):
            authors = paper.get('authors', 'Unknown')
            title = paper.get('title', 'Unknown Title')
            year = paper.get('publication_year', 'n.d.')
            doi = paper.get('doi', '')
            
            if style == 'IEEE':
                cit = f"[{i+1}] {authors}, \"{title},\" {year}. {doi}"
            elif style == 'APA':
                cit = f"{authors} ({year}). {title}. {doi}"
            elif style == 'MLA':
                cit = f"{authors}. \"{title}.\" {year}. {doi}"
            else:
                cit = f"{authors} ({year}). {title}."
                
            citations.append(cit)
            
        answer = "Generated Citations:\n\n" + "\n\n".join(citations)
        
        return {
            "answer": answer,
            "papers": papers,
            "agent_used": self.name
        }
