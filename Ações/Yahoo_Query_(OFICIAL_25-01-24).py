#YAHOO QUERY AGORA VAI?
import pandas as pd
from yahooquery import Ticker
import pandas as pd
import yfinance as yf
import datetime
from typing import Dict, List, Union
import pandas as pd
import yfinance as yf

lista = ["PETR3.SA",
        "EMBR3.SA",
        "DXCO3.SA",
        "WEGE3.SA",
        "CYRE3.SA",
        "MULT3.SA",
        "ALSO3.SA",
        "EZTC3.SA",
        "MRVE3.SA",
        "SMTO3.SA",
        "PCAR3.SA",
        "ABEV3.SA",
        "BEEF3.SA",
        "LREN3.SA",
        "JBSS3.SA",
        "MGLU3.SA",
        "NTCO3.SA",
        "ARZZ3.SA",
        "HYPE3.SA",
        "BRFS3.SA",
        "MRFG3.SA",
        "VIIA3.SA",
        "ALPA4.SA",
        "BBDC3.SA",
        "CIEL3.SA",
        "BBAS3.SA",
        "BBDC4.SA",
        "ITUB4.SA",
        "B3SA3.SA",
        "BRKM5.SA",
        "UGPA3.SA",
        "PETR3.SA",
        "VBBR3.SA",
        "PRIO3.SA",
        "RAIZ4.SA",
        "HAPV3.SA",
        "RADL3.SA",
        "FLRY3.SA",
        "RDOR3.SA",
        "TOTS3.SA",
        "LWSA3.SA",
        "TIMS3.SA",
        "VIVT3.SA",
        "CMIG4.SA",
        "EQTL3.SA",
        "EGIE3.SA",
        "SBSP3.SA",
        "ELET3.SA",
        "ELET6.SA",
        "CPFE3.SA",
        "CPLE6.SA",
        "ENEV3.SA",
        "CVCB3.SA",
        "CMIN3.SA",
        "COGN3.SA",
        "CSAN3.SA",
        "SLCE3.SA",
        "YDUQ3.SA",
        "ASAI3.SA",
        "PETZ3.SA",
        "RRRP3.SA",
        "CRFB3.SA",
        "CASH3.SA"
]

def get_stocks(
                acoes: Union[List[str], str],
                data_inicio: str,
                data_fim: str,
                proxy: Union[Dict[str, str], None] = None,
                ) -> pd.DataFrame:
    # """Função para capturar dados de Ações ou Índices Listados.
    # """
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
    

acoes = get_stocks(acoes=f'{input(str("Qual Empresa Gostaria de Consultar?"))}',
                   data_inicio=f'{input(str("Qual a Data Inicial Gostaria de Consultar?"))}',
                   data_fim=f'{input(str("Qual a Data Final Gostaria de Consultar?"))}'
                   
)
print(acoes, '01')


petr = Ticker(acoes)
TickerS = pd.DataFrame(petr.history(start="2023-12-01", end="2023-12-31"))

df = TickerS
dados = Ticker(acoes)     # Coleta dados
dados = dados.income_statement()# Chama Demonstração de resultados
dados = dados.transpose()            # Transpõe a matriz
dados.columns = dados.iloc[0,:] # Renomeia colunas
dados = dados.iloc[2:,1:]       # Seleciona dados
dados = dados.iloc[:, 1::-1]    # Inverte colunas
dados
print(dados, '02')

# Criar um dataframe com as informações dos dois dataframes
df_final = pd.merge(acoes, dados, left_index=True, right_index=True, how="inner")

# Imprimir o dataframe final (É O COMPLETO COM DATAS E DRE PUBLICADO)
print(df_final, '03')

# Definindo o símbolo da ação e o período desejado
simbolo = lista
yf.set_tz_cache_location("custom/cache/location")
data_final = datetime.date.today() - datetime.timedelta(days=1) # data de ontem
data_inicial = data_final - datetime.timedelta(days=7) # data de uma semana atrás

# Renomeando as colunas
TickerS.rename(columns={'open': 'Abertura', 'close': 'Fechamento',
                        'symbol' : 'Ticker',
                        'date' : 'Data',
                       	'high' : 'Maior Valor Neg.',
                       	'low' : 'Menor Valor Neg.',
                        'volume' : 'Volume',
                        'adjclose' : 'Adj. Fecham.',
                        'dividends' : 'Dividendos',
                        'splits' : 'Splits'
}, inplace=True)

# Criando uma coluna com o preço de abertura do dia anterior
TickerS["Abertura_Anterior"] = TickerS["Abertura"].shift(1)

# Criando uma coluna com o preço de fechamento do dia anterior
TickerS["Fechamento_Anterior"] = TickerS["Fechamento"].shift(1)

# Criando uma coluna com a variação entre o preço de abertura de ontem e o preço de abertura de uma semana atrás
TickerS["Variacao_Abertura_Ontem_Abertura_Semana"] = TickerS["Abertura_Anterior"] - TickerS["Abertura"].shift(6)

# Criando uma coluna com a variação entre o preço de fechamento de ontem e o preço de abertura de uma semana atrás
TickerS["Variacao_Fechamento_Ontem_Abertura_Semana"] = TickerS["Fechamento_Anterior"] - TickerS["Abertura"].shift(6)

#Cria Lista Vazia Para Evitar Erro De Não Definição De Parâmetro
print (TickerS, '04')
resultado = []

