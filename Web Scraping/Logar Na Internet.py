# -*- coding: utf-8 -*-
# Importando as bibliotecas
import pandas as pd
import yfinance
import datetime
import fundamentos as fun
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date, timedelta
from workalendar.america import Brazil
import pytesseract
import requests

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
simbolo = Tickers['Ticker']
yfinance.set_tz_cache_location("custom/cache/location")
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
# Obtendo os dados do Yahoo Finance
print('\nPegando Tickers e Gravando No DataFrame')
#df = pdr.get_data_yahoo(simbolo)#, data_inicial, data_final)
df = pd.DataFrame(Tickers['Ticker'])
print(df)
#df = yf.download(Tickers, data_inicial, data_final, auto_adjust=True)


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Criar o driver do Chrome
driver = webdriver.Chrome()

# Acessar o site da B3
driver.get("https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/")

# Esperar até que o elemento do iframe esteja presente e visível na página
iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='TrustArc Cookie Consent Manager']")))

# Mudar o contexto do driver para o iframe
driver.switch_to.frame(iframe)

# Encontrar os elementos das caixas de opção
ano = driver.find_element(By.ID, "ctl00_contentPlaceHolderConteudo_AnoDropDownList")
mes = driver.find_element(By.ID, "ctl00_contentPlaceHolderConteudo_MesDropDownList")
dia = driver.find_element(By.ID, "ctl00_contentPlaceHolderConteudo_DiaDropDownList")

# Selecionar os valores de acordo com a data de ontem
ano.send_keys(str(ontem.year))
mes.send_keys(str(ontem.month))
dia.send_keys(str(ontem.day))

# Encontrar o elemento do captcha
captcha_image = login_form.find_element_by_id("captcha")

# Obter o atributo src do captcha, que é a URL da imagem
captcha_url = captcha_image.get_attribute("src")

# Fazer uma requisição HTTP para obter a imagem do captcha
captcha_response = requests.get(captcha_url)

# Salvar a imagem do captcha em um arquivo temporário
with open("captcha.png", "wb") as f:
  f.write(captcha_response.content)

# Usar o pytesseract para converter a imagem do captcha em uma string de texto
captcha_text = pytesseract.image_to_string("captcha.png")

# Encontrar o elemento do campo de captcha
captcha_field = login_form.find_element_by_id("captchaText")

# Digitar o texto do captcha
captcha_field.send_keys(captcha_text)

# Encontrar o elemento do botão de login
login_button = login_form.find_element_by_id("loginButton")

# Clicar no botão de login
login_button.click()

# Aguardar alguns segundos para o site carregar
driver.implicitly_wait(10)
# Clicar no botão de download
botao = driver.find_element(By.ID, "ctl00_contentPlaceHolderConteudo_BuscarButton")
botao.click()

# Criar o driver do Chrome
driver = webdriver.Chrome()

# Acessar o site da B3
driver.get("https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/")

# Encontrar o elemento do iframe que contém as caixas de opção
iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title='TrustArc Cookie Consent Manager']")

# Mudar o contexto do driver para o iframe
driver.switch_to.frame(iframe)

# Encontrar os elementos das caixas de opção
ano = driver.find_element(By.ID, "ctl00_contentPlaceHolderConteudo_AnoDropDownList")
mes = driver.find_element(By.ID, "ctl00_contentPlaceHolderConteudo_MesDropDownList")
dia = driver.find_element(By.ID, "ctl00_contentPlaceHolderConteudo_DiaDropDownList")

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
botao = driver.find_element(By.ID, "ctl00_contentPlaceHolderConteudo_BuscarButton")
botao.click()

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
