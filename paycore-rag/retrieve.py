"""Retrieval : recherche des chunks les plus proches d'une question."""

from typing import Dict, List

from embeddings import embed_text


def similarity(vec_a: List[int], vec_b: List[int]) -> int:
    """Compte les mots-clés actifs communs entre deux vecteurs.

    Cette similarité est pédagogique. En production, on utiliserait plutôt une
    similarité cosinus sur de vrais embeddings.
    """
    matches = 0
    for a, b in zip(vec_a, vec_b):
        if a == 1 and b == 1:
            matches += 1
    return matches


def retrieve(question: str, index: List[Dict[str, object]], top_k: int = 3) -> List[Dict[str, object]]:
    """Récupère les top-k chunks les plus proches de la question.

    Pour le TP, on diversifie les sources afin d'éviter que tous les résultats
    viennent du même document lorsque plusieurs documents sont utiles.
    """
    question_embedding = embed_text(question)
    scored_chunks = []

    for item in index:
        score = similarity(question_embedding, item["embedding"])
        scored_chunks.append(
            {
                "score": score,
                "chunk": item["chunk"],
            }
        )

    scored_chunks.sort(key=lambda item: item["score"], reverse=True)

    # Diversification pédagogique par source.
    selected = []
    seen_sources = set()

    for item in scored_chunks:
        source = item["chunk"]["source"]
        if source not in seen_sources:
            selected.append(item)
            seen_sources.add(source)
        if len(selected) == top_k:
            break

    # Compléter si le corpus ne contient pas assez de sources distinctes.
    if len(selected) < top_k:
        for item in scored_chunks:
            if item not in selected:
                selected.append(item)
            if len(selected) == top_k:
                break

    return selected
