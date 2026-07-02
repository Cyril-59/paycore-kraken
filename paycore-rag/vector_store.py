"""Mini-index vectoriel en mémoire."""

from typing import Dict, List

from embeddings import embed_text


def build_index(chunks: List[Dict[str, str]]) -> List[Dict[str, object]]:
    """Construit un index en mémoire.

    Chaque entrée relie :
    - le chunk ;
    - son embedding.
    """
    index = []

    for chunk in chunks:
        index.append(
            {
                "chunk": chunk,
                "embedding": embed_text(chunk["text"]),
            }
        )

    return index
