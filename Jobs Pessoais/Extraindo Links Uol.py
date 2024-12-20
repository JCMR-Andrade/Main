# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Link da página que queremos extrair informações
link = "https://www.uol.com.br/"

# Faz a requisição HTTP para obter o conteúdo da página
requisicao = requests.get(link)

# Cria o objeto BeautifulSoup
soup = BeautifulSoup(requisicao.text, "html.parser")

# Encontra todos os elementos <p> com a classe "title__element"
titulos = soup.find_all("h3", class_=["headlineHorizontal", "title__element headlineMain__title",
                                               "headlineHorizontalAvatar__content", "container", "row",
                                               "headlineMain section__grid__main__highlight__item",
                                               "row section__grid__main", "sectionGrid__rows",
                                               "relatedList__container__item", "title__element headlineSub__content__title",
                                               "title__element titleBrand__title", "title_element",
                                               "col-24 col-lg-15", "relatedList headlineMain__related-list",
                                               "titleBrand headlinePhotoBrand__content__titleBrand"])

# Encontra todos os elementos <a> com a classe "hyperlink headlineHorizontal__link"
links = soup.find_all("a", class_= ["hyperlink headlineMain__link", "hyperlink headlineBrandPhoto__link",
                                    "hyperlink relatedList__related", "hyperlink headlineHorizontalBrand__link"])


# Cria listas vazias para os títulos e links
lista_titulos = []
lista_links = []

# Itera sobre os títulos e links correspondentes
for titulo, link in zip(titulos, links):

    nome = titulo.text.strip()
    url = link["href"]

    if nome not in lista_titulos:
        lista_titulos.append(nome)
        lista_links.append(url)
    else:
        pass

# Imprime os títulos e links na ordem correta
    for titulo, link in zip(lista_titulos, lista_links):
        print("Título:", titulo)
        print("Link:", link)
        print("-" * 30)


df = pd.DataFrame({"Títulos" : lista_titulos, "Link" : lista_links})
df.to_excel('Links.xlsx', index=False)
print(df)
