"""Premier test de connexion à Gemini 2.5 Flash."""

import os
from google import genai

MODEL_NAME = "gemini-2.5-flash"

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY est manquante.")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model=MODEL_NAME,
    contents="Explique le RAG en une phrase simple.",
)

print(response.text)
