# -*- coding: utf-8 -*-

"""Função para capturar dados de Ações ou Índices Listados.
"""
#YAHOO QUERY AGORA VAI?
import pandas as pd
from yahooquery import Ticker
import pandas as pd
import pandas_datareader.data as pdr
import yfinance as yf
import mplfinance as mpf
import warnings
from typing import Dict, List, Tuple, Union
from datetime import date, datetime
import pandas as pd

warnings.filterwarnings('ignore')

def get_stocks(
                acoes: Union[List[str], str],
                data_inicio: str,
                data_fim: str,
                proxy: Union[Dict[str, str], None] = None,
                ) -> pd.DataFrame:
    """Função para capturar dados de Ações ou Índices Listados.
    """
    df1 = pd.DataFrame()
    if isinstance(acoes, list):
        for st in acoes:
            if not st.endswith(".SA"): st = st+".SA"
            if proxy:
                df = yf.download(st, start=data_inicio, end=data_fim, proxy=proxy)
            else:
                df = yf.download(st, start=data_inicio, end=data_fim)
            df1 = pd.concat([df, df1], axis=1)
    else:
        if not acoes.endswith(".SA"): acoes = acoes+".SA"
        if proxy:
            df1 = yf.download(acoes, start=data_inicio, end=data_fim, proxy=proxy)
        else:
            df1 = yf.download(acoes, start=data_inicio, end=data_fim)
    df1.index = pd.to_datetime(df1.index)
    return df1
    

Tkr = input(str('Digite a Empresa: '))
Ini = input(str('Digite a Data de Início da Busca: '))
Fim = input(str('Digite a Data de Término da Busca: '))
#Fim = Fim1.strftime('%Y-%m-%d')
acoes = get_stocks(acoes=f'{Tkr}',
                   data_fim=f'{Fim}',
                   data_inicio=f'{Ini}')

print(acoes)
mpf.plot(acoes, type='renko', style='mike', volume=True,  mav=(20, 200))

# Salvar o dataframe df_novo em um arquivo CSV
Arq =f"C:\\Users\\HP\\Documents\\Python Scripts\\PythoN\\B3\\Ações\\Preços Empresa " + str(Tkr).upper() + ".csv"
acoes.to_csv(Arq, sep=';',decimal=',',index=True,encoding="utf-8")
"""
#Extraindo Dados Diários, Iniciando Dia 0, Já Que o Período Está MAX

petr = Ticker("PETR4.SA”)
petr.history(period="max")
"""

"""
#Consultar um intervalo de tempo específico, adicionando datas de início e fim aos parâmetros:
petr = Ticker("PETR4.SA")
petr.history(start="2005–05–01", end="2013–12–31")

"""

"""Extraindo dados intraday, Extraindo intervalos de 30 min, Extraindo intervalos de 1 minuto:

abev = Ticker("ABEV3.SA")
abev.history(period="60d",  interval = "30m")

abev = abev.history(period="7d",  interval = "1m")
abev
"""

'''#extrair dados financeiros para análise fundamentalista. Para isso, são retornados os principais indicadores
#presentes nos relatórios anuais das empresas, tais como receita, lucro, Ebit, gastos com pesquisa e inovação, etc.

petr = Ticker("PETR4.SA")     # Coleta dados
petr = petr.income_statement()# Chama Demonstração de resultados
petr = transpose()            # Transpõe a matriz
petr.columns = petr.iloc[0,:] # Renomeia colunas
petr = petr.iloc[2:,1:]       # Seleciona dados
petr = petr.iloc[:, 1::-1]    # Inverte colunas
petr

'''