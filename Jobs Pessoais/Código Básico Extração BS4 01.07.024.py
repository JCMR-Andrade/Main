# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(soup, quotes):
# recuperando todos os elementos HTML <div> de citação na página
    elementos_de_citacao = soup.find_all('div', class_='quote')

# iterando sobre a lista de elementos de citação
# para extrair os dados de interesse e armazená-los
# na lista de citações
    for elemento_de_citacao in elementos_de_citacao:
        # extraindo o texto da citação
        texto = elemento_de_citacao.find('span', class_='text').text
        # extraindo o autor da citação
        autor = elemento_de_citacao.find('small', class_='author').text

        # extraindo os elementos HTML <a> relacionados à citação
        elementos_de_tag = elemento_de_citacao.find('div', class_='tags').find_all('a', class_='tag')

        # armazenando a lista de strings de tags em uma lista
        tags = []
        for elemento_de_tag in elementos_de_tag:
            tags.append(elemento_de_tag.text)

        # adicionando um dicionário contendo os dados da citação
        # em um novo formato à lista de citações
        quotes.append(
            {
                'text': texto,
                'author': autor,
                'tags': ', '.join(tags)  # mesclando as tags em uma string "A, B, ..., Z"
            }
        )

# a URL da página inicial do site de destino
base_url = 'https://quotes.toscrape.com'

# definindo o cabeçalho User-Agent para usar na solicitação GET abaixo
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# recuperando a página da web de destino
pagina = requests.get(base_url, headers=headers)

# analisando a página da web de destino com Beautiful Soup
soup = BeautifulSoup(pagina.text, 'html.parser')

# inicializando a variável que conterá
# a lista de todos os dados de citação
citas = []

# raspando a página inicial
scrape_page(soup, citas)

# obtendo o elemento HTML "Next →"
elemento_next_li = soup.find('li', class_='next')

# se houver uma próxima página para raspar
while elemento_next_li is not None:
    proxima_url_relativa = elemento_next_li.find('a', href=True)['href']

    # obtendo a nova página
    pagina = requests.get(base_url + proxima_url_relativa, headers=headers)

    # analisando a nova página
    soup = BeautifulSoup(pagina.text, 'html.parser')

    # raspando a nova página
    scrape_page(soup, citas)

    # procurando o elemento HTML "Next →" na nova página
    elemento_next_li = soup.find('li', class_='next')

# lendo o arquivo "quotes.csv" e criando-o
# se não estiver presente
arquivo_csv = open('quotes.csv', 'w', encoding='utf-8', newline='')

# inicializando o objeto de gravação para inserir dados
# no arquivo CSV
escritor = csv.writer(arquivo_csv)

# escrevendo o cabeçalho do arquivo CSV
escritor.writerow(['Texto', 'Autor', 'Tags'])

# escrevendo cada linha do CSV
for citacao in citas:
    escritor.writerow(citacao.values())

# encerrando a operação e liberando os recursos
arquivo_csv.close()
