from backend.app.rag.embedding import generate_embedding

text = "Artificial Intelligence in Healthcare"

embedding = generate_embedding(text)

print("Embedding Length:", len(embedding))
print(embedding[:10])