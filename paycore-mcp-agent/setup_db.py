import sqlite3

DB_PATH = "paycore_demo.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS incidents")

cursor.execute("""
CREATE TABLE incidents (
    id INTEGER PRIMARY KEY,
    incident_type TEXT,
    channel TEXT,
    amount REAL,
    status TEXT,
    created_at TEXT
)
""")

cursor.executemany("""
INSERT INTO incidents (incident_type, channel, amount, status, created_at)
VALUES (?, ?, ?, ?, ?)
""", [
    ("double_debit", "mobile_app", 120.50, "open", "2026-06-01"),
    ("double_debit", "ecommerce", 89.90, "investigating", "2026-06-02"),
    ("refund_delay", "pos_terminal", 45.00, "closed", "2026-06-03"),
    ("suspected_fraud", "api_partner", 999.00, "open", "2026-06-04"),
])

conn.commit()
conn.close()

print("Base paycore_demo.db créée avec succès.")
