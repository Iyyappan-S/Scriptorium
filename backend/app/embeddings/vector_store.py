from typing import List, Dict, Any
from backend.app.services.search_service import search_papers

class VectorStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized: return
        self._initialized = True

    def search_vectors(self, query: str, k: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        print(f"Fallback MOCK Vector Search (MongoDB Regex) for query: {query}")
        raw_papers = search_papers(query, limit=k)
        
        results = []
        for p in raw_papers:
            results.append({
                "paper_id": p.get('id', 'unknown'),
                "title": p.get("title", ""),
                "authors": p.get("authors", ""),
                "publication_year": p.get("publication_year", 2024),
                "abstract": p.get("abstract", ""),
                "doi": p.get("doi", ""),
                "concepts": p.get("concepts", ""),
                "cited_by_count": p.get("cited_by_count", 0),
                "score": 0.85 # Mock semantic score
            })
        return results

def get_vector_store():
    return VectorStore()