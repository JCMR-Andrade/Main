# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime
import investpy as inv
from pylab import mpl, plt


df = inv.get_stocks_overview(country='Brazil', as_json=False, n_results=150
                             )

print(df)
# Vamos realizar uma análise de indicadores da empresa ITAUSA, com base no ticker ITS4. O ticker é necessário para que seja possível
# importar as informações da empresa, no caso, os demonstrativos: Demonstração de resultado (receitas e lucro);
# Balanço Patrimonial (ativos, passivos e patrimônio líquido) e Demonstração de fluxo de caixa.
ticker = "ITSA4"

# '''Para importar as receitas e o lucro, utilizamos a função get_stock_financial_summary, com o argumento stock referenciando o ticker,
# country para o país (Brazil), summary_type para o tipo do demonstrativo (income_statement) e o período,
# podendo ser anual (annual) ou trimestral (quarterly).'''

itsa_dre = inv.get_stock_financial_summary(stock=ticker,
                                           country="Brazil",
                                           summary_type="income_statement",
                                           period="annual")
print(itsa_dre, '01')

# '''Realizamos o mesmo procedimento para o balanço patrimonial, alterando o argumento summary_type para "balance_sheet".'''
itsa_bs = inv.get_stock_financial_summary(stock=ticker,
                                          country="Brazil",
                                          summary_type="balance_sheet",
                                          period="annual")
print(itsa_bs, '02')

# '''Apesar de não utilizarmos posteriormente, é possível importar também a demonstração de fluxo de caixa.'''
itsa_cf = inv.get_stock_financial_summary(stock=ticker,
                                          country="Brazil",
                                          summary_type="cash_flow_statement",
                                          period="annual")
print(itsa_cf, '03')

# '''Return on Equity (ROE)
# O retorno sobre o patrimônio mede a rentabilidade sobre o capital da empresa, ou seja, a eficiência da empresa em utilizar os seus recursos próprios.
#  Esse indicador é importante para entender a taxa de crescimento da empresa.'''
ROE = itsa_dre['Net Income'] / itsa_bs['Total Equity'] * 100

ROE
print(ROE, '04')

# '''Return on Asset (ROA)
# Retorno sobre os ativos mede a rentabilidade da empresa em relação aos seus ativos, ou seja, o se ela consegue usar eficientemente
# os seus ativos para gerar lucro. Diferente do ROE, a ROA exprime o quão alavancada uma empresa está, isto porque os ativos totais
# incluem a quantidade de capital emprestado para executar suas operações.'''
ROA = itsa_dre['Net Income'] / itsa_bs['Total Assets'] * 100

ROA
print(ROA, '05')

# '''Análise de ações
# Para analisar uma empresa, é possível  relacionar o seu valor com o preço da ação negociado.
# Antes de criar os indicadores desse tipo de medida, devemos buscar os dados do número de ações em circulação da empresa.
# Realizamos esse procedimento com a função get_stock_information, com o ticker, o país e com o argumento as_json = False (para retornar um data frame).
# Das informações coletadas, iremos utilizar somente a coluna "Shares Outstanding".'''
itsa = inv.get_stock_information(stock='AGRO3',
                                 country="Brazil",
                                 as_json=False)

itsa["Shares Outstanding"]
print(itsa)

# '''Lucro por ação
# O LPA mede a rentabilidade por cada ação que possui em circulação.
# Quanto maior o LPA da empresa, maior o seu valor (investidores irão pagar mais pela ação).
# O LPA é necessário também para calcular o P/L da empresa que abordaremos a seguir.'''
LPA = itsa_dre['Net Income'] * 1000000 / itsa["Shares Outstanding"].values

LPA

# '''Preço / Lucro
# O P/L é utilizado para avaliar se o preço das ações de uma empresa está caro ou barato.
# Teoricamente, indica o número de anos que um investidor demoraria para recuperar o capital investido.
# No código, primeiro devemos importar os dados da cotação da ITSA4 para realizar o cálculo do P/L.
# O primeiro passo deste processo é definir as datas de inicio e fim com base nas datas capturadas pelos demonstrativos importados anteriormente,
# com isso, a ideia é que obtemos uma maior automação. Para definir essas datas, pegamos o primeiro e último valor do índice do data frame itsa_dre.
# Em seguida, utilizamos o método strftime para transformar em string e definir o formar de dia/mês/ano (a função get_stock_historical_data só aceita
# a data neste formato).'''

start = itsa_dre.index[-1].strftime(format="%d/%m/%Y")
end = itsa_dre.index[0].strftime(format="%d/%m/%Y")
# Uma vez definidos as datas de inicio e de fim, utilizamos a função get_stock_historical_data para buscar a cotação do ativo.
itsa_price = inv.get_stock_historical_data(stock=ticker,
                                           country="Brazil",
                                           from_date=start,
                                           to_date=end)

# '''Para realizar o cálculo, é necessário utilizar os preços de fechamentos, contidos da coluna "Close".
# Realiza-se a junção com o data frame do LPA, completa-se os dados faltantes (os preços são diários, causando problemas com a coluna do LPA).
# E por fim, retira-se os dados faltantes restantes. Ao final do código, renomeamos as colunas e calculamos o P/L.'''
# Junta os objetos LPA e a coluna Close de itsa_price
pl = pd.concat([LPA, itsa_price['Close']], axis=1)

# Completa os valores faltantes
pl.fillna(method="ffill", inplace=True)

# Retira os valores faltantes
pl.dropna(inplace=True)

# Renomeia as colunas
pl = pl.rename({"Net Income": "LPA",
                "Close": 'Price'}, axis='columns')

# Calcula o P/L
pl["pl"] = pl["Price"] / pl["LPA"]


plt.style.use('seaborn')
