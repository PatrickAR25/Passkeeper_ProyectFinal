import sqlite3


class LoginManager:
    def __init__(self, db_path='passkeeper.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_user_table()

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def register_user(self, username, password):
        """Registra un nuevo usuario."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # El usuario ya existe

    def authenticate_user(self, username, password):
        """Autentica un usuario existente."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone() is not None
