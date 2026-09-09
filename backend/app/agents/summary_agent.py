from app.agents.base_agent import BaseAgent

from app.rag.search import semantic_search
from app.rag.context import build_context
from app.llm.gemini import generate_summary


class SummaryAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "Summary Agent"
        )

    def execute(self, query: str):

        self.log(
            f"Creating research summary for: {query}"
        )

        # ====================================================
        # STEP 1 — RETRIEVE RESEARCH PAPERS
        # ====================================================

        papers = semantic_search(
            query,
            top_k=5
        )

        self.log(
            f"Retrieved {len(papers)} research papers"
        )

        # ====================================================
        # STEP 2 — BUILD RESEARCH CONTEXT
        # ====================================================

        context = build_context(
            papers
        )

        self.log(
            "Summary context created"
        )

        # ====================================================
        # STEP 3 — GENERATE SUMMARY
        # ====================================================

        summary = generate_summary(
            query,
            context
        )

        self.log(
            "Research summary generated"
        )

        # ====================================================
        # STEP 4 — PREPARE SOURCES
        # ====================================================

        sources = []

        for result in papers:

            document = result.get(
                "document",
                {}
            )

            sources.append({

                "title": document.get(
                    "title",
                    ""
                ),

                "authors": document.get(
                    "authors",
                    ""
                ),

                "publication_year": document.get(
                    "publication_year",
                    ""
                ),

                "doi": document.get(
                    "doi",
                    ""
                )

            })

        # ====================================================
        # STEP 5 — RETURN RESULT
        # ====================================================

        return {

            "agent": self.agent_name,

            "query": query,

            "count": len(papers),

            "summary": summary,

            "sources": sources

        }
