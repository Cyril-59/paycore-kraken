"""Corpus documentaire PayCore utilisé par le mini-RAG.

Chaque document contient :
- id : identifiant unique ;
- title : titre lisible ;
- source : nom du fichier source fictif ;
- text : contenu documentaire utilisé pour le retrieval.
"""

DOCUMENTS = [
    {
        "id": "doc_1",
        "title": "Procédure double débit",
        "source": "procedure_double_debit.md",
        "text": (
            "Si un client signale un double débit, l'opérateur doit vérifier "
            "l'identifiant de transaction. Il doit comparer les horodatages. "
            "Il doit contrôler le statut des deux opérations. Il doit ouvrir "
            "un ticket d'investigation si les deux débits sont confirmés."
        ),
    },
    {
        "id": "doc_2",
        "title": "Politique remboursement",
        "source": "politique_remboursement.md",
        "text": (
            "Un remboursement ne doit être déclenché qu'après vérification "
            "du statut de paiement. Si le second débit est confirmé comme erreur, "
            "le remboursement est soumis à validation interne."
        ),
    },
    {
        "id": "doc_3",
        "title": "FAQ opérateur",
        "source": "faq_operateur.md",
        "text": (
            "En cas de doute, l'opérateur doit informer le client qu'une vérification "
            "est en cours. Il ne doit pas promettre de remboursement immédiat. "
            "Il doit tracer l'échange dans l'outil support."
        ),
    },
]
