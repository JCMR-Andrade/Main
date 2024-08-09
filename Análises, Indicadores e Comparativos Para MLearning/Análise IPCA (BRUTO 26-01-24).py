# -*- coding: utf-8 -*-

'''ANÁLISE DA INFLAÇÃO BRASILEIRA NO PYTHON'''
# Importa as bibliotecas necessárias
import sidrapy 
import numpy as np
import pandas as pd 
import datetime as dt 
import seaborn as sns
from matplotlib import pyplot as plt

'''Usamos a função get_table para importar os dados de acordo com os parâmetros da API acima.'''
# Importa as variações do IPCA
ipca_raw = sidrapy.get_table(table_code = '1737',
                             territorial_level = '1',
                             ibge_territorial_code = 'all',
                             variable = '63,69,2263,2264,2265',
                             period = 'last%20472')

# Realiza a limpeza e manipulação da tabela
ipca =  (
    ipca_raw
    .loc[1:,['V', 'D2C', 'D3N']]
    .rename(columns = {'V': 'value',
                       'D2C': 'date',
                       'D3N': 'variable'}
            )
    .assign(variable = lambda x: x['variable'].replace({'IPCA - Variação mensal' : 'Var. mensal (%)',
                                                        'IPCA - Variação acumulada no ano': 'Var. acumulada no ano (%)', 
                                                        'IPCA - Variação acumulada em 3 meses' : 'Var. MM3M (%)',
                                                        'IPCA - Variação acumulada em 6 meses': 'Var. MM6M (%)',
                                                        'IPCA - Variação acumulada em 12 meses' : 'Var. MM12M (%)'}),
            date  = lambda x: pd.to_datetime(x['date'],
                                              format = "%Y%m"),
            value = lambda x: x['value'].astype(float)
           )
    .pipe(lambda x: x.loc[x.date > '2007-01-01']
          )
        )

# Configura o tema do gráfico
## Cores
colors = ['#282f6b', '#b22200', '#eace3f', '#224f20', '#b35c1e', '#419391', '#839c56','#3b89bc']
 
## Tamanho
theme = {'figure.figsize' : (15, 10)}
 
## Aplica o tema
sns.set_theme(rc = theme,
              palette = colors)
# Filtra somente para o IPCA acumulado em 12 meses
ipca_12m = (   
            ipca
            .pipe(lambda x: x.loc[x.variable == 'Var. MM12M (%)'])
           )
 
# Plota o IPCA acumulado em 12 meses
sns.lineplot(x = 'date',
             y = 'value',
             data = ipca_12m).set(title = 'IPCA acumulado em 12 meses',
                                                           xlabel = '',
                                                           ylabel = '% a.a.')
 
# Adiciona a fonte no gráfico           
plt.annotate('Fonte: analisemacro.com.br com dados do Sidra/IBGE',
            xy = (1.0, -0.08),
            xycoords='axes fraction',
            ha='right',
            va="center",
            fontsize=10)

# Plota todas as variações
g = sns.FacetGrid(ipca, col = 'variable',
                  col_wrap = 2,
                  hue = 'variable',
                  sharey = False,
                  height = 4,
                  aspect = 2)
 
 
g.map_dataframe(sns.lineplot, 
                x = 'date',
                y = 'value').set(xlabel = "",
                                 ylabel = '%')
 
# Adiciona a fonte no gráfico           
plt.annotate('Fonte: analisemacro.com.br com dados do Sidra/IBGE',
            xy = (1.0, -0.13),
            xycoords='axes fraction',
            ha='right',
            va="center",
            fontsize=10)

plt.show()

'''IPCA Contribuição por grupo
A contribuição por grupo do IPCA possibilita analisarmos qual grupo possuiu a maior contribuição na variação mensal. A API obtida no SIDRA para a importação da série segue abaixo.'''
# Importa as variações e os pesos dos grupos do IPCA

ipca_gp_raw = sidrapy.get_table(table_code = '7060',
                             territorial_level = '1',
                             ibge_territorial_code = 'all',
                             variable = '63,66',
                             period = 'all',
                             classification = '315/7170,7445,7486,7558,7625,7660,7712,7766,7786'
                             )

# Realiza a limpeza e manipulação da tabela
ipca_gp =  (
    ipca_gp_raw
    .loc[1:,['V', 'D2C', 'D3N', 'D4N']]
    .rename(columns = {'V': 'value',
                       'D2C': 'date',
                       'D3N': 'variable',
                       'D4N': 'groups'})
    .assign(variable = lambda x: x['variable'].replace({'IPCA - Variação mensal' : 'variacao',
                                                        'IPCA - Peso mensal': 'peso'}),
            date  = lambda x: pd.to_datetime(x['date'],
                                              format = "%Y%m"),
            value = lambda x: x['value'].astype(float),
            groups = lambda x: x['groups'].astype(str)
           )
    .pipe(lambda x: x.loc[x.date > '2007-01-01'])
        )

# Torna em formato wide e calcula a contribuição de cada grupo pro IPCA
ipca_gp_wider = (
    ipca_gp
    .pivot_table(index = ['date', 'groups'],
                 columns = 'variable',
                 values = 'value')
    .reset_index()
    .assign(contribuicao = lambda x: (x.peso * x.variacao) / 100)
                )


# Importa a biblioteca plotly
import plotly.express as px

# Plota a contribuição de cada grupo com plotly
fig = px.bar(ipca_gp_wider,
       x = 'date',
       y = 'contribuicao',
       color = 'groups',
       color_discrete_sequence = colors)

# Salva a figura em um arquivo HTML e abre no navegador
# fig.write_html("figura.html", auto_open=True)

# Ou salva a figura em um arquivo de imagem e abre no visualizador padrão
fig.write_image("figura.png", scale=2)

import os
os.startfile("figura.png")

fig.show()