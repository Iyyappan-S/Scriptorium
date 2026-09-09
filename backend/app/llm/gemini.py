from backend.app.services.gemini_service import (
    generate_answer,
    classify_query,
)


def generate_summary(query: str, context: str) -> str:
    """
    Generate an academic summary using the retrieved research context.
    """

    prompt = f"""
You are an academic research assistant.

User's research request:
{query}

Retrieved academic research content:
{context}

Create a concise academic summary based ONLY on the retrieved
research content.

Requirements:
- Clearly address the user's research request.
- Identify the main topic.
- Highlight important findings.
- Mention important research insights.
- Use clear academic language.
- Do not invent information.
- Do not add facts that are not present in the provided content.
- If the retrieved content is insufficient, clearly say so.
"""

    return generate_answer(
        context,
        prompt
    )