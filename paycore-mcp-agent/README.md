# TP Chapitre 4 — Serveur MCP custom & agent contrôlé

Ce dossier contient tous les fichiers nécessaires au TP : serveur MCP custom, base SQLite fictive, outils SQL read-only, agent Gemini et orchestration multi-agents.

## 1. Créer et ouvrir le projet

```bash
mkdir paycore-mcp-agent
cd paycore-mcp-agent
code .
```

Copiez les fichiers de cette archive dans le dossier `paycore-mcp-agent`.

## 2. Créer l'environnement Python

PowerShell :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloque :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Bash Windows / Git Bash :

```bash
python -m venv .venv
source .venv/Scripts/activate
```

macOS / Linux / WSL :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 4. Configurer Gemini

PowerShell :

```powershell
$env:GEMINI_API_KEY="VOTRE_CLE_API"
```

Bash :

```bash
export GEMINI_API_KEY="VOTRE_CLE_API"
```

Tester :

```bash
python -c "import os; print('OK' if os.getenv('GEMINI_API_KEY') else 'CLE MANQUANTE')"
```

## 5. Créer et tester la base

```bash
python setup_db.py
```

Vérifier qu'il y a 4 lignes :

```bash
python -c "import sqlite3; conn=sqlite3.connect('paycore_demo.db'); print(conn.execute('SELECT COUNT(*) FROM incidents').fetchone()); conn.close()"
```

Résultat attendu :

```text
(4,)
```

## 6. Tester les outils SQL

```bash
python test_db_tools.py
```

Résultat attendu :
- le schéma s'affiche ;
- la requête SELECT fonctionne ;
- la requête DELETE est bloquée.

## 7. Tester le serveur MCP manuellement

```bash
python mcp_server.py
```

Le terminal reste actif. Arrêtez avec :

```text
Ctrl + C
```

## 8. Configurer MCP dans VS Code

Le fichier `.vscode/mcp.json` fourni est configuré pour Windows :

```json
{
  "servers": {
    "paycoreDb": {
      "type": "stdio",
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
      "args": ["mcp_server.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

Pour macOS / Linux / WSL, remplacez son contenu par celui de `.vscode/mcp.unix.json`.

## 9. Démarrer MCP dans VS Code

Dans VS Code :

```text
Ctrl + Shift + P
MCP: List Servers
paycoreDb
Start Server
```

Tester la resource :

```text
Ctrl + Shift + P
MCP: Browse Resources
paycoreDb
paycore://schema
```

## 10. Prompt de test dans le chat VS Code compatible MCP

```text
Utilise le serveur MCP paycoreDb.

Commence par consulter la resource paycore://schema.

Puis utilise l’outil query_incidents pour répondre à la question suivante :

Quels incidents de double débit sont encore ouverts ou en investigation ?

Contraintes :
- utilise uniquement une requête SELECT ;
- interroge uniquement la table incidents ;
- cite la requête SQL utilisée ;
- cite les données utilisées ;
- indique les limites ;
- ne propose aucune action client automatique.
```

Résultat attendu : deux incidents `double_debit` :
- `mobile_app`, `open`, `120.50` ;
- `ecommerce`, `investigating`, `89.90`.

## 11. Tester l'agent Gemini

```bash
python agent_demo.py
```

## 12. Tester l'orchestration multi-agents

```bash
python multi_agent_demo.py
```

## 13. Dépannage rapide

- Serveur MCP absent : vérifier `.vscode/mcp.json`.
- Erreur `No module named mcp` : relancer `pip install -r requirements.txt` et vérifier le chemin Python de `.venv`.
- Base absente : relancer `python setup_db.py`.
- Tool absent : `MCP: Reset Cached Tools` puis redémarrer le serveur.
- Logs : `MCP: List Servers` puis `Show Output`.

## 14. Ce que l'apprenant doit savoir dire

J'ai développé un serveur MCP custom connecté à une base SQLite. Je l'ai déclaré dans VS Code, puis j'ai utilisé une resource et un tool MCP. J'ai ensuite simulé un agent contrôlé capable de transformer une question en requête SQL, d'exécuter l'outil autorisé, d'observer le résultat et de répondre avec limites.
