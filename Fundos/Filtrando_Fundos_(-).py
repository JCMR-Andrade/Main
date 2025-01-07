# -*- coding: utf-8 -*-
import comparar_fundos_br as comp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
from typing import Any, List, Tuple, Union

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

import seaborn as sns; sns.set()
import matplotlib.pyplot as plt


df_ini = comp.get_brfunds(anos=2022,
                          meses=1,
                          classe='Fundo Multimercado')

def rentabilidade_fundos(
    dados_fundos_cvm: pd.DataFrame,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    copia = dados_fundos_cvm.copy()
    fundo_acoes_filtrado_transformed = copia.pivot_table(
        index="DT_COMPTC", values=['VL_QUOTA', 'NR_COTST', 'VL_PATRIM_LIQ']
    )
    # Ordenando o DataFrame pelo valor da coluna 'DT_COMPTC'
    fundo_acoes_filtrado_transformed = fundo_acoes_filtrado_transformed.sort_values(by='DT_COMPTC')
    fundo_acoes_filtrado_transformed.to_excel('né.xlsx')

    cotas_normalizadas = (fundo_acoes_filtrado_transformed["VL_QUOTA"]/ fundo_acoes_filtrado_transformed["VL_QUOTA"].iloc[0])
    print(cotas_normalizadas, '\n COTAS_NORMALIZADAS\n')

    rentabilidade_fundos_diaria = fundo_acoes_filtrado_transformed["VL_QUOTA"].pct_change()
    rentabilidade_fundos_acumulada = (1 + rentabilidade_fundos_diaria).cumprod() - 1
    print(rentabilidade_fundos_acumulada, '\n RENTABILIDADE_FUNDOS_ACUMULADA\n')

    rentabilidade_fundos_total = pd.DataFrame(rentabilidade_fundos_acumulada).iloc[1].to_frame()
    rentabilidade_fundos_total.columns = ["Rentabilidade Total"]
    print(rentabilidade_fundos_total, '\n RENTABILIDADE_FUNDOS_TOTAL\n')

    rentabilidade_media_anualizada = pd.DataFrame(rentabilidade_fundos_diaria * (252)).mean(axis=0).dropna().to_frame()
    rentabilidade_media_anualizada.columns = ["Rentabilidade Diaria"]
    print(rentabilidade_media_anualizada, '\n RENTAABILIDADE_MEDIA_ANUALIZADA\n')

    T = fundo_acoes_filtrado_transformed.shape[0]
    # retorno_periodo_anualizado = (((fundo_acoes_filtrado_transformed["VL_QUOTA"].iloc[-1]/ fundo_acoes_filtrado_transformed["VL_QUOTA"].iloc[0])** (252 / T)- 1)* 100).to_frame()
    
    # Isso é um valor numérico
    valor = (((fundo_acoes_filtrado_transformed["VL_QUOTA"].iloc[-1]/ fundo_acoes_filtrado_transformed["VL_QUOTA"].iloc[0])** (252 / T)- 1)* 100)
    print(valor, '\nVALOR\n')
    # Isso é um dataframe com uma coluna
    df = pd.DataFrame ({"\nRentabilidade (%)": [valor]})#.set_index('DT_COMPTC')
    print(df, '\n RENTABILIDADE %\n')

    rentabilidade_acumulada_por_ano = pd.DataFrame(rentabilidade_fundos_acumulada.groupby(pd.Grouper(freq="Y", origin='start')).last(1).T).dropna()
    rentabilidade_acumulada_por_ano.columns = [str(x)[:4] for x in rentabilidade_acumulada_por_ano.columns]
    print(rentabilidade_acumulada_por_ano, 'RENTABILIDADE_ACUMULADA_POR_ANO\n')

    volatilidade_fundos = pd.DataFrame(rentabilidade_fundos_diaria).std().dropna().to_frame() * np.sqrt(252)
    volatilidade_fundos.columns = ["volatilidade"]
    # Calculando a diferença entre o dia calculado e o dia anterior para a volatilidade dos fundos
    volatilidade_fundos["diferenca"] = volatilidade_fundos["volatilidade"].diff()
    print(volatilidade_fundos, '\nVOLATILIDADE_FUNDOS\n')

    risco_retorno = pd.concat([volatilidade_fundos, df], axis=0)
    print(risco_retorno, '\nRISCO_RETORNO\n')
    # # Redefinindo o índice dos DataFrames
    # risco_retorno = risco_retorno.reset_index(drop=True)
    # cotas_normalizadas = cotas_normalizadas.reset_index(drop=True)
    rentabilidade_media_anualizada = rentabilidade_media_anualizada.reset_index(drop=True)
    # rentabilidade_acumulada_por_ano = rentabilidade_acumulada_por_ano.reset_index(drop=True)
    rentabilidade_fundos_total = rentabilidade_fundos_total.reset_index(drop=True)
    volatilidade_fundos = volatilidade_fundos.reset_index(drop=True)

    # Concatenando os DataFrames verticalmente
    df_final = pd.concat([copia, cotas_normalizadas, rentabilidade_fundos_acumulada, rentabilidade_media_anualizada, rentabilidade_acumulada_por_ano, rentabilidade_fundos_total, risco_retorno], axis=1).fillna('')
    df_final = pd.DataFrame(df_final).rename(index={df_final.index.name: 'DT_COMPTC'})
    df_final = pd.DataFrame(df_final).rename(columns={'CNPJ - Nome' : 'Fundo',
                                            'CLASSE' : 'Tipo De Fundo',
                                            'VL_QUOTA' : 'Vl Cota',
                                            'NR_COTST' : 'Nr Cotistas',
                                            'VL_PATRIM_LIQ' : 'P. Liquido',
                                            'VL_QUOTA' : 'Cota Ajustada',
                                            'VL_Q' : 'Rent. Acumulada'
    })
    df_final.to_excel('Shit.xlsx', index_label='DT_COMPTC')
    # df_end = pd.DataFrame(df_final,
    #                     columns=['CNPJ - Nome', 'CLASSE', 'VL_QUOTA', 'NR_COTST', 'VL_PATRIM_LIQ', 'VL_QUOTA', 'Rentabilidade Total', 'Rentabilidade Diaria', 'Rentabilidade (%)', 'volatilidade'],
    #                     index='DT_COMPTC'
# )

# Retornando o DataFrame final
    return df_final


# Criando a lista de filtro
fundo = ['36.771.708/0001-93 // STIMA ENERGIA FUNDO DE INVESTIMENTO MULTIMERCADO']

# Criando uma lista vazia
lista_nomes = []

# Loop para filtrar os nomes
for nome in df_ini['CNPJ - Nome']:
    # Verificando se o nome está na lista de filtro
    if nome in fundo:
        # Adicionando os nomes filtrados à lista
        lista_nomes.append(nome)

# Selecionando as linhas do dataframe com base na lista de nomes
df_filtrado1 = df_ini[df_ini['CNPJ - Nome'].isin(lista_nomes)]

print(df_filtrado1, '01')
# Chamando a função fora do loop com o dataframe filtrado
df_filtrado = rentabilidade_fundos(df_filtrado1)

print(df_filtrado.columns, '02')
# Concatenando os dataframes verticalmente
# df_final = pd.concat(df_filtrado, axis=0, join='inner',)
# # df_final2 = pd.merge(left=df_filtrado1, right=df_final, how='left', on='DT_COMPTC')
# print(df_final.columns, '03')

df_filtrado.to_excel('teste1.xlsx')

result = comp.plotar_evolucao(df=df_filtrado,
                              lista_fundos=lista_nomes,
                              index='DT_COMPTC')

print (result)