import os
from google import genai
from db_tools import get_schema_text, run_readonly_query, clean_sql, validate_readonly_query

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY est manquante.")

client = genai.Client(api_key=api_key)


def planner_agent(question: str) -> str:
    schema = get_schema_text()

    prompt = f"""
Tu es l'agent Planner.

Tu dois transformer la question en une requête SQL SELECT sur la table incidents.

SCHÉMA :
{schema}

QUESTION :
{question}

Réponds uniquement avec la requête SQL.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return clean_sql(response.text)


def safety_agent(sql: str) -> tuple[bool, str]:
    is_valid, message = validate_readonly_query(sql)

    if not is_valid:
        return False, message

    return True, sql


def executor_agent(sql: str) -> dict:
    return run_readonly_query(sql)


def analyst_agent(question: str, sql: str, observation: dict) -> str:
    prompt = f"""
Tu es l'agent Analyste.

QUESTION :
{question}

SQL :
{sql}

OBSERVATION :
{observation}

Produis une réponse structurée :

Réponse :
Données utilisées :
Limites :
Validation humaine nécessaire :
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text


def run_multi_agent_flow(question: str) -> str:
    print("\n=== AGENT PLANNER ===")
    sql = planner_agent(question)
    print(sql)

    print("\n=== AGENT SÉCURITÉ ===")
    is_safe, safety_message = safety_agent(sql)
    print(safety_message)

    if not is_safe:
        return f"Flux arrêté par l'agent sécurité : {safety_message}"

    print("\n=== AGENT EXECUTOR ===")
    observation = executor_agent(sql)
    print(observation)

    print("\n=== AGENT ANALYSTE ===")
    return analyst_agent(question, sql, observation)


if __name__ == "__main__":
    question = "Quels canaux concentrent les incidents ouverts ?"
    answer = run_multi_agent_flow(question)

    print("\n=== RÉPONSE FINALE ===")
    print(answer)
