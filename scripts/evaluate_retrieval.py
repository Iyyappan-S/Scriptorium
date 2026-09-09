import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from app.embeddings.vector_store import get_vector_store

def evaluate():
    store = get_vector_store()
    
    queries = [
        "machine learning applications in healthcare",
        "deep learning medical image analysis",
        "history of ancient Roman architecture",
        "random unrelated text that shouldn't match anything"
    ]
    
    threshold = 0.50
    k = 5
    
    print("\nRETRIEVAL EVALUATION")
    print("-" * 30)
    for q in queries:
        print(f"\nQuery: '{q}'")
        results = store.search_vectors(q, k=k, score_threshold=threshold)
        print(f"Results found (passing threshold {threshold}): {len(results)}")
        for r in results:
            print(f"  - [{r['score']:.4f}] {r['title']}")

if __name__ == "__main__":
    evaluate()
