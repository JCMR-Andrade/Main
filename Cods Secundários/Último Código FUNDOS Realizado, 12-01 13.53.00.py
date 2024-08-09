# -*- coding: utf-8 -*-

# Último Código Realizado, Sem As Barras de Evolução

import datetime as dt
import comparar_fundos_br as comp
import pandas as pd
import time
import warnings
from typing import Any, List, Tuple, Union
import numpy as np
import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np
import sys

informe_diario_fundos_historico = comp.get_brfunds(anos=range(2022,2024), #somente 2021
                                              meses=range(1,2), #somente Jan e Fev,
                                              classe=["Fundo Multimercado"])


# Criando um dataframe com uma coluna de nomes
df = pd.DataFrame(informe_diario_fundos_historico)

print(df.isnull().any())

# Definindo a função que calcula a rentabilidade dos fundos
def rent_fundos(
    dados_fundos_cvm: pd.DataFrame,
    ) -> pd.DataFrame:
    # Copiando o dataframe original para evitar alterações indesejadas
    copia = dados_fundos_cvm.copy()
    
    # Identificando os valores nulos, NaN ou infinitos no dataframe copia
    print(copia.isnull().any())

# Removendo as linhas que contêm valores nulos, NaN ou infinitos
    copia = copia.dropna()
# Ou substituindo os valores nulos, NaN ou infinitos por zero
    copia = copia.fillna(0)
    print(copia.columns.tolist())

    Arvo=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\{dt.datetime.now().strftime('%Y-%m-%d')} SIM (InformeFundos).csv"
    copia.to_csv(Arvo, sep=';',decimal=',',index=True,encoding="latin1")

    # Usando o método where para encontrar o valor 3.13 na coluna Comum
    copia1 = df.where(df == '2022-01-03')
    # Removendo as linhas com NaN
    copia1 = copia1.dropna()
# # Obtendo o índice da linha
    posicao = copia1.index[:]
# # Imprimindo a posição
    print(posicao, 'PRINT 04')

    # Imprimindo o resultado
    print(copia1, 'PRINT 05')

    # Encontra Qual Valor Está Na "Linha", "Coluna"
    copia = df.iloc[:]
    print(copia, '<--- PRIMEIRO ITEM DA PRIMEIRA LINHA')

#Converte para DFrame
    copia2 = pd.DataFrame(copia)

