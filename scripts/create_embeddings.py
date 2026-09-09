import pandas as pd
import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer

def create_embeddings():
    print("Loading dataset...")
    df = pd.read_csv("../dataset/processed/clean_research_papers.csv")
    
    print("Loading SentenceTransformer...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Generating embeddings...")
    texts = []
    for _, row in df.iterrows():
        text = f"Title: {row['title']}\nAbstract: {row['abstract']}\nConcepts: {row['concepts']}"
        texts.append(text)
        
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=128)
    embeddings = np.array(embeddings).astype('float32')
    
    print("Creating FAISS index...")
    # Normalize for inner product (cosine similarity equivalent)
    faiss.normalize_L2(embeddings)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    os.makedirs("../backend/embeddings", exist_ok=True)
    faiss.write_index(index, "../backend/embeddings/research.index")
    
    print("Saving metadata...")
    metadata = df.to_dict('records')
    with open("../backend/embeddings/metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)
        
    print(f"FAISS index created with {index.ntotal} vectors.")
    print("Embeddings generated successfully.")

if __name__ == "__main__":
    create_embeddings()