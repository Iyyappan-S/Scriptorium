from backend.app.agents.base_agent import BaseAgent

from backend.app.rag.search import semantic_search


class CitationAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "Citation Agent"
        )


    def execute(self, query: str):

        self.log(
            f"Generating citations for: {query}"
        )


        # Retrieve relevant papers
        papers = semantic_search(
            query,
            top_k=5
        )


        citations = []


        for paper in papers:

            document = paper.get(
                "document",
                {}
            )


            title = document.get(
                "title",
                "Unknown Title"
            )


            authors = document.get(
                "authors",
                "Unknown Authors"
            )


            year = document.get(
                "publication_year",
                ""
            )


            doi = document.get(
                "doi",
                ""
            )


            # -----------------------------------------
            # APA STYLE
            # -----------------------------------------

            citation = (
                f"{authors} "
                f"({year}). "
                f"{title}. "
                f"{doi}"
            )


            citations.append(
                citation
            )


        return {

            "success": True,

            "agent": self.agent_name,

            "query": query,

            "count": len(citations),

            "citations": citations,

            "papers": papers

        }