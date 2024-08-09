# -*- coding: utf-8 -*-
import pygwalker as pyg
import pandas as pd
import duckdb
import datetime as dt
import numpy as np


df = pd.read_csv('C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Área de Trabalho\\Estudos STFIM\\bbce_registros 01-01-2020___17-01-2024 - Copia.csv', sep=';')
nmp = df.to_numpy()

#Imprimir Nome Das Colunas Para Poder Convertê-las Em Numeric
print(df.columns)

# #Antes de Converter Os Valores, É Necessário Tirar Pontos, Vírgulas e R$ Caso Não Venham Como Texto Da Planilha

# df['    Open    '] = df['    Open    '].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True)
# df['    High    '] = df['    High    '].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True)
df['Valor'] = df['Valor'].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True)
# df['    Close    '] = df['    Close    '].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True)
# df['      Adj Close      '] = df['      Adj Close      '].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True)
# df['    Volume    '] = df['    Volume    '].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True)

#Converte a Data no Formato de Data
df['Data / Hora'] = pd.to_datetime(df['Data / Hora'], dayfirst=True) # usar dayfirst=True

# Então Convertemos As Colunas Para Números Com PD.TO_NUMERIC e ignora os Errors

df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
df['MWh'] = pd.to_numeric(df['MWh'], errors='coerce')
df['MWm'] = pd.to_numeric(df['MWm'], errors='coerce')
# df['    Close    '] = pd.to_numeric(df['    Close    '], errors='coerce')
# df['      Adj Close      '] = pd.to_numeric(df['      Adj Close      '], errors='coerce')
# df['    Volume    '] = pd.to_numeric(df['    Volume    '], errors='coerce')



# #Roda o BI
pyg.walk(df,
         use_kernel_calc=False,         # Set `True`, pygwalker will use duckdb as computing engine, it support you explore bigger dataset(<=100GB).
         hideDataSourceConfig=True,    # Hide DataSource import and export button (True) or not (False). Default to True
         themeKey='vega',              # Theme type.
         dark='media',                 # Auto detect OS theme.
         store_chart_data=True         # Whether to save chart to disk, only work when spec is json file, Default to False.
)  