#Imprime o Arquivo
    
    Arvo=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\{dt.datetime.now().strftime('%Y-%m-%d')} DF_1 (InformeFundos).csv"
    copia2.to_csv(Arvo, sep=';',decimal=',',index=True,encoding="latin1")

    # Usando o método pivot_table para criar um dataframe com o valor da quota e do patrimônio líquido por data e por fundo

    fundo_acoes_filtrado_transformed = copia.pivot_table(columns=["DT_COMPTC", "CNPJ - Nome", "CLASSE","NR_COTST",
    "VL_PATRIM_LIQ","VL_QUOTA"], values=["DT_COMPTC", "CNPJ - Nome", "VL_QUOTA", "VL_PATRIM_LIQ"]
    )
    # Criando um dataframe com as colunas 'DT_COMPTC', 'Fundo' e 'CLASSE'
    df_classe = copia[['DATA DE REFERENCIA','CNPJ - Nome', 'CLASSE']]
    
    # Criando um dataframe com as colunas 'DT_COMPTC', 'Fundo' e 'VL_QUOTA'
    df_quota = copia[['DATA DE REFERENCIA','CNPJ - Nome', 'VL_QUOTA']]
    
    # Criando um dataframe com as colunas 'DT_COMPTC', 'Fundo' e 'NR_COTST'
    df_cotst = copia[['DATA DE REFERENCIA','CNPJ - Nome', 'NR_COTST']]
    
    # Criando um dataframe com as colunas 'DT_COMPTC', 'Fundo' e 'VL_PATRIM_LIQ'
    df_patrim = copia[['DATA DE REFERENCIA','CNPJ - Nome', 'VL_PATRIM_LIQ']]
    
    # Calculando as outras colunas que você quer
    
    # Convertendo o índice do dataframe para o tipo datetime
    fundo_acoes_filtrado_transformed.index = pd.to_datetime(fundo_acoes_filtrado_transformed.index)
    
    # Ordenando o dataframe pela data
    fundo_acoes_filtrado_transformed = fundo_acoes_filtrado_transformed.sort_index()
    
    # Calculando as cotas normalizadas, dividindo o valor da quota de cada data pelo valor da quota da primeira data
    cotas_normalizadas = (fundo_acoes_filtrado_transformed["VL_QUOTA"]/ fundo_acoes_filtrado_transformed["VL_QUOTA"].iloc[0])
    # Calculando a rentabilidade diária dos fundos, usando a variação percentual do valor da quota
    rentabilidade_fundos_diaria = fundo_acoes_filtrado_transformed["VL_QUOTA"].pct_change()
    # Calculando a rentabilidade acumulada dos fundos, usando o produto cumulativo da rentabilidade diária mais um
    rentabilidade_fundos_acumulada = (1 + rentabilidade_fundos_diaria).cumprod() - 1
    # Calculando a rentabilidade total dos fundos, usando o último valor da rentabilidade acumulada
    rentabilidade_fundos_total = rentabilidade_fundos_acumulada.iloc[-1].to_frame()
    # Renomeando a coluna da rentabilidade total
    rentabilidade_fundos_total.columns = ["Rent_Total"]
    # Calculando a rentabilidade média anualizada dos fundos, usando a média da rentabilidade diária multiplicada por 252 (número de dias úteis em um ano)
    rentabilidade_media_anualizada = (rentabilidade_fundos_diaria * (252)).mean(axis=0).dropna().to_frame()
    # Renomeando a coluna da rentabilidade média anualizada
    rentabilidade_media_anualizada.columns = ["Rent_Diária"]
    # Calculando o número de linhas do dataframe
    T = fundo_acoes_filtrado_transformed.shape[0]
    # Calculando o retorno do período anualizado dos fundos, usando a fórmula ((valor final / valor inicial) ^ (252 / T) - 1) * 100
    retorno_periodo_anualizado = (((fundo_acoes_filtrado_transformed["VL_QUOTA"].iloc[-1]/ fundo_acoes_filtrado_transformed["VL_QUOTA"].iloc[0])** (252 / T)- 1)* 100).dropna().to_frame()
    # Renomeando a coluna do retorno do período anualizado
    retorno_periodo_anualizado.columns = ["Rent_Anual"]
    # Calculando a rentabilidade acumulada por ano dos fundos, usando o último valor da rentabilidade acumulada para cada ano
    rentabilidade_acumulada_por_ano = (rentabilidade_fundos_acumulada.groupby(pd.Grouper(freq="Y")).last(1).T.dropna())
    # Renomeando as colunas da rentabilidade acumulada por ano com os anos correspondentes
    rentabilidade_acumulada_por_ano.columns = [str(x)[:4] for x in rentabilidade_acumulada_por_ano.columns]
    # Calculando a volatilidade dos fundos, usando o desvio padrão da rentabilidade diária multiplicado pela raiz quadrada de 252
    volatilidade_fundos = rentabilidade_fundos_diaria.std().dropna().to_frame() * np.sqrt(252)
    # Renomeando a coluna da volatilidade
    volatilidade_fundos.columns = ["volatilidade"]
    # Calculando o risco-retorno dos fundos, usando a volatilidade e o retorno do período anualizado
    risco_retorno = pd.concat([volatilidade_fundos, retorno_periodo_anualizado], axis=0)
    # Juntando os cinco dataframes em um só, usando as colunas 'DT_COMPTC' e 'Fundo' como chaves de junção
    df_final = pd.merge(df_classe, df_quota, on=['DT_COMPTC', 'CNPJ - Nome'])
    df_final = pd.merge(df_final, df_cotst, on=['DT_COMPTC', 'CNPJ - Nome'])
    df_final = pd.merge(df_final, df_patrim, on=['DT_COMPTC', 'CNPJ - Nome'])
    df_final = pd.merge(df_final, rentabilidade_fundos_total,on=['DT_COMPTC', 'CNPJ - Nome'])
    df_final = pd.merge(df_final, rentabilidade_media_anualizada, on=['DT_COMPTC', 'CNPJ - Nome'])
    df_final = pd.merge(df_final, retorno_periodo_anualizado, on=['DT_COMPTC', 'CNPJ - Nome'])
    # Renomeando as colunas que você quer
    
    df_final = df_final.rename(columns={'VL_QUOTA': 'Rent_Diária', 'NR_COTST': 'Rent_Anual', 'VL_PATRIM_LIQ': 'Volatilidade'})
    # Retornando o dataframe final
    df_final = pd.DataFrame(df_final)
    print(pd.DataFrame(df_final.columns.tolist(), 'PRINT 03'))
    return df_final

