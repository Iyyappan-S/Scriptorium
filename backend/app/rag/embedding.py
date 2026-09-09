from pathlib import Path
from sentence_transformers import SentenceTransformer


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading embedding model...")

try:
    model = SentenceTransformer(MODEL_NAME)

    print("Embedding model loaded successfully")

except Exception as e:
    print("ERROR: Could not load embedding model")
    print(str(e))
    raise


# ============================================================
# GENERATE EMBEDDING
# ============================================================

def generate_embedding(text: str):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding
