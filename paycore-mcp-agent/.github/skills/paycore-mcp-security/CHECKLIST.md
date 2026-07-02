# Checklist Rapide — Sécurité PayCore MCP

Avant de pusher, vérifier :

## 🔐 Clés API
- [ ] Aucune clé API en dur
- [ ] `os.getenv("GEMINI_API_KEY")` utilisé
- [ ] Levée d'erreur si variable manquante

## 🛡️ Requêtes SQL
- [ ] Validation `SELECT` uniquement
- [ ] Mots-clés interdits détectés
- [ ] Scope limité à `FROM incidents`
- [ ] `LIMIT 10` ajouté par défaut

## 📊 Données
- [ ] Aucun numéro client réel
- [ ] Aucun IBAN/email de prod
- [ ] Exemples marqués `# fictif`

## 🤖 Prompts LLM
- [ ] Pas d'ordres `UPDATE/DELETE`
- [ ] Rappel `incidents` uniquement
- [ ] Validation humaine mentionnée

## ▶️ Test Automatique
```bash
python .github/skills/paycore-mcp-security/scripts/check_security.py
```

---

**Qui réviser :**
- `db_tools.py` → Validation SQL
- `mcp_server.py` → Outils MCP
- `agent_demo.py` → Prompts LLM
- Nouveaux fichiers `*.py`
