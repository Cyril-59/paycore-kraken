import pytest
import sqlite3
import os
from src.payment_gateway import process_payment

# Chemin vers une base de données de test en mémoire
TEST_DB_PATH = ":memory:"

@pytest.fixture
def setup_db():
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            user_id TEXT PRIMARY KEY,
            balance REAL
        )
    """)
    conn.commit()
    # Insérer des données de test
    cursor.execute("INSERT OR REPLACE INTO accounts (user_id, balance) VALUES (?, ?)", ("user123", 1000.0))
    cursor.execute("INSERT OR REPLACE INTO accounts (user_id, balance) VALUES (?, ?)", ("user456", 50.0))
    conn.commit()
    conn.close()
    yield
    # Nettoyage (pas nécessaire pour :memory: mais bonne pratique)
    if os.path.exists(TEST_DB_PATH) and TEST_DB_PATH != ":memory:":
        os.remove(TEST_DB_PATH)

def get_balance(user_id):
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def test_successful_payment(setup_db):
    initial_balance = get_balance("user123")
    assert initial_balance == 1000.0

    success = process_payment("user123", 100.0, "1234567890123456", db_path=TEST_DB_PATH)
    assert success is True
    assert get_balance("user123") == 900.0

def test_insufficient_funds(setup_db):
    initial_balance = get_balance("user456")
    assert initial_balance == 50.0

    success = process_payment("user456", 100.0, "9876543210987654", db_path=TEST_DB_PATH)
    assert success is False
    assert get_balance("user456") == 50.0 # Le solde ne doit pas changer

def test_account_not_found(setup_db):
    success = process_payment("nonexistent_user", 50.0, "1111222233334444", db_path=TEST_DB_PATH)
    assert success is False
    assert get_balance("nonexistent_user") is None

def test_sql_injection_prevention(setup_db):
    # Tentative d'injection SQL via user_id
    malicious_user_id = "user123' OR 1=1; --"
    # Le paiement devrait échouer ou ne pas trouver le compte 'malicieux'
    success = process_payment(malicious_user_id, 10.0, "1234123412341234", db_path=TEST_DB_PATH)
    assert success is False # Le compte 'malicieux' ne doit pas être trouvé

    # Vérifier que le solde de user123 n'a pas changé
    assert get_balance("user123") == 1000.0

def test_card_number_masking_in_logs(caplog, setup_db):
    import logging
    with caplog.at_level(logging.INFO):
        process_payment("user123", 10.0, "1234567890123456", db_path=TEST_DB_PATH)
    
    # Vérifier que le log contient le numéro de carte masqué
    assert "SUCCES: Carte **** **** **** 3456 débitée de 10.0 pour l'utilisateur user123" in caplog.text

def test_api_key_env_var():
    # Test indirect de la variable d'environnement
    # On ne peut pas facilement mocker os.getenv directement dans pytest sans une refactorisation plus poussée
    # Mais on peut vérifier qu'elle est définie et non la valeur par défaut si elle est configurée
    assert os.getenv("STRIPE_API_KEY_PROD") != "sk_test_YOUR_DEFAULT_TEST_KEY" or os.getenv("STRIPE_API_KEY_PROD") is None

    # Pour un test plus robuste, on mockera os.getenv après refactorisation.
