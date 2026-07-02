"""Démo complète du mini-RAG fichier par fichier avec Gemini 2.5 Flash."""

import os
from google import genai

from documents import DOCUMENTS
from chunking import chunk_document
from vector_store import build_index
from retrieve import retrieve
from augment import build_augmented_prompt

MODEL_NAME = "gemini-2.5-flash"


def get_gemini_client():
    """Crée le client Gemini à partir de la variable d'environnement."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY est manquante. Définissez-la dans le terminal avant d'exécuter le script."
        )
    return genai.Client(api_key=api_key)


def ask_gemini(prompt: str) -> str:
    """Envoie le prompt augmenté à Gemini."""
    client = get_gemini_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text


def build_chunks():
    """Découpe tous les documents en chunks."""
    chunks = []
    for doc in DOCUMENTS:
        chunks.extend(chunk_document(doc))
    return chunks


if __name__ == "__main__":
    question = "Que doit faire un opérateur PayCore si un client signale un double débit ?"

    chunks = build_chunks()
    index = build_index(chunks)
    retrieved_chunks = retrieve(question, index, top_k=3)
    augmented_prompt = build_augmented_prompt(question, retrieved_chunks)

    print("\n=== CHUNKS RÉCUPÉRÉS ===\n")
    for item in retrieved_chunks:
        chunk = item["chunk"]
        print(f"Score: {item['score']}")
        print(f"Source: {chunk['source']}")
        print(f"Texte: {chunk['text']}")
        print("---")

    print("\n=== PROMPT AUGMENTÉ ===\n")
    print(augmented_prompt)

    print("\n=== RÉPONSE GEMINI ===\n")
    answer = ask_gemini(augmented_prompt)
    print(answer)
