import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

arq = pd.read_csv("Crash_Data.csv") # Importar o arquivo csv

# Ocorrências por mês
def occurrences_month(): # Criar a função
   
    months = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho',
          8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'} # Criar o dicionário de meses

    month_order = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
               'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'] # Criar a lista de meses em ordem

    arq['Month'] = arq['Month'].replace(months) # Substituir os números pelos meses

    arq['Month'] = pd.Categorical(arq['Month'], categories=month_order, ordered=True) # Ordenar os meses

    month_count = arq['Month'].value_counts().sort_index() # Contar o número de ocorrências por mês e ordenar

    return month_count # Retornar o número de ocorrências por mês

# Idades
def occurrences_age(): # Criar a função

    ages = {'0_to_16': '0 à 16', '17_to_25': '17 à 25', '26_to_39': '26 à 39', '40_to_64': '40 à 64',
        '65_to_74': '65 à 74', '75_or_older': '75 +'} # Criar o dicionário de idades

    arq['Age Group'] = arq['Age Group'].replace(ages) # Formatar as idades

    age_count = arq['Age Group'].value_counts() # Contar o número de ocorrências por idade

    return age_count # Retornar o número de ocorrências por idade

# Estados
def occurrence_state(): # Criar a função

    states = {'NSW': 'New South Wales', 'Vic': 'Victoria', 'Qld': 'Queensland', 'SA': 'South Australia',
              'WA': 'Western Australia', 'Tas': 'Tasmania', 'NT': 'Northern Territory',
              'ACT': 'Australian Capital Territory'} # Criar o dicionário de estados

    arq['State'] = arq['State'].replace(states) # Substituir as siglas dos estados pelos nomes

    state_count = arq['State'].value_counts() # Contar o número de ocorrências por estado

    state_count_df = state_count.reset_index() # Resetar o índice

    return state_count_df # Retornar o número de ocorrências por estado

# Vítimas
def occurrence_victims(): # Criar a função

    victims = {'Driver': 'Motorista', 'Passenger': 'Passageiro', 'Pedestrian': 'Pedestre',
               'Motorcycle rider': 'Motociclista', 'Motorcycle pillion passenger': 'Passageiro de moto',
               'Pedal cyclist': 'Ciclista', 'Other/-9': 'Outros'} # Criar o dicionário de vítimas

    arq['Road User'] = arq['Road User'].replace(victims) # Substituir os nomes das vítimas pelos nomes em português

    victim_count = arq['Road User'].value_counts() # Contar o número de ocorrências por tipo de vítima

    return victim_count # Retornar o número de ocorrências por tipo de vítima

# Idades_Meses
def occurrence_age_month(): # Criar a função

    age_month_count = pd.crosstab(index=arq['Month'], columns=arq['Age Group']) # Criar a tabela cruzada idade/meses

    return age_month_count # Retornar a tabela cruzada idade/meses

# Trazer as variáveis para o script principal
month_count = occurrences_month() 
age_count = occurrences_age()
state_count = occurrence_state()
victim_count = occurrence_victims()
age_month_count = occurrence_age_month()
occurrence_count = occurrences_month().sum()

# Gráfico de pizza
labels_age = age_count.index
values_age = age_count.values

fig1 = go.Figure(data=[go.Pie(labels=labels_age, values=values_age)])

fig1.update_layout(
    title_text="Ocorrências por Faixa Etária",
    title_x=0.5,
    title_font=dict(size=24),
    autosize=True,
    font=dict(size=18)
)

fig1.show()

# Gráfico de linha
x_month = month_count.index
y_month = month_count.values

fig2 = go.Figure(data=go.Scatter(x=x_month, y=y_month, mode='lines+markers'))

fig2.update_layout(
    title_text="Ocorrências por Mês",
    title_x=0.5,
    title_font=dict(size=24),
    autosize=True,
    xaxis_title="Mês",
    yaxis_title="Ocorrências",
    font=dict(size=18)
)

fig2.show()

# Gráfico de barras horizontais
x_victim = victim_count.values
y_victim = victim_count.index

fig3 = go.Figure(data=[go.Bar(x=x_victim, y=y_victim, orientation='h')])

fig3.update_layout(
    title_text="Ocorrências por Tipo de Vítima",
    title_x=0.5,
    title_font=dict(size=24),
    autosize=True,
    xaxis_title="Ocorrências",
    yaxis_title="Tipo de Vítima",
    font=dict(size=18)
)

fig3.update_xaxes(tickformat=".0f")

fig3.show()

# Tabela de ocorrências por estado
header_state = ["Estado", "Ocorrências"]
cell_state = [state_count["State"], state_count["count"]]

fig4 = go.Figure(data=[go.Table(
                                header=dict(values=header_state, font=dict(size=20), height=50),
                                cells=dict(values=cell_state, font=dict(size=20), height=50))])

fig4.update_layout(
    title_text="Ocorrências por Estado",  # Adicione esta linha
    title_x=0.5,
    title_font=dict(size=24),
    autosize=True,
    font=dict(size=18)
)

fig4.show()

# Gráfico de calor
x_age_month = age_month_count.columns
y_age_month = age_month_count.index
z_age_month = age_month_count.values

fig5 = go.Figure(data=go.Heatmap(x=x_age_month, y=y_age_month, z=z_age_month))

fig5.update_layout(
    title_text="Ocorrências por Mês e Faixa Etária",
    title_x=0.5,
    title_font=dict(size=24),
    autosize=True,
    xaxis_title="Mês",
    yaxis_title="Faixa Etária",
    font=dict(size=18)
)

fig5.show()

fig = make_subplots(rows=2, cols=2, subplot_titles=("Gráfico de Pizza", "Gráfico de Linha", "Gráfico de Barras", "Gráfico de Calor"), specs=[[{'type': 'domain'}, {}], [{}, {}]])

# Adiciona cada figura ao subplot
fig.add_trace(go.Pie(labels=fig1.data[0]['labels'], values=fig1.data[0]['values'], showlegend=False), row=1, col=1)
fig.add_trace(go.Scatter(x=fig2.data[0]['x'], y=fig2.data[0]['y'], mode='lines+markers', showlegend=False), row=1, col=2)
fig.add_trace(go.Bar(x=fig3.data[0]['x'], y=fig3.data[0]['y'], orientation='h', showlegend=False), row=2, col=1)
fig.add_trace(go.Heatmap(x=fig5.data[0]['x'], y=fig5.data[0]['y'], z=fig5.data[0]['z'], showscale=True, colorbar=dict(len=0.5, y=0.2)), row=2, col=2)

# Adiciona uma legenda manualmente
fig.update_layout(
    annotations=[
        dict(text='Gráfico de Pizza', x=0.225, y=1.02, font=dict(size=24), showarrow=False),
        dict(text='Gráfico de Linha', x=0.775, y=1.02, font=dict(size=24), showarrow=False),
        dict(text='Gráfico de Barras', x=0.225, y=0.4, font=dict(size=24), showarrow=False),
        dict(text='Gráfico de Calor', x=0.775, y=0.4, font=dict(size=24), showarrow=False)
    ],
    font = dict(size=18)
)

fig.update_xaxes(tickformat=".0f", row=2, col=1)

fig.show()