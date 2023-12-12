import pandas as pd
import sqlite3

# Ler a planilha
planilha = pd.read_excel('./planilha.xlsx')

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('seu_banco_de_dados.db')
cursor = conn.cursor()

# Criar a tabela no banco de dados
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        quantidade INTEGER
    )
''')

# Inserir dados na tabela
for index, row in planilha.iterrows():
    codigo = row['Código']
    nome = row['Nome']
    quantidade = row['Quantidade']

    cursor.execute('''
        INSERT INTO produtos (id, nome, quantidade)
        VALUES (?, ?, ?)
    ''', (codigo, nome, quantidade))

# Commit para salvar as alterações
conn.commit()

# Fechar a conexão
conn.close()

print("Banco de dados criado e populado com sucesso.")