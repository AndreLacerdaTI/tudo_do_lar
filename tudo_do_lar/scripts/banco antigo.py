import sqlite3

# COMANDOS PARA CONTROLE DO BANCO DE DADOS

# Função para 
def connect_execute(execute):
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()
    cursor.execute(execute)
    return cursor

def select_like(nome_tabela, valor):
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM "+nome_tabela+" WHERE nome LIKE '%' || ? || '%'", (valor,))
    dados = cursor.fetchall()
    return dados

def select(nome_tabela,comando):
    # O parametro 'comando' receberá o restante do select, como por exemplo: ORDER BY nome
    comando_select = "SELECT * FROM "+nome_tabela+" "+comando
    cursor = connect_execute(comando_select)
    dados = cursor.fetchall()
    return dados
    
def insert(nome_tabela, colunas, valores):
    # Inserindo no banco com os parametros enviados do app e front-end
    comando_insert = f"INSERT INTO {nome_tabela} ({', '.join(colunas)}) VALUES ({', '.join(['?']*len(valores))})"
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()
    cursor.execute(comando_insert,valores)
    conexao.commit()

def tabela_dicionario(nome_tabela):
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Executar a consulta para obter dados dos usuários
    comando = 'SELECT * FROM '+nome_tabela
    cursor.execute(comando)
    
    # Obter os resultados como uma lista de dicionários
    colunas = [col[0] for col in cursor.description]
    dicionario = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

    # Fechar a conexão com o banco de dados
    conn.close()

    # Renderizar o template com os dados
    return dicionario