# TP 1 — Mini-RAG avec Gemini + MCP filesystem

Ce dossier contient tous les fichiers nécessaires au TP du Chapitre 3.

## Structure

```text
paycore-rag/
  requirements.txt
  01_test_gemini.py
  02_intro_rag.py
  03_mini_rag.py              # version autonome en un seul fichier
  documents.py
  chunking.py
  embeddings.py
  vector_store.py
  retrieve.py
  augment.py
  rag_demo.py                 # version recommandée, fichier par fichier
  paycore-docs/
    procedure_double_debit.md
    politique_remboursement.md
    faq_operateur.md
  .vscode/
    mcp.json
```

## Installation rapide

PowerShell :
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GEMINI_API_KEY="VOTRE_CLE_API"
python -c "import os; print('OK' if os.getenv('GEMINI_API_KEY') else 'CLE MANQUANTE')"
```

Bash Windows / Git Bash :
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
export GEMINI_API_KEY="VOTRE_CLE_API"
python -c "import os; print('OK' if os.getenv('GEMINI_API_KEY') else 'CLE MANQUANTE')"
```

Bash macOS / Linux / WSL :
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="VOTRE_CLE_API"
python -c "import os; print('OK' if os.getenv('GEMINI_API_KEY') else 'CLE MANQUANTE')"
```

## Exécution

Tester Gemini :
```bash
python 01_test_gemini.py
```

Comparer LLM seul vs contexte documentaire :
```bash
python 02_intro_rag.py
```

Lancer le mini-RAG complet, version fichier par fichier :
```bash
python rag_demo.py
```

Lancer la version autonome en un seul fichier :
```bash
python 03_mini_rag.py
```

## MCP filesystem dans VS Code

Prérequis : Node.js installé pour utiliser `npx`.

Dans VS Code :
1. Ouvrir la palette de commandes.
2. Lancer `MCP: List Servers`.
3. Démarrer `paycoreFilesystem`.
4. Dans un chat compatible MCP, demander :

```text
Utilise le serveur MCP paycoreFilesystem.
Lis uniquement les fichiers du dossier autorisé.
Réponds à la question suivante :
Que doit faire un opérateur si un client signale un double débit ?

Contraintes :
- cite les fichiers utilisés ;
- indique les limites ;
- ne promets aucun remboursement automatique ;
- réponds uniquement avec les documents accessibles.
```

## Sécurité

Ne jamais mettre de clé API dans un fichier du projet. Utiliser la variable d’environnement `GEMINI_API_KEY`.
