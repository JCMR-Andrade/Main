# -*- coding: utf-8 -*-
'''Passo 2: Importando as Bibliotecas Necessárias
Em seguida, importamos as bibliotecas BeautifulSoup e Requests instaladas no passo anterior.'''
import requests
from bs4 import BeautifulSoup
import csv

'''Passo 3: Obtendo o Conteúdo da Página
Para coletar dados de uma página web, precisamos obter o conteúdo HTML da página.
Usando a biblioteca Requests, fazemos uma requisição HTTP à página desejada.'''
url = "https://www.dadosaocubo.com/"
response = requests.get(url)

if response.status_code == 200:
	html_content = response.text
else:
	print("Erro ao acessar a página.")
	exit()

# print(html_content, end="")
'''Passo 4: Extraindo os Dados com BeautifulSoup
Agora que temos o conteúdo HTML da página, podemos usar a biblioteca BeautifulSoup
para extrair os dados específicos que desejamos coletar. Vamos supor que queremos coletar o título e o link de cada publicação.'''
soup = BeautifulSoup(html_content, "html.parser")

posts = soup.find_all("div", class_="feat-item")

for post in posts:
  name = post.find("h2", class_="entry-title").text.strip()
  link = post.find("a")['href']
  print("Post:", name)
  print("Link:", link)
  print("-" * len("Link"+link))


'''Passo 5: Armazenando os Dados
Por fim, você pode armazenar os dados coletados em um arquivo CSV, Excel ou banco de dados para futuras análises. Confere o código Python abaixo.'''
with open("dados_coletados.csv", 'w', newline='', encoding='latin1') as csvfile:
  fieldnames = ["Post", "Link"]
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
  writer.writeheader()
  for post in posts:
    name = post.find("h2", class_="entry-title").text.strip()
    link = post.find("a")['href']
    writer.writerow({"Post": name, "Link": link})


