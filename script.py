import pandas as pd
import matplotlib.pyplot as plt

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

fig, axs = plt.subplots(2, 3, figsize=(20, 15)) # Criar a figura e o grid de subplots 2x3 com o tamanho 20x15
fig.suptitle('Acidentes de Trânsito Fatais na Austrália entre 1989 e 2021', fontsize=20) # Adicionar título à figura

# Gráfico de pizza

axs[0, 0].pie(age_count, labels = age_count.index, autopct='%1.1f%%') # Criar o gráfico de pizza com as idades na posição 0,0
axs[0, 0].set_title('Distribuição de Idades') # Adicionar título

# Ocorrências Totais

axs[0, 1].remove() # Remover o gráfico vazio da posição 0,1
axs[0, 1] = fig.add_subplot(2, 3, 2) # Adicionar um novo subplot na posição 0,1 com o tamanho 2x3 e o índice 2

axs[0, 1].text(0.5, 0.5, f'Total de\nOcorrências:\n\n{occurrence_count}', ha='center', va='center', fontsize=30) # Adicionar o texto com o total de ocorrências
axs[0, 1].axis('off') # Remover os eixos

# Tabela

axs[0, 2].axis('tight') # Remover os espaços em branco
axs[0, 2].axis('off') # Remover os eixos
axs[0, 2].set_title('Ocorrências por Estado', y=1)  # Adicionar título à tabela

labels = ['Estado', 'Número de Ocorrências'] # Criar a lista de cabeçalhos

table = axs[0, 2].table(cellText=state_count.values, # Criar a tabela com os valores do número de ocorrências por estado na posição 0,2
                        colLabels=labels, # Adicionar os cabeçalhos das colunas
                        cellLoc = 'center', # Centralizar o texto das células
                        loc='center') # Centralizar a tabela no subplot

table.auto_set_font_size(False) # Desabilitar o ajuste automático do tamanho da fonte
table.set_fontsize(10) # Alterar o tamanho da fonte das células
table.scale(1, 3)  # Alterar o tamanho das células
table.auto_set_column_width(col=list(range(len(state_count.columns)))) # Ajustar a largura das colunas automaticamente ao texto

cells = table.properties()["children"] # Armazenar as propriedades das células na variável cells

for cell in cells: # Criar um loop para percorrer as células

    cell.set_edgecolor("black")  # Cor da borda = black
       
    if cell.get_text().get_text() in labels: # Se o texto da célula estiver na lista de cabeçalhos
        cell.set_facecolor("grey")  # Cor do cabeçalho = grey
    else: # Se não
        cell.set_facecolor("white")  # Cor das células = white

# Gráfico de linha

month_count.plot(kind='line', ax=axs[1, 0]) # Criar o gráfico de linha com o número de ocorrências por mês na posição 1,0 
axs[1, 0].set_xticks(range(len(month_count.index))) # Adicionar os ticks no eixo x com o número de meses
axs[1, 0].set_xticklabels(month_count.index, rotation=45) # Adicionar os rótulos em cada tick no eixo x com o nome dos meses e rotacionar 45 graus
axs[1, 0].set_title('Número de Ocorrências por Mês') # Adicionar título
axs[1, 0].set_xlabel('Mês') # Adicionar rótulo ao eixo x
axs[1, 0].set_ylabel('Número de Ocorrências') # Adicionar rótulo ao eixo y

# Gráfico de barras

axs[1, 1].barh(victim_count.index, victim_count.values, color='skyblue')  # Criar o gráfico de barras horizontais com o número de ocorrências por tipo de vítima na posição 1,1
axs[1, 1].set_xlabel('Número de Ocorrências')  # Adicionar rótulo ao eixo x
axs[1, 1].set_ylabel('Tipo de Vítima')  # Adicionar rótulo ao eixo y
axs[1, 1].set_title('Número de Ocorrências por Tipo de Veículo')  # Adicionar título

# Gráfico de barras empilhadas

age_month_count.plot(kind='bar', stacked=True, ax=axs[1, 2]) # Criar o gráfico de barras empilhadas com o número de ocorrências por mês e grupo de idades na posição 1,2
axs[1, 2].set_xticks(range(len(month_count.index))) # Adicionar os ticks no eixo x com o número de meses
axs[1, 2].set_xticklabels(month_count.index, rotation=45) # Adicionar os rótulos em cada tick no eixo x com o nome dos meses e rotacionar 45 graus
axs[1, 2].set_title('Número de Ocorrências por Mês e Grupo de Idades')  # Adicionar título
axs[1, 2].set_xlabel('Mês')  # Adicionar rótulo ao eixo x
axs[1, 2].set_ylabel('Número de Ocorrências')  # Adicionar rótulo ao eixo y
axs[1, 2].legend(title='Grupo de Idades')  # Adicionar legenda
axs[1, 2].legend(title='Grupo de Idades', bbox_to_anchor=(1.05, 1), loc='upper left') # Posicionar a legenda fora do gráfico

plt.tight_layout(pad=5.0)  # Adiciona um preenchimento de 5 pontos de fonte entre os subplots
plt.show() # Mostrar o gráfico