# Instructions PayCore MCP

Serveur MCP pédagogique connecté à une base SQLite fictive pour démonstration.

## Sécurité et Données

- **Uniquement données fictives** : Tous les exemplaires et données doivent être fictifs
- **Jamais de données réelles** : Ne jamais proposer ou suggérer des données client en production
- **Pas de clés API en dur** : Interdiction absolue d'écrire les clés API dans le code
- **Variables d'environnement** : Utiliser `GEMINI_API_KEY` pour toute intégration API

## Requêtes SQL — Contraintes Read-Only

- **Préserver la logique read-only** : Aucune opération d'écriture n'est autorisée
- **Opérations interdites** : Jamais proposer `UPDATE`, `DELETE`, `DROP`, `ALTER` ou `CREATE` dans les requêtes générées
- **Scope limité** : Toutes les requêtes SQL se limitent à la table `incidents`
- **Limitation des résultats** : Ajouter `LIMIT 10` lorsque la requête peut retourner plusieurs lignes
- **Transparence** : Toujours afficher les limites de la réponse (ex: "Résultats limités à 10 lignes")

## Validation et Gouvernance

- **Validation humaine** : Toute action métier sensible doit rester soumise à validation humaine
- **Pas d'auto-exécution** : Ne jamais exécuter automatiquement les mutations ou changements d'état critiques

## Style de Réponse

Répondre selon le modèle structuré suivant :

1. **Diagnostic court** : Résumé rapide du contexte/problème
2. **Proposition structurée** : Solution claire et organisée
3. **Code minimal si nécessaire** : Exemples de code focalisés et complets
4. **Tests à lancer** : Commandes ou étapes pour valider la solution
5. **Risques résiduels** : Limitations connues ou points d'attention

## Exemples de Requêtes Valides

```sql
-- ✅ Bon : select read-only avec LIMIT
SELECT * FROM incidents WHERE status = 'open' LIMIT 10;

-- ❌ Mauvais : update
UPDATE incidents SET status = 'closed' WHERE id = 1;

-- ❌ Mauvais : table hors scope
SELECT * FROM users;
```
