# -*- coding: utf-8 -*-
# Importando as bibliotecas
import pandas as pd
import pandas_datareader.data as pdr
import yfinance
import datetime
import fundamentos as fun
import dateutil
from datetime import datetime as dt
import pytz
import yfinance as yf
# Importar o selenium, o pandas, o datetime e o workalendar
from selenium import webdriver
import pandas as pd
from datetime import date, timedelta
from workalendar.america import Brazil
import time

# Ajustando o pandas_datareader com o yfinance
yfinance.pdr_override()
yfinance.set_tz_cache_location("custom/cache/location")

#Cria um DataFrame com todas as Empresas Listadas na B3
ticker = fun.get_tickers()
empresas = pd.DataFrame(ticker)
print(empresas)
Tickers = pd.DataFrame.drop(self=empresas,
                            columns={'Nome Comercial', 'Razão Social'})

Tickers.rename(columns= {'Papel':'Ticker'}, inplace=True)

print(Tickers)

# Definindo o símbolo da ação e o período desejado
data_inicial = []
data_final = []
simbolo = Tickers['Ticker']
data_final = datetime.date.today() - datetime.timedelta(days=1) # data de ontem
data_inicial = data_final - datetime.timedelta(days=7) # data de uma semana atrás

tz = pytz.timezone("America/Sao_Paulo")
# start = tz.localize(data_inicial)
# end = tz.localize(data_final)
# data_inicial = datetime.combine(data_inicial, dt.time())
# data_final = datetime.combine(data_final, dt.time())
semana_passada = data_inicial
ontem = data_final
#tickers = ['Tickers']
df = yf.download(Tickers, data_inicial, data_final, auto_adjust=True)


# Criar o driver do Chrome
driver = webdriver.Chrome()

# Acessar o site da B3
driver.get("https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/")
time.sleep(20)

# Encontrar os elementos das caixas de opção
# Em vez de usar driver.find_element_by_id("id")
By =[]
ano = driver.find_element(by=By.ID,
                          value="ctl00_contentPlaceHolderConteudo_AnoDropDownList")
mes = driver.find_element(by=By.ID,
                          value="ctl00_contentPlaceHolderConteudo_MesDropDownList")
dia = driver.find_element(by=By.ID,
                          value="ctl00_contentPlaceHolderConteudo_DiaDropDownList")

# Criar um objeto de calendário do Brasil
cal = Brazil()

# Obter a data de ontem
ontem = date.today() - timedelta(days=1)

# Verificar se a data de ontem é dia útil, caso contrário, subtrair um dia até que seja
while ontem.weekday() > 4 or cal.is_holiday(ontem):
    ontem = ontem - timedelta(days=1)

# Selecionar os valores de acordo com a data de ontem
ano.send_keys(str(ontem.year))
mes.send_keys(str(ontem.month))
dia.send_keys(str(ontem.day))

# Clicar no botão de download
botao = driver.find_element_by_id("ctl00_contentPlaceHolderConteudo_BuscarButton")
botao.click()

# # Obtendo os dados do Yahoo Finance
# df = pdr.get_data_yahoo(simbolo, data_inicial, data_final)

# Renomeando as colunas
df.rename(columns={"Open": "Abertura", "Close": "Fechamento"}, inplace=True)

# Criando uma coluna com o preço de abertura do dia anterior
df["Abertura_Anterior"] = df["Abertura"].shift(1)

# Criando uma coluna com o preço de fechamento do dia anterior
df["Fechamento_Anterior"] = df["Fechamento"].shift(1)

# Criando uma coluna com a variação entre o preço de abertura de ontem e o preço de abertura de uma semana atrás
df["Variacao_Abertura_Ontem_Abertura_Semana"] = df["Abertura_Anterior"] - df["Abertura"].shift(5)

# Criando uma coluna com a variação entre o preço de fechamento de ontem e o preço de abertura de uma semana atrás
df["Variacao_Fechamento_Ontem_Abertura_Semana"] = df["Fechamento_Anterior"] - df["Abertura"].shift(5)

# Criando uma função que retorna True se as variações forem positivas e False caso contrário
def comparar_precos(variacao_abertura, variacao_fechamento):
  if variacao_abertura > 0 and variacao_fechamento > 0:
    return True
  else:
    return False

#Cria Lista Vazia Para Evitar Erro De Não Definição De Parâmetro
resultado = []

# Aplicando a função na última linha do dataframe
if(resultado):
      try:
         resultado = comparar_precos(df["Variacao_Abertura_Ontem_Abertura_Semana"].iloc[-1], df["Variacao_Fechamento_Ontem_Abertura_Semana"].iloc[-1])
      except IndexError:
        print('Porra')


# Exibindo o resultado
print(resultado)
