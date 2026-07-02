import sqlite3

class AccountRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                user_id TEXT PRIMARY KEY,
                balance REAL
            )
        """
        )
        conn.commit()
        conn.close()

    def get_balance(self, user_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def update_balance(self, user_id, new_balance):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = ? WHERE user_id = ?", (new_balance, user_id))
        conn.commit()
        conn.close()

    def create_account_if_not_exists(self, user_id, initial_balance=0.0):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO accounts (user_id, balance) VALUES (?, ?)", (user_id, initial_balance))
        conn.commit()
        conn.close()
