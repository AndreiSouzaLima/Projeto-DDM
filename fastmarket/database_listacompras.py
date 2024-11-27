import sqlite3

class Database_lista:
    def __init__(self, db_name='fastmarket/dados/lista_compras.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS listas_compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            nome TEXT NOT NULL,
            data_criacao TEXT NOT NULL,
            ultima_compra TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS compras_totais (
            user_id INTEGER PRIMARY KEY,
            total_compras INTEGER DEFAULT 0
        )''')

        self.conn.commit()

    def criar_lista(self, user_id, nome, data_criacao):
        self.cursor.execute(
            "INSERT INTO listas_compras (user_id, nome, data_criacao) VALUES (?, ?, ?)",
            (user_id, nome, data_criacao)
        )
        self.conn.commit()

    def get_listas_by_user(self, user_id):
        self.cursor.execute("SELECT * FROM listas_compras WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def deletar_lista(self, id_lista):
        self.cursor.execute("DELETE FROM listas_compras WHERE id = ?", (id_lista,))
        self.conn.commit()

    def carregar_total_compras(self, user_id):
        self.cursor.execute("SELECT total_compras FROM compras_totais WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0  

    def atualizar_total_compras(self, user_id, total_compras):
        self.cursor.execute('''INSERT INTO compras_totais (user_id, total_compras)
                               VALUES (?, ?)
                               ON CONFLICT(user_id) 
                               DO UPDATE SET total_compras = ?''',
                            (user_id, total_compras, total_compras))
        self.conn.commit()

    def close(self):
        self.conn.close()
