# Directive de Génération IA - PayCore Group SecOps

## 1. Sécurité Applicative (Zero Trust)
- Interdiction stricte de concaténer des variables dans les requêtes SQL. Exiger l'usage de requêtes paramétrées.
- Révocation et masquage immédiat de tout secret (API Key, Token) identifié lors de l'analyse du code.
- **Validation et Assainissement des Entrées (Input Validation and Sanitization)** : Toutes les entrées provenant d'utilisateurs ou de sources externes doivent être validées et assainies de manière stricte avant toute utilisation.
- **Gestion des Erreurs Sécurisée (Secure Error Handling)** : Les messages d'erreur exposés aux utilisateurs finaux ne doivent jamais contenir d'informations sensibles (traces de pile, détails techniques d'implémentation, données de base de données, etc.).
- **Principe du Moindre Privilège (Least Privilege)** : Le code généré et les configurations associées doivent toujours fonctionner avec le minimum de privilèges nécessaires pour accomplir leur tâche.
- **Analyse de Sécurité des Dépendances (Dependency Security Scanning)** : Chaque nouvelle dépendance suggérée ou ajoutée doit être vérifiée pour des vulnérabilités connues (CVE).

## 2. Standards de Qualité
- Application du principe de responsabilité unique (découplage des fonctions monolithiques).
- Implémentation systématique du typage explicite (Type Hints).
- Documentation des signatures de fonctions via Docstrings standardisées.
- **Immutabilité des Données (Data Immutability)** : Favoriser l'utilisation de structures de données immuables ou rendre les objets immuables lorsque cela est pertinent pour éviter les effets de bord inattendus.
- **Gestion de la Concurrence et Asynchronisme (Concurrency & Asynchrony Management)** : Pour les opérations I/O-bound (ex: appels réseau, attente de réponse), privilégier les approches asynchrones (`asyncio` en Python) pour améliorer la réactivité et la scalabilité.
- **Documentation des Décisions Architecturales (Architectural Decision Records - ADRs)** : Pour les choix architecturaux significatifs ou les compromis importants, l'IA doit générer une brève explication justifiant la décision.
- **Configuration Centralisée et Typée (Typed Configuration)** : Les configurations doivent être gérées via des mécanismes standardisés et typés (ex: classes `dataclasses` ou `Pydantic Settings` pour Python), plutôt que des chaînes de caractères brutes.

## 3. Couverture de Tests
- Chaque refactoring doit inclure les tests unitaires associés (framework pytest).
- Couverture obligatoire des cas aux limites (Boundary conditions, types inattendus).
- **Mocking des Dépendances Externes (Mocking External Dependencies)** : Les tests unitaires doivent isoler le code testé en "mockant" (simulant) toutes les dépendances externes (DB, API externes, système de fichiers).
- **Tests Négatifs et Gestion des Exceptions (Negative Testing & Exception Handling)** : En plus des cas de succès, les tests doivent explicitement vérifier les comportements attendus en cas d'échec (ex: fonds insuffisants, données invalides, erreurs d'API) et que les exceptions sont correctement gérées.

## 4. Spécificités Python
- **Conformité PEP 8 (PEP 8 Compliance)** : Tout le code Python généré doit adhérer strictement aux conventions de style de la PEP 8.
- **Gestion des Ressources avec `with` (Context Managers)** : Utiliser systématiquement les gestionnaires de contexte (`with` statement) pour toutes les opérations impliquant des ressources qui doivent être fermées (fichiers, connexions DB, locks, etc.).
