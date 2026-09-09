from app.embeddings.vector_store import search_vectors


def semantic_search(query: str, top_k: int = 5):
    """
    Perform semantic search using the FAISS vector store.

    Args:
        query: User's research question.
        top_k: Number of relevant papers to retrieve.

    Returns:
        List of relevant research papers.
    """

    return search_vectors(
        query,
        k=top_k
    )
