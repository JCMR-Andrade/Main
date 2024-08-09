# -*- coding: utf-8 -*-
# Importar as bibliotecas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytesseract
import requests

# Criar um objeto webdriver para abrir o navegador
driver = webdriver.Chrome()

# Acessar o site
driver.get("https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/")

# Encontrar o elemento do formulário de login
login_form = driver.find_element_by_id("loginForm")

# Encontrar o elemento do campo de usuário
user_field = login_form.find_element_by_id("username")

# Digitar o usuário
user_field.send_keys("seu_usuario")

# Encontrar o elemento do campo de senha
password_field = login_form.find_element_by_id("password")

# Digitar a senha
password_field.send_keys("sua_senha")

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

# Obter o código fonte da página após o login
page_source = driver.page_source

# Imprimir o código fonte
print(page_source)
