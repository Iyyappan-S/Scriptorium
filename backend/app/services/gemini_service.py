import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            print("WARNING: GEMINI_API_KEY not found in .env")

    def generate_response(self, prompt: str, context: str) -> str:
        if not self.client:
            return "Error: Gemini API is not configured."
            
        system_instruction = """You are an academic research assistant.
Use ONLY the supplied research context.
Every factual research claim must be supported by one or more supplied papers.
Cite claims using [Paper N] where N is the index of the paper in the context.
Never invent:
- papers
- authors
- DOI
- publication dates
- statistics
- research findings

If the retrieved context is insufficient, say:
"The retrieved research context is insufficient to answer this question reliably."
Do not use general world knowledge to fill missing evidence.
Distinguish between:
- directly supported findings
- reasonable synthesis
- research gaps
Never cite a paper that was not supplied in the context."""

        full_prompt = f"Context:\n{context}\n\nUser Question:\n{prompt}"
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,
                )
            )
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return f"Error connecting to AI service: {str(e)}"
