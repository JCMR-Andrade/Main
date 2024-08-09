# Importar as bibliotecas necessárias
import requests
from bs4 import BeautifulSoup
from xlsxwriter import Workbook

# Definir o link do site que contém as tabelas
site = "https://www.guia-informatica.com/copie-uma-tabela-de-um-site-para-o-excel-mantendo-a-formatacao/"

# Obter o código HTML do site usando requests
response = requests.get(site)
html = response.text

# Criar um objeto BeautifulSoup para analisar o HTML
soup = BeautifulSoup(html, "html.parser")

# Encontrar todas as tags <table> no HTML
tables = soup.find_all("table")

# Criar um objeto Workbook do ExcelWriter
workbook = Workbook("tabelas.xlsx")

# Iniciar um contador para gerar nomes de planilhas
counter = 1

# Percorrer cada tabela encontrada
for table in tables:
    # Criar uma planilha com o nome "Tabela X", onde X é o valor do contador
    worksheet = workbook.add_worksheet(f"Tabela {counter}")
    # Incrementar o contador
    counter += 1
    # Iniciar as coordenadas da célula onde a tabela será escrita
    row = 0
    col = 0
    # Percorrer cada linha da tabela
    for tr in table.find_all("tr"):
        # Percorrer cada célula da linha
        for td in tr.find_all(["td", "th"]):
            # Obter o texto da célula
            text = td.get_text()
            # Escrever o texto na célula correspondente da planilha
            worksheet.write(row, col, text)
            # Avançar para a próxima coluna
            col += 1
        # Avançar para a próxima linha e reiniciar a coluna
        row += 1
        col = 0
# Fechar o arquivo do Excel
workbook.close()