resultado = 0

# Criando uma função que retorna True se as variações forem positivas e False caso contrário
def comparar_precos(variacao_abertura, variacao_fechamento):
  if variacao_abertura > 0 and variacao_fechamento > 0:
    # Você não precisa usar self para referenciar o objeto TickerS, basta usar o seu nome
    TickerS.variacao_abertura = 'Variacao_Abertura_Ontem_Abertura_Semana'
    TickerS.variacao_fechamento = 'Variacao_Fechamento_Ontem_Abertura_Semana'
    # Você precisa retornar o valor de resultado + 1, não apenas resultado
    return resultado + 1
  else:
    return False
  
print(resultado)  

# Aplicando a função na última linha do dataframe
if(resultado):
      try:
         resultado = comparar_precos(df["Variacao_Abertura_Ontem_Abertura_Semana"].iloc[-1], df["Variacao_Fechamento_Ontem_Abertura_Semana"].iloc[-1])
      except IndexError:
        print('Porra')
       

# Exibindo o resultado
print(resultado, '06')

# # Criar um dataframe vazio para armazenar os dados das ações
df_acoes = pd.DataFrame(columns=["Ticker", "Abertura", "Fechamento", "variacao_fechamento"])
lista_acoes = [TickerS]


# Criar um arquivo CSV com os dados das ações
df_acoes.to_csv("acoes_ontem.csv", index=False)

# Criar outro dataframe vazio para armazenar os dados das ações que atendem à condição
df_condicao = pd.DataFrame(columns=["TICKER", "ABERTURA", "FECHAMENTO"])

TickerS1 = pd.DataFrame(TickerS)
# Verificar se a condição é verdadeira
condicao = (TickerS["Abertura_Anterior"] < TickerS["Variacao_Fechamento_Ontem_Abertura_Semana"]) & (TickerS["Fechamento_Anterior"] > TickerS["Variacao_Abertura_Ontem_Abertura_Semana"])

# Filtrar o dataframe usando a condição
TickerS1 = TickerS[condicao].dropna()
# Criar um dataframe com as informações dos dois dataframes
df_final1 = pd.merge(TickerS1, dados, left_on='symbol', right_index=True)

print(df_final1, '10')

def fim():

    try:
        
        
        # Verificar se a condição é verdadeira
        if TickerS["Abertura_Anterior"] < TickerS["Variacao_Fechamento_Ontem_Abertura_Semana"].any() and \
        TickerS["Fechamento_Anterior"] > TickerS["Variacao_Abertura_Ontem_Abertura_Semana"].any():
            # Adicionar uma nova linha ao dataframe com os dados da ação
            TickerS1 = TickerS1.append({"TICKER": petr, "ABERTURA": TickerS["Abertura_Anterior"],
                                               "FECHAMENTO": TickerS["Fechamento_Anterior"],
                                                                      "Variacao Fechamento": resultado}, ignore_index=True)
            TickerS1 = pd.DataFrame(TickerS)
            TickerS1 = TickerS1.insert(column='Ticker')
            
    except ValueError:        #Serve para evitar que de Erro por causa das células em branco!
        print('Erro?!?!')

# Criar outro arquivo CSV com os dados das ações que atendem à condição
df_condicao = pd.DataFrame(TickerS)
df_valido = pd.DataFrame(df_condicao)
df_condicao2 = pd.DataFrame(df_condicao)
comparar_precos2 = pd.DataFrame(df_valido)

# Criar uma variável para o número do arquivo
agora = datetime.datetime.now().strftime("%Y%m%d__%H_%M_%S")

Arquivo =f"C:\\User\s\HP\\Documents\Python Scripts\\PythoN\\B3\\Ações\\EmpresasABR "+ str({agora}) +".csv"

#Arquivo=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\df_condicao2.csv"
TickerS.to_csv(Arquivo, sep=';',decimal=',',index=True,encoding="latin1")

fim()

# Para cada ação no dataframe, obter os preços de abertura e fechamento da semana passada
# for index, row in df_acoes.iterrows():
#     # Definir o ticker da ação
#     ticker = row["TICKER"]

#     # Definir a URL para obter os dados históricos da ação


#     # Verificar se há dados disponíveis para a data da ***semana passada***
#     if dados_historico["result"] != []:
#         # Obter os preços de abertura e fechamento da semana passada
#         abertura_sp = dados_historico["result"][0]["preabe"]
#         fechamento_sp = dados_historico["result"][0]["preult"]

#         # Obter os preços de abertura e fechamento de ontem
#         abertura_o = row["ABERTURA"]
#         fechamento_o = row["FECHAMENTO"]


# Para cada ação na lista, obter os preços de abertura e fechamento de ontem
#for acao in lista_acoes:
    # Definir o ticker da ação
    #ticker = column['Ticker']

    # # Definir a URL para obter os dados históricos da ação
  

    # Verificar se há dados disponíveis para a data de ontem
    # if dados_historico["result"] != []:
    #     # Obter os preços de abertura e fechamento de ontem
    #     abertura = dados_historico["result"][0]["preabe"]
    #     fechamento = dados_historico["result"][0]["preult"]

        # Adicionar uma nova linha ao dataframe com os dados da ação
#df_acoes = df_acoes.append({"TICKER": petr, "ABERTURA": TickerS["Abertura"], "FECHAMENTO": TickerS["Fechamento"]}, ignore_index=True)

