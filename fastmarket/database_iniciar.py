import sqlite3

class DatabaseIniciar:
    def __init__(self):
        self.conn = sqlite3.connect("fastmarket/dados/shopping_list.db")
        self.create_table()

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS itens_lista (
                            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_lista INTEGER NOT NULL,
                            nome TEXT NOT NULL,
                            marca TEXT,
                            unidade REAL,
                            preco_unitario REAL,
                            valor_total REAL,
                            FOREIGN KEY (id_lista) REFERENCES listas_compras(id_lista)
                        );''')

    def adicionar_item(self, id_lista, nome, marca, unidade, preco_unitario):
        valor_total = unidade * preco_unitario if unidade and preco_unitario else 0
        self.conn.execute("INSERT INTO itens_lista (id_lista, nome, marca, unidade, preco_unitario, valor_total) VALUES (?, ?, ?, ?, ?, ?)",
                          (id_lista, nome, marca, unidade, preco_unitario, valor_total))
        self.conn.commit()

    def get_itens_by_lista(self, id_lista):
        cursor = self.conn.execute("SELECT * FROM itens_lista WHERE id_lista = ?", (id_lista,))
        return cursor.fetchall()

    def remover_item(self, id_item):
        self.conn.execute("DELETE FROM itens_lista WHERE id_item = ?", (id_item,))
        self.conn.commit()

    def update_item(self, id_item, nome, marca, unidade, preco_unitario):
        valor_total = unidade * preco_unitario if unidade and preco_unitario else 0
        self.conn.execute("UPDATE itens_lista SET nome = ?, marca = ?, unidade = ?, preco_unitario = ?, valor_total = ? WHERE id_item = ?",
                          (nome, marca, unidade, preco_unitario, valor_total, id_item))
        self.conn.commit()
