from backend.app.agents.base_agent import BaseAgent
from backend.app.rag.search import semantic_search
from backend.app.rag.generator import generate_rag_answer


class ResearchAgent(BaseAgent):

    def __init__(self):
        super().__init__("Research Agent")

    def execute(self, query: str):

        self.log(
            f"Searching research papers for: {query}"
        )

        papers = semantic_search(
            query,
            top_k=5
)
        answer = generate_rag_answer(
            query,
            papers
        )

        return {
            "query": query,
            "answer": answer,
            "papers": papers,
            "count": len(papers),
            "agent": self.agent_name
        }