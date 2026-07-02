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
