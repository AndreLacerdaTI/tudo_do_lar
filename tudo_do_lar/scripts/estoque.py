import sqlite3

# COMANDOS PARA CONTROLE DO BANCO DE DADOS

# Função para conectar com o banco e retornar dados
def connect_execute_estoque(execute):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute(execute)
    return cursor

def select_estoque(nome_tabela,comando):
    # O parametro 'comando' receberá o restante do select, como por exemplo: ORDER BY nome
    comando_select = ("SELECT * FROM "+nome_tabela+" "+comando)
    cursor = connect_execute_estoque(comando_select)
    dados = cursor.fetchall()
    return dados

def select_param_estoque(nome_tabela, coluna, valor):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM "+nome_tabela+" WHERE "+coluna+" = ?",(valor,))
    dados = cursor.fetchall()
    return dados

def update_estoque(nome, quantidade, id):
    conn = sqlite3.connect('estoque.db')
    cur = conn.cursor()
    cur.execute('UPDATE Produtos SET nome = ?, quantidade = ? WHERE id = ?', (nome, quantidade, id))
    conn.commit()
    conn.close()


def insert_estoque(nome_tabela, colunas, valores):
    # Inserindo no banco com os parametros enviados do app e front-end
    comando_insert = f"INSERT INTO {nome_tabela} ({', '.join(colunas)}) VALUES ({', '.join(['?']*len(valores))})"
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute(comando_insert,valores)

    # Obter o ID do registro recém-inserido
    inserted_id = cursor.lastrowid
    conexao.commit()
    return inserted_id

def delete(nome_tabela, id):
    conn = sqlite3.connect('estoque.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM "+nome_tabela+" WHERE id=?", (id,))
    conn.commit()
    conn.close()