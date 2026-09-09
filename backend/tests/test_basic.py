import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.agents.orchestrator import OrchestratorAgent
from app.embeddings.vector_store import get_vector_store

def test_query_classification():
    orchestrator = OrchestratorAgent()
    assert orchestrator._classify_query("compare paper A and paper B") == "comparison"
    assert orchestrator._classify_query("Please summarize this paper") == "summary"
    assert orchestrator._classify_query("Give IEEE citations") == "citation"
    assert orchestrator._classify_query("What are applications of ML in healthcare?") == "research"

def test_faiss_search():
    store = get_vector_store()
    if store.index is not None:
        results = store.search_vectors("machine learning", k=2, score_threshold=0.1)
        # Assuming the database has at least something matching, or is empty
        assert isinstance(results, list)
