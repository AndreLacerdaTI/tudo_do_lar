import sqlite3

# COMANDOS PARA CONTROLE DO BANCO DE DADOS

# Função para conectar com o banco e retornar dados
def connect_execute(execute):
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()
    cursor.execute(execute)
    return cursor

def select_param(nome_tabela, coluna, valor):
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM "+nome_tabela+" WHERE "+coluna+" = ?",(valor,))
    dados = cursor.fetchall()
    return dados

def select_like(nome_tabela, valor):
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM "+nome_tabela+" WHERE nome LIKE '%' || ? || '%' OR telefone LIKE '%' || ? || '%' OR data_chegada LIKE '%' || ? || '%' OR data_entrega LIKE '%' || ? || '%'", (valor,valor,valor,valor))
    colunas = [col[0] for col in cursor.description]
    dicionario = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
    return dicionario

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

    # Obter o ID do registro recém-inserido
    inserted_id = cursor.lastrowid
    conexao.commit()
    return inserted_id

def update(nome, telefone, endereco, data_chegada, data_entrega, finalizado, id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('UPDATE OS SET nome = ?, telefone = ?, endereco = ?, data_chegada = ?, data_entrega = ?, finalizado = ? WHERE id = ?', (nome, telefone, endereco, data_chegada, data_entrega, finalizado, id))
    conn.commit()
    conn.close()

def update_servico(descricao, valor, id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('UPDATE Servicos SET descricao = ?, valor = ? WHERE id = ?', (descricao, valor, id))
    conn.commit()
    conn.close()

def delete(nome_tabela, id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM "+nome_tabela+" WHERE id=?", (id,))
    conn.commit()
    conn.close()

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

def tabela_os_dicionario_consulta(filtro):
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Executar a consulta para finalizados ou não finalizados
    if type(filtro)!=list:
        consulta = "SELECT * FROM OS WHERE finalizado = ?"
        cursor.execute(consulta, (filtro,))
    else:
        consulta = "SELECT * FROM OS WHERE data_chegada BETWEEN ? AND ? ORDER BY data_chegada"
        cursor.execute(consulta, (filtro[0], filtro[1]))
    # Obter os resultados como uma lista de dicionários
    colunas = [col[0] for col in cursor.description]
    #dados = cursor.fetchall()
    #print(dados)
    dicionario = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
    # Fechar a conexão com o banco de dados
    conn.close()

    # Renderizar o template com os dados
    return dicionario

def tabela_dicionario_order(nome_tabela,comando):
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Executar a consulta para obter dados dos usuários
    comando = 'SELECT * FROM '+nome_tabela+' ORDER BY '+comando
    cursor.execute(comando)
    # Obter os resultados como uma lista de dicionários
    colunas = [col[0] for col in cursor.description]
    dicionario = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

    # Fechar a conexão com o banco de dados
    conn.close()

    # Renderizar o template com os dados
    return dicionario

def valores_dicionario(os):
    # Somando os valores dos serviços e exportando em um dicionario formatado em R$
    valores = {}
    for os_id in os:
        id = os_id['id']
        info_servicos = select_param('Servicos', 'os_id', id)
        total = 0
        for valor in info_servicos:
            id = valor[3]
            preco = valor[2]
            total = total + preco
            valor_real = "R$ {:,.2f}".format(total)
            valor_formatado = valor_real.replace('.',',')
        valores[id] = valor_formatado
        valor_formatado = 'Sem serviço'
    return valores

def converir_valores_nulos(valor):
    if valor=='' or valor=='None':
        return None
    else:
        return valor
