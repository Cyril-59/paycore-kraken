# ==============================================================================
# SCRIPT DE PROVISIONNEMENT : OPÉRATION KRAKEN (PAYCORE GROUP)
# Description : Génération automatisée de l'espace de travail pour la formation.
# ==============================================================================

# Phase 1 : Initialisation de l'arborescence du projet (Structure racine)
# Crée les répertoires nécessaires pour l'infrastructure, le code source, 
# la gouvernance et les modules Node.js de manière silencieuse.
mkdir -p .devcontainer .vscode src rules docs logs rag-lab mcp-server/src

# Phase 2 : Déploiement de l'Infrastructure-as-Code (IaC) et configuration IDE
# Force la désactivation de la télémétrie locale et pré-installe les extensions
# requises pour garantir un environnement iso-production entre tous les apprenants.
cat << 'EOF' > .devcontainer/devcontainer.json
{
  "name": "KRAKEN Lab - Environnement Complet",
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "customizations": {
    "vscode": {
      "settings": {
        "telemetry.telemetryLevel": "off",
        "python.testing.pytestEnabled": true
      },
      "extensions": [
        "Continue.continue",
        "ms-python.python",
        "ms-vscode.vscode-typescript-next"
      ]
    }
  },
  "postCreateCommand": "pip install pytest && cd rag-lab && npm install && cd ../mcp-server && npm install",
  "forwardPorts": [3000]
}
EOF

cat << 'EOF' > .vscode/settings.json
{
  "telemetry.telemetryLevel": "off",
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true
}
EOF

# Phase 3 : Injection du code legacy (Cibles d'audit SecOps et Refactoring)
# Ces modules contiennent des vulnérabilités volontaires (OWASP) et une dette 
# technique sévère pour les travaux pratiques du Jour 1.
cat << 'EOF' > src/payment_gateway.py
import sqlite3
import time
import logging

# [VULNÉRABILITÉ CRITIQUE] Secret d'authentification exposé dans le code source
STRIPE_API_KEY_PROD = "sk_live_51MabcDExYz123456789SecretKeyKRAKEN"

def process_payment(user_id, amount, card_number):
    """
    Traite un paiement entrant. 
    [DÉFAUT D'ARCHITECTURE] Violation du principe de responsabilité unique (SOLID).
    """
    print(f"Initialisation du paiement de {amount} pour l'utilisateur {user_id}")
    time.sleep(1) # Simulation de la latence du fournisseur de paiement
    
    # [VULNÉRABILITÉ CRITIQUE] Injection SQL (CWE-89) via concaténation non assainie
    conn = sqlite3.connect('paycore_prod.db')
    cursor = conn.cursor()
    
    query = "SELECT balance FROM accounts WHERE user_id = '" + str(user_id) + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if not result:
        print("Erreur : Compte introuvable")
        return False
        
    balance = result[0]
    
    if balance >= amount:
        new_balance = balance - amount
        update_query = "UPDATE accounts SET balance = " + str(new_balance) + " WHERE user_id = '" + str(user_id) + "'"
        cursor.execute(update_query)
        conn.commit()
        
        # [VULNÉRABILITÉ CRITIQUE] Fuite de données personnelles (PII/PCI-DSS) dans les logs
        logging.error(f"SUCCES: Carte {card_number} debitee de {amount}")
        return True
    else:
        print("Erreur : Fonds insuffisants")
        return False
EOF

cat << 'EOF' > src/fraud_scoring.py
def calculate_fraud_score(amount: float, is_international: bool, failed_attempts: int) -> float:
    """
    Calcule un score de fraude entre 0.0 (Légitime) et 1.0 (Fraude avérée).
    """
    score = 0.0
    
    if amount > 10000:
        score += 0.4
    elif amount > 1000:
        score += 0.2
        
    if is_international:
        score += 0.3
        
    if failed_attempts >= 3:
        score += 0.5
        
    # [DÉFAUT LOGIQUE] Absence de normalisation. Le score peut excéder le plafond de 1.0.
    # Les tests unitaires générés devront isoler ce cas aux limites.
    return score
EOF

# Phase 4 : Mise en place du référentiel de gouvernance IA et documentation
# Fichiers utilisés pour forcer le comportement du LLM via le contexte système (Prompting).
cat << 'EOF' > rules/ai_assistant_rules.md
# Directive de Génération IA - PayCore Group SecOps

## 1. Sécurité Applicative (Zero Trust)
- Interdiction stricte de concaténer des variables dans les requêtes SQL. Exiger l'usage de requêtes paramétrées.
- Révocation et masquage immédiat de tout secret (API Key, Token) identifié lors de l'analyse du code.

## 2. Standards de Qualité
- Application du principe de responsabilité unique (découplage des fonctions monolithiques).
- Implémentation systématique du typage explicite (Type Hints).
- Documentation des signatures de fonctions via Docstrings standardisées.

## 3. Couverture de Tests
- Chaque refactoring doit inclure les tests unitaires associés (framework pytest).
- Couverture obligatoire des cas aux limites (Boundary conditions, types inattendus).
EOF

cat << 'EOF' > docs/api_payment.md
# Spécification API Payment - PayCore v2

## Endpoint : `/charge`
Interface de facturation sécurisée.

### Contrat de données (Payload) :
- `amount` (float) : Montant strictement positif.
- `currency` (str) : Devise au standard ISO 4217 (ex: "EUR").
- `source_token` (str) : Jeton de tokenisation (PCI-DSS compliant).

