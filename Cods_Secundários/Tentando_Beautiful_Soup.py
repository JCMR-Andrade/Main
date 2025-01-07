# -*- coding: utf-8 -*-


# Importar as bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
from time import sleep

def myClick(by, desc):
    wait = WebDriverWait(driver, 10)
    by = by.upper()
    if by == 'XPATH':
        wait.until(EC.element_to_be_clickable((By.XPATH, desc))).click()
    if by == 'ID':
        wait.until(EC.element_to_be_clickable((By.ID, desc))).click()
    if by == 'LINK_TEXT':
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, desc))).click()

# # Definir o URL da página de login do gov.br
url_login = "https://sso.acesso.gov.br/login"

# Definir o URL da página da CVM
url_cvm = "https://www.rad.cvm.gov.br/ENET/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento=124650&CodigoTipoInstituicao=1"

# Definir o seu CPF e senha do gov.br
cpf = "06757567903"
senha = "Wallabies1."

# Criar um objeto webdriver para controlar o navegador
# Você pode mudar o Chrome para o navegador que você preferir
driver = webdriver.Chrome()
# some global location
wait = WebDriverWait(driver, 10)

# Abrir a página de login do gov.br no navegador
driver.get(url_login)

# Esperar até que o elemento com o id do campo de CPF esteja presente na página
# Você pode mudar o tempo máximo de espera (10 segundos no exemplo)
element_cpf = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "accountId")))

# Preencher o campo de CPF com o seu CPF
element_cpf.send_keys(cpf)

time.sleep(5)

# Clicar no botão de avançar
wait.until(EC.element_to_be_clickable((By.ID, "enter-account-id"))).click()

time.sleep(5)

# Esperar até que o elemento com o id do campo de senha esteja presente na página
element_senha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "new-password")))

# Preencher o campo de senha com a sua senha
element_senha.send_keys(senha)

# Clicar no botão de entrar
WebDriverWait(driver, 15).until(EC.element_to_be_clickable("login-button-panel").click())

# Esperar até que a autenticação seja concluída
# Você pode mudar o tempo máximo de espera (10 segundos no exemplo)
WebDriverWait(driver, 10).until(EC.url_changes(url_login))

# Abrir a página da CVM no navegador
driver.get(url_cvm)

# Esperar até que o elemento com o id da tabela esteja presente na página
element_table = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "iFrameFormulariosFilho")))

# Obter o HTML da página
html = driver.page_source

# Fechar o navegador
# driver.quit()

# Criar um objeto BeautifulSoup para analisar o HTML
soup = BeautifulSoup(html, "html.parser")

# Encontrar a tabela que contém os dados financeiros
table = soup.find("ctl00$cphPopUp$hdnGuiaAtiva", id="aspnetForm")

# Extrair as linhas da tabela
rows = table.find_all("tr")

# Criar uma lista para armazenar os dados
data = []

# Percorrer cada linha da tabela
for row in rows:
    # Extrair as células da linha
    cells = row.find_all("td")

    # Criar uma lista para armazenar os valores da linha
    values = []

    # Percorrer cada célula da linha
    for cell in cells:
        # Extrair o texto da célula
        text = cell.get_text()

        # Remover os espaços em branco extras
        text = text.strip()

        # Adicionar o texto à lista de valores
        values.append(text)

    # Adicionar a lista de valores à lista de dados
    data.append(values)

# Criar um DataFrame do Pandas com os dados
df = pd.DataFrame(data)

# Exibir o DataFrame
print(df)
