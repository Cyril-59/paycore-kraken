from db_tools import get_schema_text, run_readonly_query

print("=== SCHÉMA ===")
print(get_schema_text())

print("\n=== REQUÊTE AUTORISÉE ===")
print(run_readonly_query("""
SELECT id, incident_type, channel, amount, status, created_at
FROM incidents
WHERE incident_type = 'double_debit'
AND status IN ('open', 'investigating')
"""))

print("\n=== REQUÊTE INTERDITE ===")
print(run_readonly_query("DELETE FROM incidents"))
