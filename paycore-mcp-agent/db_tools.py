import re
import sqlite3
from typing import Any

DB_PATH = "paycore_demo.db"


def get_schema_text() -> str:
    return """
Table: incidents

Colonnes:
- id INTEGER
- incident_type TEXT
- channel TEXT
- amount REAL
- status TEXT
- created_at TEXT

Usage:
Table fictive des incidents de paiement PayCore.

status possible values :
- open
- investigating
- closed

incident_type possible values :
- double_debit
- refund_delay
- suspected_fraud
"""


def clean_sql(sql: str) -> str:
    """Nettoie les balises Markdown parfois générées par un LLM."""
    sql = sql.strip()
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    return sql.strip()


def validate_readonly_query(query: str) -> tuple[bool, str]:
    """Valide une requête pédagogique read-only limitée à la table incidents."""
    query = clean_sql(query)
    query_clean = query.lower().replace('\n', '').strip()

    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "pragma"]

    if not query_clean.startswith("select"):
        return False, "Erreur : seules les requêtes SELECT sont autorisées."

    if ";" in query_clean.rstrip(";"):
        return False, "Erreur : une seule requête SQL est autorisée."

    if any(re.search(rf"\b{word}\b", query_clean) for word in forbidden):
        return False, "Erreur : requête interdite."

    if "from incidents" not in query_clean:
        return False, "Erreur : seule la table incidents est autorisée."

    return True, query


def run_readonly_query(query: str) -> dict[str, Any]:
    """Exécute une requête SELECT limitée, retourne colonnes + lignes."""
    is_valid, result = validate_readonly_query(query)

    if not is_valid:
        return {
            "ok": False,
            "error": result,
            "columns": [],
            "rows": [],
        }

    query = result

    if "limit" not in query.lower():
        query = query.rstrip(";") + " LIMIT 10;"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        return {
            "ok": True,
            "query": query,
            "columns": columns,
            "rows": rows,
        }

    except Exception as error:
        return {
            "ok": False,
            "error": str(error),
            "columns": [],
            "rows": [],
        }

    finally:
        conn.close()
