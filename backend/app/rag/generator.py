from app.services.gemini_service import generate_answer


def generate_rag_answer(query: str, papers: list) -> str:
    """
    Generate a grounded academic answer using
    research papers retrieved from FAISS.
    """

    if not papers:
        return "No relevant research papers were found."

    context_parts = []

    for index, paper in enumerate(papers, start=1):

        document = paper.get("document", paper)

        title = str(
            document.get(
                "title",
                "Unknown Title"
            )
        ).strip()

        authors = str(
            document.get(
                "authors",
                "Unknown Authors"
            )
        ).strip()

        year = document.get(
            "publication_year",
            "N/A"
        )

        abstract = str(
            document.get(
                "abstract",
                ""
            )
        ).strip()

        concepts = str(
            document.get(
                "concepts",
                ""
            )
        ).strip()

        doi = str(
            document.get(
                "doi",
                ""
            )
        ).strip()

        similarity_score = paper.get(
            "distance",
            "N/A"
        )

        if not abstract:
            abstract = "Abstract not available."

        if not concepts:
            concepts = "Not available."

        if not doi:
            doi = "Not available."

        context_parts.append(
            f"""
============================================================
[RESEARCH PAPER {index}]
============================================================

Title:
{title}

Authors:
{authors}

Publication Year:
{year}

Similarity Score:
{similarity_score}

DOI:
{doi}

Concepts:
{concepts}

Abstract:
{abstract}

============================================================
"""
        )

    context = "\n".join(context_parts)

    return generate_answer(
        context,
        query
    )
