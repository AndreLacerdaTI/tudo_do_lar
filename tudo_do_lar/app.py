# Importando comandos dos bancos.py
from banco import *

from flask import Flask, render_template

# Insert Clientes
"""
nome = input('nome: ')
telefone = input('telefone: ')
endereco = input('telefone: ')

tabela = "Clientes"
colunas = ["nome", "telefone", "endereco"]
valores = [nome, telefone, endereco]

insert(tabela, colunas, valores)
"""
# Insert Item
"""
tipo = input('tipo: ')
marca = input('marca: ')
descricao = input('descricao: ')
servico_id = input('servico_id: ')

tabela = "Item"
colunas = ["tipo", "marca", "descricao", "servico_id"]
valores = [tipo, marca, descricao, servico_id]

insert(tabela, colunas, valores)
"""
# Insert Servico
"""
descricao = input('descricao: ')
cliente_id = input('cliente id: ')
tabela = "Servico"
colunas = ["descricao", "cliente_id"]
valores = [descricao, cliente_id]

insert(tabela, colunas, valores)

"""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/atualizar_clientes', methods=['POST'])
def atualizar_clientes():
    comando = "ORDER BY id"
    dados = select('Servicos' ,comando)
    print(dados)
    return render_template('index.html',clientes=dados)

@app.route('/atualizar_servicos', methods=['POST'])
def atualizar_servicos():
    comando = "ORDER BY nome"
    clientes = select(comando)
    print(clientes)
    return render_template('index.html',clientes=clientes)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='192.168.20.125')