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
from selenium.webdriver.common.action_chains import ActionChains # Importar a classe ActionChains
from selenium.webdriver.common.keys import Keys

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
# url_login = "https://sso.acesso.gov.br/login"

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

# Abrir a página da CVM no navegador
driver.get(url_cvm)

# Obter o HTML da página
html = driver.page_source

# Criar um objeto BeautifulSoup para analisar o HTML
soup = BeautifulSoup(html, "html.parser")

# Esperar até que o elemento com o id da tabela esteja presente na página
# Clicar no botão de avançar
wait.until(EC.element_to_be_clickable((By.ID, "btnGeraRelatorioPDF"))).click()


# Clicar no segundo botão na janela da PopUp
wait.until(EC.element_to_be_clickable((By.ID, "btnConsulta"))).click()

# Mudar o foco para o frame que contém o botão Gerar PDF
driver.switch_to.frame("iFrameFormulariosFilho")

# Clicar no botão que abre o popout
wait.until(EC.element_to_be_clickable((By.ID, "btnGeraRelatorioPDF"))).click()

# Fechar o navegador
# driver.quit()


# # Importar as bibliotecas necessárias
# from selenium import webdriver

# # Criar um objeto webdriver para controlar o navegador
# driver = webdriver.Chrome()

# # Abrir a página da CVM no navegador
# driver.get("https://www.rad.cvm.gov.br/ENET/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento=124650&CodigoTipoInstituicao=1")

# #Guardar o identificador da janela atual
# window_before = driver.current_window_handle

# # Obter o identificador da janela da PopUp
# window_after = driver.window_handles[1]

# # Mudar o foco para a janela da PopUp
# driver.switch_to.window(window_after)



# # Criar um objeto ActionChains, passando o driver como argumento
# actions = ActionChains(driver)

# # Adicionar uma ação de mover o mouse para o elemento do botão Gerar PDF
# actions.move_to_element(button)

# # Adicionar uma ação de clicar no elemento do botão Gerar PDF
# actions.click()

# # Adicionar uma ação de pressionar a tecla Control
# actions.key_down(Keys.CONTROL)

# # Adicionar uma ação de pressionar a tecla S
# actions.send_keys(Keys.S)

# # Adicionar uma ação de soltar a tecla Control
# actions.key_up(Keys.CONTROL)

# # Executar a sequência de ações
# actions.perform()
 # Encontrar a tabela que contém os dados financeiros
# table = soup.find(id="ctl00_cphPopUp_dgDocumentos")

# # Encontrar o cabeçalho da tabela
# thead = table.find(name="thead")

# # Extrair as células do cabeçalho
# th_cells = thead.find_all(name="th")

# # Criar uma lista para armazenar os nomes das colunas
# columns = []

# # Percorrer cada célula do cabeçalho
# for cell in th_cells:
#     # Extrair o texto da célula
#     text = cell.get_text()

#     # Remover os espaços em branco extras
#     text = text.strip()

#     # Adicionar o texto à lista de colunas
#     columns.append(text)

# # Encontrar o corpo da tabela
# tbody = table.find(name="tbody")

# # Extrair as linhas do corpo da tabela
# rows = tbody.find_all(name="tr")

# # Criar uma lista para armazenar os dados
# data = []

# # Percorrer cada linha do corpo da tabela
# for row in rows:
#     # Extrair as células da linha
#     cells = row.find_all(name="td")

#     # Criar uma lista para armazenar os valores da linha
#     values = []

#     # Percorrer cada célula da linha
#     for cell in cells:
#         # Extrair o texto da célula
#         text = cell.get_text()

#         # Remover os espaços em branco extras
#         text = text.strip()

#         # Adicionar o texto à lista de valores
#         values.append(text)

#     # Adicionar a lista de valores à lista de dados
#     data.append(values)

# # Criar um DataFrame do Pandas com os dados e as colunas
# df = pd.DataFrame(data, columns=columns)

# Exibir o DataFrame
# print(df)
