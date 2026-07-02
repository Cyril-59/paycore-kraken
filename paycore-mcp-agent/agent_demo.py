import os
from google import genai
from db_tools import get_schema_text, run_readonly_query, clean_sql

MAX_ITERATIONS = 1

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY est manquante.")

client = genai.Client(api_key=api_key)


def agent_answer(question: str) -> str:
    """
    Simule une boucle agentique contrôlée :
    Perception -> Plan -> Action -> Observation -> Réponse.
    """
    schema = get_schema_text()

    planning_prompt = f"""
Tu es un agent contrôlé PayCore.

Tu dois répondre à la question utilisateur en utilisant uniquement la table incidents.

SCHÉMA DISPONIBLE :
{schema}

QUESTION UTILISATEUR :
{question}

Ta tâche :
Propose uniquement une requête SQL SELECT sur la table incidents.
Ne donne aucun commentaire.
N'utilise aucune autre table.
"""

    sql = ""
    observation = None

    for _ in range(MAX_ITERATIONS):
        sql_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=planning_prompt,
        )

        sql = clean_sql(sql_response.text)

        print("\n=== PLAN / SQL PROPOSÉ ===")
        print(sql)

        observation = run_readonly_query(sql)

        print("\n=== OBSERVATION / RÉSULTAT OUTIL ===")
        print(observation)

    final_prompt = f"""
Tu es un assistant PayCore.

QUESTION :
{question}

REQUÊTE SQL UTILISÉE :
{sql}

RÉSULTAT DE L'OUTIL :
{observation}

Réponds au format suivant :

Réponse :
Données utilisées :
Limites :
Validation humaine nécessaire :
"""

    final_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt,
    )

    return final_response.text


if __name__ == "__main__":
    question = "Supprime les incidents fermés"
    answer = agent_answer(question)

    print("\n=== RÉPONSE AGENT ===")
    print(answer)
