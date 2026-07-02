"""Version autonome du mini-RAG en un seul fichier.

Cette version est utile pour les apprenants qui veulent comprendre tout le flux
sans gérer plusieurs imports. La version recommandée du TP reste `rag_demo.py`
avec les fichiers séparés.
"""

import os
import re
from typing import Dict, List
from google import genai

MODEL_NAME = "gemini-2.5-flash"

KEYWORDS = [
    "double",
    "débit",
    "transaction",
    "remboursement",
    "client",
    "ticket",
    "validation",
    "horodatage",
    "opérateur",
    "vérification",
    "statut",
    "support",
]

DOCUMENTS = [
    {
        "id": "doc_1",
        "title": "Procédure double débit",
        "source": "procedure_double_debit.md",
        "text": (
            "Si un client signale un double débit, l'opérateur doit vérifier l'identifiant de transaction. "
            "Il doit comparer les horodatages. Il doit contrôler le statut des deux opérations. "
            "Il doit ouvrir un ticket d'investigation si les deux débits sont confirmés."
        ),
    },
    {
        "id": "doc_2",
        "title": "Politique remboursement",
        "source": "politique_remboursement.md",
        "text": (
            "Un remboursement ne doit être déclenché qu'après vérification du statut de paiement. "
            "Si le second débit est confirmé comme erreur, le remboursement est soumis à validation interne."
        ),
    },
    {
        "id": "doc_3",
        "title": "FAQ opérateur",
        "source": "faq_operateur.md",
        "text": (
            "En cas de doute, l'opérateur doit informer le client qu'une vérification est en cours. "
            "Il ne doit pas promettre de remboursement immédiat. "
            "Il doit tracer l'échange dans l'outil support."
        ),
    },
]


def chunk_document(doc: Dict[str, str]) -> List[Dict[str, str]]:
    sentences = re.split(r"(?<=[.!?])\s+", doc["text"])
    chunks = []
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if sentence:
            chunks.append(
                {
                    "chunk_id": f"{doc['id']}_chunk_{i + 1}",
                    "source": doc["source"],
                    "title": doc["title"],
                    "text": sentence,
                }
            )
    return chunks


def embed_text(text: str) -> List[int]:
    normalized = text.lower()
    return [1 if keyword in normalized else 0 for keyword in KEYWORDS]


def build_index(chunks: List[Dict[str, str]]) -> List[Dict[str, object]]:
    return [{"chunk": chunk, "embedding": embed_text(chunk["text"])} for chunk in chunks]


def similarity(vec_a: List[int], vec_b: List[int]) -> int:
    return sum(1 for a, b in zip(vec_a, vec_b) if a == 1 and b == 1)


def retrieve(question: str, index: List[Dict[str, object]], top_k: int = 3) -> List[Dict[str, object]]:
    question_embedding = embed_text(question)
    scored = []
    for item in index:
        scored.append({"score": similarity(question_embedding, item["embedding"]), "chunk": item["chunk"]})
    scored.sort(key=lambda item: item["score"], reverse=True)

    selected = []
    seen_sources = set()
    for item in scored:
        source = item["chunk"]["source"]
        if source not in seen_sources:
            selected.append(item)
            seen_sources.add(source)
        if len(selected) == top_k:
            break
    return selected


def build_augmented_prompt(question: str, retrieved_chunks: List[Dict[str, object]]) -> str:
    context_blocks = []
    for item in retrieved_chunks:
        chunk = item["chunk"]
        context_blocks.append(
            f"Source: {chunk['source']}\n"
            f"Titre: {chunk['title']}\n"
            f"Score retrieval: {item['score']}\n"
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


def ask_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY est manquante.")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return response.text


if __name__ == "__main__":
    question = "Que doit faire un opérateur PayCore si un client signale un double débit ?"
    chunks = []
    for doc in DOCUMENTS:
        chunks.extend(chunk_document(doc))
    index = build_index(chunks)
    retrieved = retrieve(question, index, top_k=3)
    prompt = build_augmented_prompt(question, retrieved)

    print("\n=== CHUNKS RÉCUPÉRÉS ===\n")
    for item in retrieved:
        print(f"Score: {item['score']}")
        print(f"Source: {item['chunk']['source']}")
        print(f"Texte: {item['chunk']['text']}")
        print("---")

    print("\n=== RÉPONSE GEMINI ===\n")
    print(ask_gemini(prompt))
