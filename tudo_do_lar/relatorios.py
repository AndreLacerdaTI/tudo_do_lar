import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from banco import *

def limpar_graficos():
    print('teste')

def grafico_pizza():
    # Dados para o gráfico de pizza
    labels = ['Sim', 'Não']

    dados = select('OS','finalizado')
    sim = 0
    nao = 0
    for i in dados:
        if i[6]=='Não':
            nao = nao+1
        else:
            sim = sim+1
    dados = [sim, nao]
    #dados = [25, 40]

    # Criar o gráfico de pizza
    fig, ax = plt.subplots()
    ax.pie(dados, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Assegurar que o gráfico de pizza seja circular


    # Converter o gráfico para uma imagem BytesIO
    img_io = BytesIO()
    plt.savefig('static/images/graficos/grafico.png', format='png')
    img_io.seek(0)
    # Codificar a imagem em base64
    img_encoded = base64.b64encode(img_io.getvalue()).decode('utf-8')
    # Limpar a figura para evitar sobreposições
    plt.clf()
    plt.close()
    # Renderizar a imagem no template
    return img_encoded