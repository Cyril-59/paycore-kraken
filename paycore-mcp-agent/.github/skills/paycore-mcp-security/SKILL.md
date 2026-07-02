---
name: paycore-mcp-security
description: 'Appliquer les règles de sécurité du projet PayCore MCP. Utiliser cette skill pour revoir db_tools.py, mcp_server.py, agent_demo.py ou tout prompt qui génère des requêtes SQL. Vérifie : pas de clés API en dur, read-only strict, scope à incidents, LIMIT 10, données fictives uniquement.'
argument-hint: 'Fichier à revoir (optionnel)'
---

# Sécurité PayCore MCP

## Quand utiliser cette skill

- ✅ Revoir du code qui génère ou exécute des requêtes SQL
- ✅ Vérifier des prompts qui demandent à générer du SQL
- ✅ Auditer les fichiers critiques : `db_tools.py`, `mcp_server.py`, `agent_demo.py`
- ✅ Valider une nouvelle intégration API ou LLM
- ✅ S'assurer qu'il n'y a pas de clés API en dur

## Principes de sécurité du projet

| Catégorie | Règle | Vérification |
|-----------|-------|-------------|
| **Données** | Uniquement fictives | Pas d'exemplaires client réels |
| **API** | Variables d'environnement uniquement | `os.getenv("GEMINI_API_KEY")` |
| **SQL** | Read-only strict | `SELECT` uniquement, pas de `UPDATE`, `DELETE`, `DROP` |
| **Scope** | Table `incidents` uniquement | Rejet si table hors scope |
| **Limites** | `LIMIT 10` par défaut | Toujours ajouter si absent |

## Procédure de vérification

### 1. Clés API et secrets

**À vérifier :**
```python
# ✅ BON
api_key = os.getenv("GEMINI_API_KEY")

# ❌ MAUVAIS
api_key = "sk-1234567890abcdef"
```

**Commande rapide :**
```bash
grep -r "GEMINI_API_KEY\|sk-\|api_key\s*=\s*['\"]" *.py
```

### 2. Validation read-only

**À vérifier dans `db_tools.validate_readonly_query()` :**
- [ ] Début par `SELECT` requis
- [ ] Mots-clés interdits : `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `PRAGMA`
- [ ] Une seule requête (pas de `;` multiple)
- [ ] Scope limité à `FROM incidents`

**Exemple de fonction correcte :**
```python
def validate_readonly_query(query: str) -> tuple[bool, str]:
    query_clean = query.lower().replace('\n', '').strip()
    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "pragma"]
    
    if not query_clean.startswith("select"):
        return False, "Erreur : seules les requêtes SELECT sont autorisées."
    
    if any(re.search(rf"\b{word}\b", query_clean) for word in forbidden):
        return False, "Erreur : requête interdite."
    
    if "from incidents" not in query_clean:
        return False, "Erreur : seule la table incidents est autorisée."
    
    return True, query
```

### 3. LIMIT 10 par défaut

**À vérifier dans `db_tools.run_readonly_query()` :**
```python
if "limit" not in query.lower():
    query = query.rstrip(";") + " LIMIT 10;"
```

### 4. Données fictives

**À vérifier :**
- [ ] Aucun numéro client réel (9999-XXXX format)
- [ ] Aucun IBAN/SWIFT en dur
- [ ] Aucune adresse email de production
- [ ] Tous les exemples sont clairement fictifs
- [ ] Commentaires `# fictif`, `# exemple`, `# démo`

**Grep pour détecter des patterns dangereux :**
```bash
grep -Er "([0-9]{4}-[0-9]{4}|@paycore\.com|prod.*database)" *.py
```

### 5. Prompts et instructions LLM

**À vérifier :**
- [ ] N'ordonne jamais `UPDATE`, `DELETE`, `DROP`
- [ ] Dit explicitement "seule la table `incidents`"
- [ ] Rappelle le `LIMIT 10` pour les listes
- [ ] Pas d'injection de contexte sensible

**Texte de référence sûr :**
```
Tu dois répondre en utilisant uniquement la table incidents.
Propose une requête SELECT avec LIMIT 10 si nécessaire.
N'utilise aucune autre table.
```

## Checklist de validation

Avant de valider un changement, parcourir :

- [ ] **db_tools.py** : validations read-only et LIMIT intact
- [ ] **mcp_server.py** : aucune clé API en dur
- [ ] **agent_demo.py** : `os.getenv()` pour GEMINI_API_KEY
- [ ] **Nouveaux prompts** : pas d'ordres `UPDATE/DELETE/DROP`
- [ ] **Données d'exemple** : fictives et clairement marquées
- [ ] **Scope SQL** : limité à `incidents` uniquement

## Ressources

- Voir [copilot-instructions.md](../../copilot-instructions.md) pour les règles complètes
- Voir [db_tools.py](../../../db_tools.py) pour la validation de référence
- Voir [agent_demo.py](../../../agent_demo.py) pour les patterns LLM sûrs
