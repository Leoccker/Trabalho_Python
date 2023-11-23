import plotly.express as px
import pandas as pd
# Importar o arquivo csv
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

# Gráficos
fig = px.pie(age_count, values=age_count.values, names=age_count.index, title='Distribuição de Idades') # Gráfico de pizza
fig.show()

fig = px.bar(state_count, x='index', y='State', title='Ocorrências por Estado') # Gráfico de barras
fig.show()

fig = px.line(month_count, x=month_count.index, y=month_count.values, title='Número de Ocorrências por Mês') # Gráfico de linha
fig.show()

fig = px.bar(victim_count, x=victim_count.values, y=victim_count.index, orientation='h', title='Número de Ocorrências por Tipo de Veículo') # Gráfico de barras horizontais
fig.show()

fig = px.bar(age_month_count, x=age_month_count.index, y=age_month_count.columns, barmode='stack', title='Número de Ocorrências por Mês e Grupo de Idades') # Gráfico de barras empilhadas
fig.show()
