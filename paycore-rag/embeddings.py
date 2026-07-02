"""Embedding pédagogique par mots-clés.

Ce fichier ne produit pas un embedding de production. Il transforme un texte en
petit vecteur lisible pour comprendre le principe du retrieval vectoriel.
"""

from typing import List

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


def embed_text(text: str) -> List[int]:
    """Transforme un texte en vecteur binaire basé sur KEYWORDS."""
    normalized = text.lower()
    return [1 if keyword in normalized else 0 for keyword in KEYWORDS]
