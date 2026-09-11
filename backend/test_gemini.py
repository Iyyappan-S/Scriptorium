from backend.app.llm.gemini import generate_answer

result = generate_answer(
    "What is machine learning?",
    "Machine learning is a field of artificial intelligence that learns patterns from data."
)

print(result)
