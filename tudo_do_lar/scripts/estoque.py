import sqlite3
from openpyxl import Workbook
import pandas as pd

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

def update_estoque(codigo, nome, quantidade, unidade, quantidade_minima, preco, id):
    conn = sqlite3.connect('estoque.db')
    cur = conn.cursor()
    print('update_estoque',preco)
    cur.execute('UPDATE Produtos SET codigo = ?, nome = ?, quantidade = ?, unidade = ?, quantidade_minima = ?, preco = ? WHERE id = ?', (codigo, nome, quantidade, unidade, quantidade_minima, preco, id))
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

def exportar_tabela_para_excel(nome_banco, nome_tabela, comando, campos, nome_arquivo_excel):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()

    # Construir a string SQL para selecionar os campos específicos
    campos_str = ', '.join(campos)
    print(comando)
    query_sql = f'SELECT {campos_str} FROM {nome_tabela} {comando}'

    # Executar a consulta para obter os dados da tabela
    cursor.execute(query_sql)
    dados_tabela = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    # Criar um novo arquivo Excel
    wb = Workbook()
    planilha = wb.active

    # Adicionar cabeçalho (nomes dos campos)
    planilha.append(campos)

    # Adicionar os dados da tabela
    for linha in dados_tabela:
        planilha.append(linha)

    # Salvar o arquivo Excel
    caminho = './static/planilhas/'+nome_arquivo_excel
    wb.save(caminho)
    # Retorna o caminho sem o "." para o html encontrar o arquivo para download
    return caminho[1:]
    #print(f'O arquivo Excel "{nome_arquivo_excel}" foi criado com sucesso.')
    #return '/static/planilhas/estoque%20baixo.xlsx'