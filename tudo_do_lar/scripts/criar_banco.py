import sqlite3

CriarTabelaClientes = """ CREATE TABLE IF NOT EXISTS Clientes (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        nome text NOT NULL,
                        telefone text,
                        endereco text
                        ); """


CriarTabelaServico = """ CREATE TABLE IF NOT EXISTS Servico (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        descricao text,
                        total REAL,
                        finalizado bool,
                        cliente_id INTEGER,
                        FOREIGN KEY (cliente_id) REFERENCES Clientes(id)
                        ); """

CriarTabelaItem = """ CREATE TABLE IF NOT EXISTS Item (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        tipo text NOT NULL,
                        marca text,
                        conserto text,
                        valor REAL,
                        servico_id INTEGER,
                        FOREIGN KEY (servico_id) REFERENCES Servico(id)
                        ); """

conexao = sqlite3.connect('database.db')
cursor = conexao.cursor()
cursor.execute(CriarTabelaClientes)
cursor.execute(CriarTabelaServico)
cursor.execute(CriarTabelaItem)