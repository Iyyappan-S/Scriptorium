def build_context(papers):

    context_parts = []

    for i, result in enumerate(papers, start=1):

        document = result.get(
            "document",
            {}
        )

        title = document.get(
            "title",
            ""
        )

        abstract = document.get(
            "abstract",
            ""
        )

        authors = document.get(
            "authors",
            ""
        )

        year = document.get(
            "publication_year",
            ""
        )

        doi = document.get(
            "doi",
            ""
        )

        concepts = document.get(
            "concepts",
            ""
        )

        cited_by_count = document.get(
            "cited_by_count",
            0
        )

        # Handle missing abstract
        if not isinstance(
            abstract,
            str
        ):
            abstract = ""

        # Handle missing authors
        if not isinstance(
            authors,
            str
        ):
            authors = ""

        # Handle missing concepts
        if not isinstance(
            concepts,
            str
        ):
            concepts = ""

        paper_context = f"""
==============================
RESEARCH PAPER {i}
==============================

Title:
{title}

Authors:
{authors}

Publication Year:
{year}

Citation Count:
{cited_by_count}

Concepts:
{concepts}

Abstract:
{abstract}

DOI:
{doi}

"""

        context_parts.append(
            paper_context
        )

    return "\n".join(
        context_parts
    )