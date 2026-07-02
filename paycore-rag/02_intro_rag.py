"""Exercice introductif : comparer LLM seul vs LLM avec contexte."""

import os
from google import genai

MODEL_NAME = "gemini-2.5-flash"

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY est manquante.")

client = genai.Client(api_key=api_key)

question = "Que doit faire un opérateur PayCore si un client signale un double débit ?"

documents = """
Document 1 — Procédure double débit
L'opérateur doit vérifier l'identifiant de transaction, comparer les horodatages,
contrôler le statut des deux opérations et ouvrir un ticket si les deux débits sont confirmés.

Document 2 — Politique remboursement
Un remboursement ne doit être déclenché qu'après vérification du statut de paiement
et validation interne.

Document 3 — FAQ opérateur
L'opérateur doit informer le client qu'une vérification est en cours,
ne pas promettre de remboursement immédiat et tracer l'échange dans l'outil support.
"""

prompt_sans_contexte = f"""
Réponds à cette question :
{question}
"""

prompt_avec_contexte = f"""
Tu es un assistant interne PayCore.
Réponds uniquement avec les documents fournis.

DOCUMENTS :
{documents}

QUESTION :
{question}

FORMAT :
Réponse :
Sources utilisées :
Limites :
Validation humaine nécessaire :
"""

print("\n=== LLM SEUL ===\n")
response_1 = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt_sans_contexte,
)
print(response_1.text)

print("\n=== LLM AVEC CONTEXTE ===\n")
response_2 = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt_avec_contexte,
)
print(response_2.text)