### Matrice des codes de retour :
- `400` : Bad Request (Validation du payload échouée).
- `402` : Payment Required (Provision insuffisante).
- `403` : Forbidden (Rejet par le moteur de scoring de fraude).
EOF

cat << 'EOF' > logs/observations.csv
Test_Realise;Prompt_Utilise;Latence_Sec;Risque_Securite_Detecte;Correction_Humaine_Requise;Enseignement
1_Prompt_Vague;"Améliore ce code payment_gateway.py";;;;
2_Prompt_Structure;"Refactorise avec @ai_assistant_rules.md";;;;
3_Gen_Tests;"Génère les tests pour fraud_scoring.py";;;;
EOF

# Phase 5 : Provisionnement de l'infrastructure TypeScript (Jour 2)
# Préparation des modules RAG (Retrieval-Augmented Generation) et Serveur MCP.
cat << 'EOF' > rag-lab/package.json
{
  "name": "paycore-mini-rag",
  "version": "1.0.0",
  "description": "Implémentation d'un moteur RAG minimaliste en TypeScript",
  "main": "index.ts",
  "scripts": {
    "start": "ts-node index.ts"
  },
  "dependencies": {
    "ts-node": "^10.9.2",
    "typescript": "^5.3.3"
  }
}
EOF

cat << 'EOF' > rag-lab/index.ts
// Modèle de données pour l'indexation sémantique simulée
interface DocumentChunk {
    id: number;
    text: string;
    keywords: string[];
}

const KNOWLEDGE_BASE: DocumentChunk[] = [
    { id: 1, text: "L'endpoint /charge nécessite un amount positif et une devise ISO.", keywords: ["charge", "endpoint", "amount", "devise"] },
    { id: 2, text: "Le code d'erreur 402 indique des fonds insuffisants sur la carte du client.", keywords: ["402", "erreur", "fonds", "carte"] },
    { id: 3, text: "Le score de fraude déclenche une erreur 403 Forbidden si le score dépasse 0.8.", keywords: ["fraude", "403", "forbidden", "score"] }
];

// Moteur d'extraction de contexte (Simulation d'une base vectorielle)
function retrieveContext(query: string): string {
    const queryWords = query.toLowerCase().split(' ');
    const results = KNOWLEDGE_BASE.filter(chunk => 
        chunk.keywords.some(keyword => queryWords.includes(keyword))
    );
    
    if (results.length === 0) return "Aucun contexte pertinent trouvé.";
    return results.map(r => `[Doc ${r.id}]: ${r.text}`).join("\n");
}

const userQuery = "Pourquoi mon utilisateur reçoit une erreur 402 lors du traitement ?";
console.log(`[SYSTEM] Requête entrante : "${userQuery}"\n`);

const context = retrieveContext(userQuery);
console.log(`[SYSTEM] Contexte extrait par le RAG :\n${context}\n`);

const finalPromptForLLM = `
Tu es l'assistant technique de PayCore. Utilise le contexte suivant pour répondre à la question.
CONTEXTE :
${context}

QUESTION : ${userQuery}
REPONSE :`;

console.log(`[SYSTEM] Payload final formaté pour l'API LLM :\n${finalPromptForLLM}`);
EOF

cat << 'EOF' > mcp-server/package.json
{
  "name": "paycore-mcp-server",
  "version": "1.0.0",
  "description": "Serveur Model Context Protocol (MCP) pour l'accès aux bases de données",
  "main": "build/index.js",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node build/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.1",
    "zod": "^3.22.4"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "typescript": "^5.3.3"
  }
}
EOF

cat << 'EOF' > mcp-server/tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"]
}
EOF

cat << 'EOF' > mcp-server/src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

// Initialisation de l'instance serveur MCP
const server = new Server(
  { name: "paycore-database-auditor", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Simulation de la base de données de production en mémoire
const MOCK_ACCOUNTS = [
  { user_id: "usr_101", balance: 5000, status: "active" },
  { user_id: "usr_102", balance: 12, status: "suspended" },
  { user_id: "usr_103", balance: 85000, status: "active" }
];

// Définition des capacités exposées au LLM (Découverte des outils)
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_account_balance",
        description: "Interroge la base de données PayCore pour extraire le solde et le statut d'un compte client.",
        inputSchema: {
          type: "object",
          properties: {
            userId: { type: "string", description: "L'identifiant unique du client (ex: usr_101)" }
          },
          required: ["userId"]
        }
      }
    ]
  };
});

// Logique d'exécution métier lors de l'invocation de l'outil par le LLM
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_account_balance") {
    const args = request.params.arguments as { userId: string };
    const account = MOCK_ACCOUNTS.find(acc => acc.user_id === args.userId);
    
    if (!account) {
      return {
        content: [{ type: "text", text: `Erreur système : Entité introuvable pour l'identifiant ${args.userId}.` }],
        isError: true
      };
    }
    
    return {
      content: [{ 
        type: "text", 
        text: `Accès base de données validé. Solde : ${account.balance} EUR. Statut : ${account.status}.` 
      }]
    };
  }
  
  throw new Error("Outil non reconnu par le registre MCP.");
});

// Amorçage du protocole de transport Standard I/O
async function run() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("[SYSTEM] Serveur MCP PayCore initialisé et en écoute sur STDIO.");
}

run().catch((error) => {
  console.error("[ERREUR FATALE] Échec du démarrage du serveur MCP:", error);
  process.exit(1);
});
EOF

echo "[SYSTEM] Provisionnement de l'espace de travail PayCore Kraken achevé avec succès. Prêt pour exécution."