import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importar o arquivo csv

arq = pd.read_csv("Crash_Data.csv")

# Ocorrências por mês
def occurrences_month():
   
    months = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho',
          8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

    month_order = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
               'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    arq['Month'] = arq['Month'].replace(months)

    arq['Month'] = pd.Categorical(arq['Month'], categories=month_order, ordered=True)

    month_count = arq['Month'].value_counts().sort_index()

    return month_count

# Idades
def occurrences_age():

    ages = {'0_to_16': '0 à 16', '17_to_25': '17 à 25', '26_to_39': '26 à 39', '40_to_64': '40 à 64',
        '65_to_74': '65 à 74', '75_or_older': '75 +'}

    arq['Age Group'] = arq['Age Group'].replace(ages)

    age_count = arq['Age Group'].value_counts()

    return age_count

# Estados
def occurrence_state():

    states = {'NSW': 'New South Wales', 'Vic': 'Victoria', 'Qld': 'Queensland', 'SA': 'South Australia',
              'WA': 'Western Australia', 'Tas': 'Tasmania', 'NT': 'Northern Territory',
              'ACT': 'Australian Capital Territory'}

    arq['State'] = arq['State'].replace(states)

    state_count = arq['State'].value_counts()

    state_count_df = state_count.reset_index()

    return state_count_df

# Vítimas
def occurrence_victims():

    victims = {'Driver': 'Motorista', 'Passenger': 'Passageiro', 'Pedestrian': 'Pedestre',
               'Motorcycle rider': 'Motociclista', 'Motorcycle pillion passenger': 'Passageiro de moto',
               'Pedal cyclist': 'Ciclista', 'Other/-9': 'Outros'}

    arq['Road User'] = arq['Road User'].replace(victims)

    victim_count = arq['Road User'].value_counts()

    return victim_count

# Idades_Meses
def occurrence_age_month():

    age_month_count = pd.crosstab(index=arq['Month'], columns=arq['Age Group'])

    return age_month_count

# Ocorrências Totais

month_count = occurrences_month()
age_count = occurrences_age()
state_count = occurrence_state()
victim_count = occurrence_victims()
age_month_count = occurrence_age_month()
occurrence_count = occurrences_month().sum()

# Gráficos

fig, axs = plt.subplots(2, 3, figsize=(20, 15))
fig.suptitle('Acidentes de Trânsito Fatais na Austrália entre 1989 e 2021', fontsize=20)

# Gráfico de pizza

axs[0, 0].pie(age_count, labels = age_count.index, autopct='%1.1f%%')
axs[0, 0].set_title('Distribuição de Idades')

# Ocorrências Totais

axs[0, 1].remove()
axs[0, 1] = fig.add_subplot(2, 3, 2)

axs[0, 1].text(0.5, 0.5, f'Total de\nOcorrências:\n\n{occurrence_count}', ha='center', va='center', fontsize=30)
axs[0, 1].axis('off')

# Tabela

axs[0, 2].axis('tight')
axs[0, 2].axis('off')
axs[0, 2].set_title('Ocorrências por Estado', y=1)  # Adicionar título à tabela

labels = ['Estado', 'Número de Ocorrências']

table = axs[0, 2].table(cellText=state_count.values,
                        colLabels=labels,
                        cellLoc = 'center', 
                        loc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 3)  # Alterar o tamanho das células
table.auto_set_column_width(col=list(range(len(state_count.columns)))) # Ajustar a largura das colunas automaticamente

cells = table.properties()["children"]

for cell in cells:

    cell.set_edgecolor("black")  # Cor da borda
       
    if cell.get_text().get_text() in labels:
        cell.set_facecolor("grey")  # Cor do cabeçalho
    else:
        cell.set_facecolor("white")  # Cor das células

# Gráfico de linha

month_count.plot(kind='line', ax=axs[1, 0])
axs[1, 0].set_xticks(range(len(month_count.index)))
axs[1, 0].set_xticklabels(month_count.index, rotation=45)
axs[1, 0].set_title('Número de Ocorrências por Mês')
axs[1, 0].set_xlabel('Mês')
axs[1, 0].set_ylabel('Número de Ocorrências')

# Gráfico de barras

axs[1, 1].barh(victim_count.index, victim_count.values, color='skyblue')  # Criar o gráfico de barras horizontais
axs[1, 1].set_xlabel('Número de Ocorrências')  # Adicionar rótulo ao eixo x
axs[1, 1].set_ylabel('Tipo de Vítima')  # Adicionar rótulo ao eixo y
axs[1, 1].set_title('Número de Ocorrências por Tipo de Veículo')  # Adicionar título

# Gráfico de barras empilhadas

age_month_count.plot(kind='bar', stacked=True, ax=axs[1, 2])
axs[1, 2].set_xticks(range(len(month_count.index)))
axs[1, 2].set_xticklabels(month_count.index, rotation=45)
axs[1, 2].set_title('Número de Ocorrências por Mês e Grupo de Idades')  # Adicionar título
axs[1, 2].set_xlabel('Mês')  # Adicionar rótulo ao eixo x
axs[1, 2].set_ylabel('Número de Ocorrências')  # Adicionar rótulo ao eixo y
axs[1, 2].legend(title='Grupo de Idades')  # Adicionar legenda
axs[1, 2].legend(title='Grupo de Idades', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout(pad=5.0)  # Adiciona um preenchimento de 5 pontos de fonte
plt.show()