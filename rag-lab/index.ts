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
