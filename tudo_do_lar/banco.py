import sqlite3

# COMANDOS PARA CONTROLE DO BANCO DE DADOS

# Função para 
def connect_execute(execute):
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()
    cursor.execute(execute)
    return cursor

def select(nome_tabela,comando):
    # O parametro 'comando' receberá o restante do select, como por exemplo: ORDER BY nome
    comando_select = "SELECT * FROM "+nome_tabela+" "+comando
    cursor = connect_execute(comando_select)
    dados = cursor.fetchall()
    return dados
    
def insert(nome_tabela, colunas, valores):
    comando_insert = f"INSERT INTO {nome_tabela} ({', '.join(colunas)}) VALUES ({', '.join(['?']*len(colunas))})"
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()
    cursor.execute(comando_insert,valores)
    conexao.commit()