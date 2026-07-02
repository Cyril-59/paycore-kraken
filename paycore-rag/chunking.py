"""Découpage des documents en chunks sourçables."""

import re
from typing import Dict, List


def chunk_document(doc: Dict[str, str]) -> List[Dict[str, str]]:
    """Découpe un document en fragments courts.

    Chaque chunk conserve sa source afin que la réponse finale puisse citer
    les documents utilisés.
    """
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
