import pandas as pd
from requests_html import HTMLSession
import datetime as dt
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import requests_html as html

# Crie uma sessão HTML
session = HTMLSession()

# Faça uma requisição à URL da página
url = "https://www.dotabuff.com/heroes?show=heroes&view=winning&mode=all-pick&date=7d"
response = session.get(url)


# Encontre o elemento da tabela usando seletores CSS
table_selector = "table.tw-w-full"  # Substitua pelo seletor correto
table = response.html.find(table_selector, first=True)
print(table)

# Inicialize listas vazias para armazenar os dados, se atentar para criar uma lista por item a ser extraído
hero_names = []
win_rates = []
pick_rates = []
kdas = []

# Extraia os dados da tabela
for row in table.find("tr"):    #TR se refere à LINHA praticamente em TODOS os HTML, creio que seja padrão boa-conduta
    cells = row.find("td")      #TD se refere ao CONTEÚDO DA CÉLULA em TODOS os HTML, boa-conduta maybe?
    if cells:
        hero_name = cells[0].text
        win_rate = float(cells[1].text.strip('%').replace(',', '.'))
        pick_rate = float(cells[2].text.strip('%').replace(',', '.'))
        kda = float(cells[3].text)

        # Adicione os valores às listas
        hero_names.append(hero_name)
        win_rates.append(win_rate)
        pick_rates.append(pick_rate)
        kdas.append(kda)

# Crie o DataFrame, através de um Dicionário cadastrando cada LISTA com uma coluna e deixando por ORDEM de Herói
df = pd.DataFrame({
    "Herói": hero_names,
    "WinRate": win_rates,
    "PickRate": pick_rates,
    "KDA": kdas
}).sort_values(by='Herói')

# Redefina o índice para torná-lo uma coluna, caso contrário não é possível criar a coluna da POSIÇÂO SEMANAL
df = df.reset_index()

# Renomeie a coluna do índice para "Posição Da Semana", por isso RESETAMOS anteriormente
df = df.rename(columns={'index': 'Posição_da_Semana'})

# Criamos outro Frame para adicionar e ordenar as colunas da forma mais apropriada
df2 = pd.DataFrame(df, columns=['Herói',
                                'Posição_da_Semana',
                                'WinRate',
                                'PickRate',
                                'KDA'
                                ]
)

print(df2)
# Criamos a variável do DIA em que foi extraído as informações para eventual comparação
dia = dt.datetime.today().strftime("%Y-%m-%d")

#Adicionamos a coluno nova no Dataframe
df2['Dt_Load'] = dia
df2['Dt_Load'] = df2['Dt_Load']
# Configurações da conexão
host = 'localhost'
user = 'root'
password = 'Saddan.07'
database = 'DadosDota_Trends'

# Crie uma conexão
connection = pymysql.connect(host=host, user=user, password=password, database=database)

# Convertemos a coluna DT_LOAD para data evitando conflito no momento de adicionar o valor
df2['Dt_Load'] = df2['Dt_Load'].astype(dtype='datetime64[us]')

# Criamos o ENGINE para fornecer as informações de conexão com o MYSQL
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

# Finalizamos adicionando o DataFrame alterado na tabela TRENDS, adicionando com APPEND e o INDEX é Falso para utilizar ele mesmo como Coluna
df2.to_sql('trends', con=engine, if_exists='append', index=False, index_label='Herói')

# alter = pd.read_sql('SELECT CONVERT(VARCHAR, Dt_Load, 23) AS data_convertida FROM trends', connection)

resul = pd.read_sql('SELECT * From trends ORDER BY Herói, Dt_Load', connection)
print(resul)
# def mysql_connection(host, user, passwd, database=None):
#     connection = connect(
#         host = host,
#         user = user,
#         passwd = passwd,
#         database = database
#     )
#     return connection

# connection = mysql_connection('localhost', 'root', 'Saddan@07', 'DadosDota_Trends')


# # '''
# cursor = connection.cursor()
# posicao = df2['Posição_da_Semana']

# # Convertemos as colunas numéricas
# df2['Posição_da_Semana'] = df2['Posição_da_Semana'].apply(str)
# df2['Win Rate(%)'] = df2['Win Rate(%)'].apply(str)
# df2['Pick Rate(%)'] = df2['Pick Rate(%)'].apply(str)
# df2['KDA'] = df2['KDA'].apply(str)

