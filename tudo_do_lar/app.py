# Importando comandos dos bancos.py
from banco import *

from relatorios import *

import qrcode

from datetime import datetime

from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Defina uma chave secreta para usar as sessões

@app.context_processor
def tema_global():
    busca_atual = session.get('busca', 'texto')
    return dict(busca=busca_atual)

# Rota para alternar o tema
@app.route('/alternar_busca', methods=['POST'])
def alternar_busca():
    busca_atual = session.get('busca', 'texto')
    nova_busca = 'data' if busca_atual == 'texto' else 'texto'
    session['busca'] = nova_busca
    return manutencao()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu', methods=['POST'])
def menu():
    endereco = request.form['endereco']
    if (endereco == 'manutencao'):
        os = tabela_dicionario_order('OS','id')
        valores = valores_dicionario(os)
        return render_template('manutencao.html',os=os,valores=valores,buscar='texto')
    if (endereco == 'relatorio'):
        grafico = grafico_pizza()
        return render_template('relatorio.html', imagem=grafico)
    return render_template(endereco+'.html')

# Pagina de manutenção

@app.route('/manutencao', methods=['POST'])
def manutencao():
    os = tabela_dicionario('OS')
    valores = valores_dicionario(os)
    return render_template('manutencao.html',os=os,valores=valores)
    #return render_template('manutencao.html',os=os)

@app.route('/filtrar_tabela', methods=['POST'])
def filtrar_tabela():
    filtro_tabela = request.form['filtro_tabela']
    os = tabela_dicionario_order('OS',filtro_tabela)
    valores = valores_dicionario(os)
    return render_template('manutencao.html',os=os,valores=valores)
    #return render_template('manutencao.html',os=os)

@app.route('/buscar_cadastro', methods=['POST'])
def buscar_cadastro():
    buscar = request.form['buscar']
    os = select_like('OS', buscar)
    valores = valores_dicionario(os)
    # Se a busca for por data ele exibirá a data formatada nos filtros
    if(session['busca']=='data'):
        data = buscar.split('-')
        buscar = data[2]+'/'+data[1]+'/'+data[0]
    return render_template('manutencao.html',os=os,valores=valores,filtro=buscar)
    #return render_template('manutencao.html',os=os)

@app.route('/nova_os', methods=['POST'])
def nova_os():
    return render_template('manutencao.html',nova_os=True)

@app.route('/novo_servico', methods=['POST'])
def novo_servico():
    os_id = request.form['os_id']
    os_id = insert('Servicos', ['os_id'], [os_id])
    print(os_id)
    return editar_os()


@app.route('/registrar_os', methods=['POST'])
def registrar_os():
    nome = request.form['nome']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    data_chegada = request.form['data_chegada']

    if data_chegada=='':
        data_atual = datetime.now()
        # Formatando a data
        data_chegada = data_atual.strftime("%Y-%m-%d")
    os_id = insert('OS', ['nome','telefone','endereco','data_chegada'], [nome,telefone,endereco,data_chegada])
    os = select_param('OS', 'id', os_id)
    qr = criar_qrcode(os[0])
    return abrir_editar_os(os_id)


@app.route('/salvar_servico', methods=['POST'])
def salvar_servico():
    nome = request.form['nome']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    id = insert('OS', ['nome','telefone','endereco'], [nome,telefone,endereco])
    os = select('OS','WHERE nome = '+nome)
    print(os)
    return render_template('manutencao.html',os=os)

@app.route('/editar_os', methods=['POST'])
def editar_os():
    os_id = request.form['os_id']
    info_os = select_param('OS', 'id', os_id)
    info_servicos = select_param('Servicos', 'os_id', os_id)
    print(info_servicos)
    if info_servicos:
        return render_template('manutencao.html', editar_os=True, info_os=info_os[0],info_servicos=info_servicos)
    else:
        return render_template('manutencao.html', editar_os=True, info_os=info_os[0])

def abrir_editar_os(os_id):
    info_os = select_param('OS', 'id', os_id)
    info_servicos = select_param('Servicos', 'os_id', os_id)
    if info_servicos:
        return render_template('manutencao.html', editar_os=True, info_os=info_os[0],info_servicos=info_servicos)
    else:
        return render_template('manutencao.html', editar_os=True, info_os=info_os[0])

@app.route('/salvar_alterações_os', methods=['POST'])
def salvar_alterações_os():
    comandos = request.form['comando']
    print(comandos)
    comando = comandos.split('-')
    print(comando[1])
    id = comando[0]
    if comando[1]=='salvar':
        nome = request.form['nome']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        data_chegada = request.form['data_chegada']
        if data_chegada=='':
            data_chegada = '-'
        data_entrega = request.form['data_entrega']
        if data_entrega=='':
            data_entrega = '-'
        finalizado = request.form['finalizado']
        update(nome, telefone, endereco, data_chegada, data_entrega, finalizado, id)
    elif comando[1]=='excluir':
        delete('OS',id)
    return manutencao()

@app.route('/alterar_servico', methods=['POST'])
def alterar_servico():
    comandos = request.form['comando']
    # Comando vem em formato: id_servico-comando-os_id
    comando = comandos.split('-')
    # Separamos o comando
    id = comando[0] # ID do servico
    os_id = comando[2] # ID da OS que ele pertence
    if comando[1]=='salvar':
        descricao = request.form['descricao']
        valor = request.form['valor']
        if valor=='':
            valor_formatado=0.0
        else:
            valor_formatado = float(valor.replace("R$", "").replace(" ", "").replace(",", "."))
        update_servico(descricao, valor_formatado, id)
    elif comando[1]=='excluir':
        delete('Servicos',id)
    return abrir_editar_os(os_id)

def criar_qrcode(valor):
        # Dados que você deseja codificar no QR code
    dados_qr_code = valor

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
    img.save("static/images/qrCode/%s.png" % valor[0])
    imagem= ("static/images/qrCode/%s.png" % valor[0])
    return imagem

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='192.168.20.125')