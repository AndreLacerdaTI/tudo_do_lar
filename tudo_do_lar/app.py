# Importando comandos dos bancos.py
from banco import *

import qrcode

from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Defina uma chave secreta para usar as sessões

@app.context_processor
def tema_global():
    tema_atual = session.get('tema', 'branco')
    return dict(tema=tema_atual)

# Rota para alternar o tema
@app.route('/alternar_tema', methods=['POST'])
def alternar_tema():
    filtros = request.form.getlist('botao_checkbox')
    print(filtros)
    tema_atual = session.get('tema', 'branco')
    novo_tema = 'laranja' if tema_atual == 'branco' else 'branco'
    session['tema'] = novo_tema
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/itens', methods=['POST'])
def itens():
    cliente_id = request.form['cliente_id']
    itens = select('Itens','WHERE cliente_id = '+cliente_id)
    return render_template('manutencao.html',itens=itens)

@app.route('/servicos', methods=['POST'])
def servicos():
    item_id = request.form['item_id']
    servicos = select('Servicos','WHERE item_id = '+item_id)
    return render_template('manutencao.html',servicos=servicos)

@app.route('/menu', methods=['POST'])
def menu():
    endereco = request.form['endereco']
    if (endereco == 'manutencao'):
        comando = "ORDER BY id"
        dados = select('Clientes' ,comando)
        return render_template('manutencao.html',clientes=dados)
    return render_template(endereco+'.html')

@app.route('/manutencao', methods=['POST'])
def manutencao():
    clientes = tabela_dicionario('Clientes')
    itens = tabela_dicionario('Itens')
    servicos = tabela_dicionario('Servicos')
    print(clientes,itens,servicos)
    return render_template('manutencao.html',clientes=clientes,itens=itens,servicos=servicos)

@app.route('/criar_qrcode', methods=['POST'])
def criar_qrcode():    
    cliente_id = request.form['cliente_id']
    print(cliente_id)
        # Dados que você deseja codificar no QR code
    dados_qr_code = cliente_id

    # Criar objeto QRCode
    qr = qrcode.QRCode(
        version=1,  # Versão do QR code (1 a 40, 1 é o menor)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nível de correção de erros
        box_size=10,  # Tamanho da caixa
        border=4,  # Espaçamento da borda
    )

    # Adicionar os dados ao objeto QRCode
    qr.add_data(dados_qr_code)
    qr.make(fit=True)

    # Criar uma imagem do QR code usando a biblioteca Pillow (PIL Fork)
    img = qr.make_image(fill_color="black", back_color="white")

    # Salvar a imagem
    img.save("static/images/%s.png" % cliente_id)
    return ("static/images/%s.png" % cliente_id)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='192.168.20.125')