# Separando os nomes em duas colunas usando o espaço como separador, antes é preciso transformar os DataFrames em TUPLAS

df = df.assign(
    CNPJ = tuple(df["CNPJ - Nome"].str.split(" // ").str[0]), # Pegando o primeiro elemento da lista
    Fundo = tuple(df["CNPJ - Nome"].str.split(" // ").str[-1]) # Pegando o último elemento da lista
)

#Fazendo o Drop do CNPJ - Nome

df = df.sort_index(ascending=False,
                   axis=1,inplace=False, 
                   sort_remaining=True).drop(['CNPJ - Nome',
                                              'CNPJ'],
                                              axis=1
                                              )

print(df)


# Agora calcula a rentabilidade dos fundos extraídos 
df_1 = pd.DataFrame(comp.calcula_rentabilidade_fundos(df))
print(df_1.columns.tolist(), "DF_1")

# #Transforma o resultado do Cálculo em DFrame Para Alinhar As Colunas 
# df_1 =pd.DataFrame(df_1)

# Transformando cada coluna do dataframe df em uma tupla de tuplas, separando as strings por vírgula, mas antes usa ASTYPE para converter para str, especifica que é STR
# e depois baseado em STR ele faz o SPLIT
df_1 = tuple(list(zip(*(df_1[coluna].astype(str).str.split(",") for coluna in df_1))))

# Exibindo o resultado
# print(df_1)

# Vendo a lista de Informações do dataframe que estão deno da Tupla, Antes Converte Pra DFrame

df_1 =pd.DataFrame(df_1)

Arquivo=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\{dt.datetime.now().strftime('%Y-%m-%d')} DF_1 (InformeFundos).csv"

df_1.to_csv(Arquivo, sep=';',decimal=',',index=True,encoding="latin1")

print(pd.DataFrame(df_1.info()))

# Acessando o sub-dataframe dentro da tupla
df = pd.DataFrame(df_1[1].loc[:, ['DT_COMPTC',
                'Fundo',
                'CLASSE',
                'VL_QUOTA',
                'NR_COTST',
                'VL_PATRIM_LIQ',
                'Rent_Total',
                'Rent_Diária',
                'Rent_Anual',
                'volatilidade']], columns=['DT_COMPTC',
                'Fundo',
                'CLASSE',
                'VL_QUOTA',
                'NR_COTST',
                'VL_PATRIM_LIQ',
                'Rent_Total',
                'Rent_Diária',
                'Rent_Anual',
                'volatilidade'])


# Vendo a lista de todas as colunas do dataframe#
print(df.columns.tolist())

# Criando uma nova coluna que combina a data e o nome da empresa
df['Data_Fundo'] = df['DT_COMPTC'].astype(str).str.cat(df['Fundo'], sep="_")

# Usando essa coluna como o novo índice
df = df.set_index('Data_Fundo')

# Renomeando as colunas e reordenando o dataframe
df = df.reindex(
    index=[pd.DataFrame(df)], 
    columns={
        'DT_COMPTC': 'Data',
        'Fundo': 'Fundo', 
        'CLASSE': 'Tipo de Fundo', 
        'VL_QUOTA': 'Valor Cota',
        'NR_COTST': 'Qtde Cotistas',
        'VL_PATRIM_LIQ': 'P. Liquido'
    }, 
    method=None,
    copy=True,
)

# Exibindo o resultado
print(df)


#Para obter as classes disponíveis:
#comp.get_classes()

#Cria a Variável para CRIAÇÃO DO ARQUIVO

