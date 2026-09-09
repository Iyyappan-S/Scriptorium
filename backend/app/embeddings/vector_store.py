import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class VectorStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        print("Initializing VectorStore...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        index_path = os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'research.index')
        meta_path = os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'metadata.pkl')
        
        print(f"Loading FAISS index from {index_path}")
        if os.path.exists(index_path) and os.path.exists(meta_path):
            self.index = faiss.read_index(index_path)
            with open(meta_path, 'rb') as f:
                self.metadata = pickle.load(f)
            print(f"Loaded {self.index.ntotal} vectors.")
        else:
            self.index = None
            self.metadata = []
            print("FAISS index not found. Needs generation.")
            
        self._initialized = True

    def search_vectors(self, query: str, k: int = 5, score_threshold: float = 0.50) -> List[Dict[str, Any]]:
        if not self.index:
            return []
            
        print(f"Searching vectors for query: {query}")
        query_vector = self.model.encode([query]).astype('float32')
        faiss.normalize_L2(query_vector)
        
        # We query for more in case of duplicates or filtering
        search_k = min(k * 2, self.index.ntotal)
        if search_k == 0:
            return []
            
        distances, indices = self.index.search(query_vector, search_k)
        
        results = []
        seen_ids = set()
        
        for i, idx in enumerate(indices[0]):
            distance = float(distances[0][i])
            if distance < score_threshold:
                continue
                
            if idx == -1 or idx >= len(self.metadata):
                continue
                
            meta = self.metadata[idx]
            paper_id = meta.get('id')
            
            if paper_id in seen_ids:
                continue
                
            seen_ids.add(paper_id)
            
            results.append({
                "paper_id": paper_id,
                "title": meta.get("title", ""),
                "authors": meta.get("authors", ""),
                "publication_year": meta.get("publication_year", 2024),
                "abstract": meta.get("abstract", ""),
                "doi": meta.get("doi", ""),
                "concepts": meta.get("concepts", ""),
                "cited_by_count": meta.get("cited_by_count", 0),
                "score": distance
            })
            
            if len(results) >= k:
                break
                
        return results

# Expose a singleton instance retrieval
def get_vector_store():
    return VectorStore()