import pandas as pd
import pymysql

# Configurações da conexão
host = 'localhost'
user = 'root'
password = 'Saddan.07'
database = 'DadosDota_Trends'

# Crie uma conexão
connection = pymysql.connect(host=host, user=user, password=password, database=database)

df3 = pd.read_sql('SELECT * FROM trends where Posição_da_Semana < 15 AND PickRate >= 10 ORDER BY Posição_da_Semana' , connection)
print(df3)