import faiss
import pickle
import os

def verify_embeddings():
    index_path = "backend/embeddings/research.index"
    meta_path = "backend/embeddings/metadata.pkl"
    
    if os.path.exists(index_path) and os.path.exists(meta_path):
        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            metadata = pickle.load(f)
            
        print("FAISS index exists: True")
        print("Metadata exists: True")
        print(f"FAISS vectors: {index.ntotal}")
        print(f"Metadata count: {len(metadata)}")
        print(f"Dimension: {index.d}")
        
        status = "PASS" if index.ntotal == len(metadata) else "FAIL"
        print(f"Status: {status}")
    else:
        print("Embeddings not found")
        
if __name__ == "__main__":
    verify_embeddings()