Arquivo=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\{dt.datetime.now().strftime('%Y-%m-%d')+1} Print01 (InformeFundos).csv"

informe_diario_fundos_historico.to_csv(Arquivo, sep=';',decimal=',',index=True,encoding="latin1")



# a1 = comp.calcula_rentabilidade_fundos(informe_diario_fundos_historico)
# rentabilidade = pd.DataFrame(a1)
# rentabilidade.dtypes
# print(type(rentabilidade))

# Chamando a função e armazenando o resultado em uma variável
resultado = comp.calcula_rentabilidade_fundos(informe_diario_fundos_historico)
resultado = pd.DataFrame(resultado).dropna().T
resultado = resultado.sort_values(by=0, axis=1)
print(resultado)
Arq=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\{time.time()} Print02 (Resultado).csv"
resultado.to_csv(Arq, sep=';',decimal=',',index=True,encoding="latin1")

# Acessando o primeiro elemento da tupla, que é o risco_retorno
risco_retorno = resultado[0]

# Criando uma máscara booleana usando o método isin
mascara = risco_retorno.index.isin(informe_diario_fundos_historico["CNPJ - Nome"])

# Reindexando a máscara pelo índice do risco_retorno
mascara = mascara.reindex(resultado.index, fill_value=False)

# Criando outra máscara booleana usando a condição
condicao = (informe_diario_fundos_historico["CNPJ - Nome"] == '36.771.708/0001-93 // STIMA ENERGIA FUNDO DE INVESTIMENTO MULTIMERCADO')

# Reindexando a condição pelo índice do risco_retorno
condicao = condicao.reindex(risco_retorno.index, fill_value=False)

# Filtrando o DataFrame usando as máscaras
fundos_filtrados = risco_retorno.loc[mascara & condicao]
# informe_diario_fundos_historico.rename(columns='CNPJ - NOME' == 'Fundo' 'DT_COMPTC' == 'Data' 'CLASSE' == 'Tipo de Fundo' 'VL_QUOTA' == 'Valor Cota'
#                                        'NR_COTST' == 'Qtde Cotistas'
#                                        'VL_PATRIM_LIQ' == 'P. Liquido')

# Imprimindo o resultado
print(fundos_filtrados)


#Arq=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\{dt.datetime.now()} Print02 (Rentabilidade).csv"

#rentabilidade.to_csv(Arq, sep=';',decimal=',',index=True,encoding="utf-8")
# df4 = comp.plotar_evolucao(a1, informe_diario_fundos_historico)

#print(a1, 'E ai')

"""pd.merge(
    dados.query('operacao == "C"').drop(['operacao'], axis=1), 
    dados.query('operacao == "V"').drop(['operacao'], axis=1), 
    on='ativo', 
    how='outer',
    suffixes=('_compra', '_venda')
).fillna('').reindex(columns=['ativo', 'data_negociacao_compra', 'data_negociacao_venda'])"""

# dfm = pd.DataFrame(informe_diario_fundos_historico, a1)
# resultado = pd.concat(dfm)
# print(resultado)

#dfim = pd.DataFrame(informe_diario_fundos_historico, df4, columns='DT_COMPTC', 'CNPJ - Nome','CLASSE	VL_QUOTA',
#                    'NR_COTST',	'VL_PATRIM_LIQ','rentabilidade','volatibilidade')
# #informe_diario_fundos_historico = pd.DataFrame(a1(row2['CNPJ - Nome'],
#                                                                              columns=['DT_COMPTC : Dia',
#                                                                                     'CNPJ - Nome : Fundo',
#                                                                                     'Classe : Tipo', 
#                                                                                     'VL_QUOTA : Cota', 
#                                                                                     'NR_COTST : Cotistas', 
#                                                                                     'VL_PATRIM_LIQ : Patrimonio Liquido'
#                                                                                     ]))
# #dfaux=pd.DataFrame(ListaMesesPeriodo(row2['Mês'],12),columns=['Mês'])

# fim = pd.DataFrame(informe_diario_fundos_historico)
# print(fim, 'Fim 1')
# fim2 = pd.DataFrame(a1)
# print(fim2, 'FIM 2')
# #res = pd.concat([fim, fim2], axis=1)
# Arquivo2=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\{time.time()}fim1.csv"

