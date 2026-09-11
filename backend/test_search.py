from backend.app.rag.embedding import generate_embedding
from backend.app.rag.vector_store import VectorStore
import json
print("Loading FAISS index...")

store = VectorStore()
store.load()

print("Generating embedding...")

embedding = generate_embedding("machine learning")

print("Searching...")

result = store.search(embedding, 1)

print("\nSEARCH RESULT:")
print(result)

print("\nTESTING JSON SERIALIZATION:")

try:
    output = json.dumps(result, indent=2, allow_nan=False)
    print(output)
    print("\nSUCCESS: Result is valid JSON.")
except Exception as e:
    print("\nJSON ERROR:")
    print(type(e).__name__)
    print(str(e))
