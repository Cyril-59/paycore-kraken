import json
from mcp.server.fastmcp import FastMCP
from db_tools import get_schema_text, run_readonly_query

mcp = FastMCP("paycore-db")


@mcp.resource("paycore://schema")
def get_schema() -> str:
    """Expose le schéma de la base PayCore."""
    return get_schema_text()


@mcp.tool()
def query_incidents(query: str) -> str:
    """Exécute une requête SELECT read-only sur la table incidents."""
    result = run_readonly_query(query)
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
