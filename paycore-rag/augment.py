"""Construction du prompt augmenté avec les chunks retrouvés."""

from typing import Dict, List


def build_augmented_prompt(question: str, retrieved_chunks: List[Dict[str, object]]) -> str:
    """Construit le prompt enrichi qui sera envoyé au LLM."""
    context_blocks = []

    for item in retrieved_chunks:
        chunk = item["chunk"]
        score = item["score"]
        context_blocks.append(
            f"Source: {chunk['source']}\n"
            f"Titre: {chunk['title']}\n"
            f"Score retrieval: {score}\n"
            f"Extrait: {chunk['text']}"
        )

    context = "\n\n---\n\n".join(context_blocks)

    return f"""
Tu es un assistant interne PayCore.
Réponds uniquement à partir des sources fournies dans le CONTEXTE.
Si l'information manque, indique clairement la limite.
Ne promets aucun remboursement automatique.

CONTEXTE :
{context}

QUESTION :
{question}

FORMAT ATTENDU :
Réponse :
Sources utilisées :
Limites :
Validation humaine nécessaire :
""".strip()
