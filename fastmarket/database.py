import sqlite3

class Database:
    def __init__(self, db_name='fastmarket/dados/aula.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL)''')
        self.conn.commit()
    
    def add_user(self, username, email, password):
        self.cursor.execute("INSERT INTO users(username, email, password) VALUES (?, ?, ?)",
                            (username, email, password))
        self.conn.commit()
        
    def get_user(self, username, password):
        self.cursor.execute("SELECT id, username, email FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2]
            }
        return None
    
    def close(self):
        self.conn.close()