# fim.to_csv(Arquivo2, sep=';',decimal=',',index=True,encoding="latin1")

# Arquivo3=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\{time.time()}fim2.csv"

# fim2.to_csv(Arquivo3, sep=';',decimal=',',index=True,encoding="latin1")

# print(a1, 'Print 02')

# # Arquivo=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\' {time.time()}' fundos2.csv"
# fim.to_csv(Arquivo, sep=',',decimal=',',index=True,encoding="latin1")

# # Criar Arquivo CSV para comparação

# fundos = pd.DataFrame(informe_diario_fundos_historico)
# fundos1 = ["fundos"]
# #print(fundos1)
# #Definição de Resultado, cadastrando objeto a1 aos Cálculos de Risco e fundos aos Informes_Diários que são os dados dos Fundos pesquisados!

# def Resultado(a1: pd.DataFrame, fundos: pd.DataFrame) -> pd.DataFrame:
#     riscos = a1[["CNPJ - Nome", "rentabilidade", "volatibilidade"]]
#     fundos1 = (fim)
#     empresas = fundos.merge(riscos, fundos1, fill_method="ffill", left_by="group")
#     empresas1 = pd.DataFrame(empresas).dropna
#     for e in Resultado():
#         e = empresas1
#         return print(e)
        
#     #print(empresas)
#     #resul = dict(empresas).copy()
# #    global resul
# empresas2 = pd.DataFrame(Resultado).astype(str, copy=True, errors="ignore")

# print(empresas2)
#    resul = empresas.copy()
   # print (e, 'Print 03')
# x=[]

# if not x in Resultado:
#             x = comp.plotar_evolucao(
#             cotas_normalizadas,
#             lista_fundos=["36.771.708/0001-93"],
#             figsize=(15, 5),
#             color="darkblue",
#             alpha=0.8,
#             sep=" // "
# )
#             #return (x).dropna
# print(str(Resultado))
# print(x)

# #x1 = Resultado

# fundo = ...
# try:
   
#     if fundo not in informe_diario_fundos_historico.iloc[2]:
#         fundo = ('36.771.708/0001-93 // STIMA ENERGIA FUNDO DE INVESTIMENTO MULTIMERCADO')
#         informe_diario_fundos_historico.droplevl()
# finally:        
#         #informe_diario_fundos_historico.loc(['CNPJ - Nome' : '36.771.708/0001-93 // STIMA ENERGIA FUNDO DE INVESTIMENTO MULTIMERCADO'])
#info = pd.DataFrame(informe_diario_fundos_historico).filter(items='36.771.708/0001-93 // STIMA ENERGIA FUNDO DE INVESTIMENTO MULTIMERCADO',
#                                                            axis=1)


# # def _mesclar_bases(cadastro_fundos: pd.DataFrame, informe_diario_fundos: pd.DataFrame) -> pd.DataFrame: #transforma as Chaves em DataFrame
# #     cadastro_fundos_filtrado = cadastro_fundos[['CNPJ_FUNDO', 'CLASSE', 'DENOM_SOCIAL']] #Essa Chave cria um DFrame com 03 colunas
# #     dados_completos_filtrados = informe_diario_fundos.merge(cadastro_fundos_filtrado, on=['CNPJ_FUNDO'], how="inner") #Cria uma Variável que é o resultado do Merge Com a Coluna CNPJ_FUNDO como referência de dados
# #     dados_completos_filtrados["CNPJ - Nome"] = dados_completos_filtrados["CNPJ_FUNDO"] + " // " + dados_completos_filtrados["DENOM_SOCIAL"]
# #     dados_completos_filtrados = dados_completos_filtrados[["CNPJ - Nome", 'DT_COMPTC', 'CLASSE', 'VL_QUOTA', "NR_COTST", "VL_PATRIM_LIQ"]]
# #     return dados_completos_filtrados              

# # Arquivo=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\' {time.time()}' fundos2.csv"
# # resul.to_csv(Arquivo, sep=',',decimal=',',index=True,encoding="latin1")
# # Arquivo=pd.DataFrame(informe_diario_fundos_historico


# #print(data)