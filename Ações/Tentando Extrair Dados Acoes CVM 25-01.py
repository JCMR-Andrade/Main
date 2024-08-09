# Importar os módulos necessários
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Obter o conteúdo HTML da página que contém a tabela
url = "https://www.rad.cvm.gov.br/ENET/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento=132254&CodigoTipoInstituicao=1"
response = requests.get(url)
html = response.text

# Criar um objeto BeautifulSoup, passando o conteúdo HTML e o nome do analisador
soup = BeautifulSoup(html, "html.parser")

# Encontrar a tabela com o id "ctl00_cphPopUp_tbDados"
table = soup.find(id="ctl00_cphPopUp_tbDados")

# Encontrar todas as linhas da tabela
rows = table.find_all("tr")

# Criar uma lista vazia para armazenar os dados da tabela
data = []

# Iterar sobre as linhas
for row in rows:
    # Encontrar todas as células da linha
    cells = row.find_all("td")
    # Criar uma lista vazia para armazenar os dados da linha
    row_data = []
    # Iterar sobre as células
    for cell in cells:
        # Extrair o texto da célula
        text = cell.text
        # Adicionar o texto à lista da linha
        row_data.append(text)
    # Adicionar a lista da linha à lista da tabela
    data.append(row_data)

# Criar uma lista com os nomes das colunas da tabela
columns = ["Conta", "Descrição", "31/03/2021", "31/12/2020", "30/09/2020", "30/06/2020", "31/03/2020"]

# Criar um dataframe a partir da lista da tabela, usando o método DataFrame do pandas
df = pd.DataFrame(data, columns=columns)

# Salvar o dataframe em um arquivo Excel, usando o método to_excel do pandas
df.to_excel("tabela.xlsx")
