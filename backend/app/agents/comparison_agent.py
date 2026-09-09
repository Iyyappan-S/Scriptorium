from backend.app.agents.base_agent import BaseAgent
from backend.app.rag.search import semantic_search
from backend.app.rag.context import build_context
from backend.app.llm.gemini import generate_answer


class ComparisonAgent(BaseAgent):

    def __init__(self):
        super().__init__("Comparison Agent")

    def execute(self, query: str):

        self.log(
            f"Comparing research topics: {query}"
        )

        # Retrieve papers relevant to the complete comparison query
        papers = semantic_search(
            query,
            top_k=5
        )

        self.log(
            f"Retrieved {len(papers)} papers"
        )

        if not papers:
            return {
                "success": False,
                "agent": self.agent_name,
                "query": query,
                "comparison": "No relevant research papers were found.",
                "count": 0,
                "papers": []
            }

        # Build research context
        context = build_context(papers)

        comparison_query = f"""
You are an academic research comparison agent.

The user wants to compare the research topics mentioned
in the following question:

User question:
{query}

Use ONLY the research context provided below.

Do NOT invent facts, papers, authors, results, applications,
advantages, limitations, or research directions.

Compare the topics using the following structure:

1. Definition
2. Core concept
3. Methodology
4. Architecture / Approach
5. Applications
6. Advantages
7. Limitations
8. Research challenges
9. Future research directions

Where appropriate, provide a comparison table.

If the provided research context does not contain enough
information for a particular section, explicitly state:

"Insufficient evidence in the retrieved research context."

Maintain an academic and objective tone.

Research Context:
{context}
"""

        comparison = generate_answer(
            comparison_query,
            context
        )

        self.log(
            "Comparison generated successfully"
        )

        return {
            "success": True,
            "agent": self.agent_name,
            "query": query,
            "comparison": comparison,
            "count": len(papers),
            "papers": papers
        }