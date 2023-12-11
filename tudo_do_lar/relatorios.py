import plotly.express as px

from banco import *

def concluidos_pendentes():
    dados = select('OS','finalizado')
    sim = 0
    nao = 0
    for i in dados:
        if i[6]=='Não':
            nao = nao+1
        else:
            sim = sim+1
    total = sim+nao
    dados = {'status': ['Concluídos: '+str(sim), 'Pendentes: '+str(nao)],
             'quantidade': [int(sim*100/total), int(nao*100/total)]}

    grafico = gerar_grafico(dados)
    return grafico

def gerar_grafico(dados):
 # Dados de exemplo (você pode substituir isso pelos seus dados reais)
    #servicos = ['Concluídos', 'Pendentes']
    #valores = [30, 70]  # Porcentagens, por exemplo
    #dados = {'status': ['Concluídos', 'Pendentes'],
    #         'quantidade': [valores[0], valores[1]]}
    
    # Criar gráfico Plotly
    #fig = px.pie(names=servicos, values=valores, title='Status dos Serviços')

    # Converter gráfico Plotly em HTML
    #plot_html = fig.to_html(full_html=False)

    fig = px.pie(dados, names='status', values='quantidade', title='Status dos Serviços',
                 color_discrete_sequence=['#E88120', '#1C3354'], width=500, height=400)  # Substitua as cores conforme necessário

    fig.update_layout(
        font=dict(
            family="Roboto Slab, serif",  # Substitua pela fonte desejada
            size=15,  # Tamanho da fonte
            color="black"  # Cor da fonte
        )
    )
    # Converter gráfico Plotly em json
    plot_json = fig.to_json()

    return plot_json
    #return plot_html
