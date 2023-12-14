import sqlite3

# Modelo com cliente, servico e itens
'''
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
                        
'''
# Banco produtos
'''


CriarTabelaOS = """ CREATE TABLE IF NOT EXISTS OS (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        nome text NOT NULL,
                        telefone text,
                        endereco text,
                        data_chegada DATE,
                        data_entrega DATE,
                        finalizado INTEGER
                        ); """


CriarTabelaServico = """ CREATE TABLE IF NOT EXISTS Servicos (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        descricao text,
                        valor REAL,
                        os_id INTEGER,
                        FOREIGN KEY (os_id) REFERENCES OS(id)
                        ); """

conexao = sqlite3.connect('database.db')
cursor = conexao.cursor()
cursor.execute(CriarTabelaOS)
cursor.execute(CriarTabelaServico)
'''

# Banco Produtos com estoque, codigo de barras e preço

CriarTabelaProdutos = """ CREATE TABLE IF NOT EXISTS Produtos (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        codigo integer INTEGER,
                        nome text NOT NULL,
                        quantidade INTEGER,
                        unidade TEXT,
                        quantidade_minima INTEGER,
                        preco REAL
                        ); """

conexao = sqlite3.connect('estoque.db')
cursor = conexao.cursor()
cursor.execute(CriarTabelaProdutos)