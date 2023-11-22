import sqlite3

CriarTabelaClientes = """ CREATE TABLE IF NOT EXISTS Clientes (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        nome text NOT NULL,
                        telefone text,
                        endereco text
                        ); """

CriarTabelaItem = """ CREATE TABLE IF NOT EXISTS Itens (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        tipo text NOT NULL,
                        marca text,
                        defeito text,
                        data_chegada DATE,
                        data_entrega DATE,
                        finalizado INTEGER,
                        cliente_id INTEGER,
                        FOREIGN KEY (cliente_id) REFERENCES Clientes(id)
                        ); """


CriarTabelaServico = """ CREATE TABLE IF NOT EXISTS Servicos (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        descricao text,
                        valor REAL,
                        item_id INTEGER,
                        FOREIGN KEY (item_id) REFERENCES Itens(id)
                        ); """

conexao = sqlite3.connect('database.db')
cursor = conexao.cursor()
cursor.execute(CriarTabelaClientes)
cursor.execute(CriarTabelaServico)
cursor.execute(CriarTabelaItem)