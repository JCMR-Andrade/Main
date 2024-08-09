# -*- coding: utf-8 -*-
from brfinance.connector import CVMHttpClientConnector
from brfinance.http_client import CVMHttpClient
from brfinance import CVMAsyncBackend
import pandas as pd
from datetime import datetime, date
import datetime
import numpy as np
from brfinance.responses import (
    GetCVMCodesResponse,
    GetCategoriesResponse,
    GetSearchResponse,
    GetReportResponse,
    GetTipoParticipanteResponse,
    GetCadastroInstrumentosTokenResponse,
    GetCadastroInstrumentosResponse,
    GetEmissorResponse,
    GetPesquisaCiaAbertaResponse
)


cvm_httpclient = CVMAsyncBackend()

# Criar uma instância da classe CVMAsyncBackend
cvm = CVMHttpClient(CVMHttpClientConnector)

# Dict de códigos CVM para todas as empresas
cvm_codes = cvm_httpclient.get_cvm_codes()
# cvm_codes1 = pd.DataFrame(cvm_codes, index=[0])
#print(cvm_codes)

#Dict de todas as categorias de busca disponíveis (Fato relevante, DFP, ITR, etc.)
categories = cvm_httpclient.get_consulta_externa_cvm_categories()
#print(categories)

#Realizando busca por Empresa
start_date = date(2023, 1, 1)
end_dt = date.today()
cvm_codes_list = ['901348'] # B3
category = ["EST_4", "EST_3", "IPE_4_-1_-1"] # Códigos de categoria para DFP, ITR e fatos relevantes
last_ref_date = False # Se "True" retorna apenas o último report no intervalo de datas


# Busca Notícias e Fatos Relevante, ITRs
search_result = cvm_httpclient.get_consulta_externa_cvm_results(start_date=date(2023, 1, 1),
                                            end_date=date.today(),
                                            category=["EST_-1",                     #  'EST_-1': TODOS os Documentos Estruturados
                                                    "EST_3",                        #  'EST_1': 'FCA - Formulário Cadastral'
                                                    "IPE_4_-1_-1",                  #  'EST_2': 'FRE - Formulário de Referência'
                                                    "IPE_-1_58_-1"]                 #  'EST_3': 'ITR - Informações Trimestrais' 
                                                )                                   #  'EST_4': 'DFP - Demonstrações Financeiras Padronizadas'
                                                                                    #  'EST_11': 'Informe do Código de Governança'    
                                                                                    #  'EST_13': 'IAN - Informações Anuais'   
                                                                                    #  'IPE_70_-1_-1': 'Estatuto Social|TODOS|   TODAS'
                                                                                    #  'IPE_4_-1_-1': 'Fato Relevante|TODOS|   TODAS'   
                                                                                    #  'IPE_44_-1_-1': 'Acordo de Acionistas|TODOS|   TODAS'
                                                                                    #  'IPE_1_-1_-1': 'Assembleia|TODOS|   TODAS'
                                                                                    #  'IPE_1_98_-1': 'Assembleia|AGCRA|   TODAS'
                                                                                    #  'IPE_1_97_-1': 'Assembleia|AGCRI|   TODAS'
                                                                                    #  'IPE_1_5_-1': 'Assembleia|AGDEB|   TODAS'
                                                                                    #  'IPE_1_1_-1': 'Assembleia|AGE|   TODAS'
                                                                                    #  'IPE_91_113_-1': 'Carta Anual de Governança Corporativa|Carta Anual de Governança Corporativa (art. 8º  VIII da Lei 13.303/16|   TODAS'
                                                                                    #  'IPE_6_-1_-1': 'Comunicado ao Mercado|TODOS|   TODAS'
                                                                                    #  'IPE_6_53_-1': 'Comunicado ao Mercado|Outros Comunicados Não Considerados Fatos Relevantes|   TODAS'
                                                                                    #  'IPE_7_-1_-1': 'Dados Econômico-Financeiros|TODOS|   TODAS'
                                                                                    #  'IPE_7_56_-1': 'Dados Econômico-Financeiros|Balanço Social|   TODAS'
                                                                                    #  'IPE_7_37_-1': 'Dados Econômico-Financeiros|Demonstrações Financeiras Anuais Completas|   TODAS'
                                                                                    #  'IPE_7_46_-1': 'Dados Econômico-Financeiros|Demonstrações Financeiras Intermediárias|   TODAS'
                                                                                    #  'IPE_7_85_-1': 'Dados Econômico-Financeiros|Plano de Investimento|   TODAS'
                                                                                    #  'IPE_101_-1_-1': 'DF - Patrimônio separado|TODOS|   TODAS'
                                                                                    #  'IPE_78_-1_-1': 'Documentos de Oferta de Distribuição Pública|TODOS|   TODAS'
                                                                                    #  'IPE_54_-1_-1': 'Escrituras e aditamentos de debêntures|TODOS|   TODAS'
                                                                                    #  'IPE_58_-1_-1': 'Informações de Companhias em Recuperação Judicial ou Extrajudicial|TODOS|   TODAS'
                                                                                    #  'IPE_100_-1_-1': 'Informe Mensal de CRA|TODOS|   TODAS'
                                                                                    #  'IPE_83_-1_-1': 'Política de Dividendos|TODOS|   TODAS'
                                                                                    #  'IPE_76_-1_-1': 'Regimento Interno do Comitê de Auditoria Estatutário|TODOS|   TODAS'
                                                                                    #  'IPE_99_117_-1': 'Regulamentos da B3|Processo de enforcement|   TODAS'
                                                                                    #  'IPE_-1_37_-1': 'Tipo: Demonstrações Financeiras Anuais Completas'
                                                                                    #  'IPE_-1_58_-1': 'Tipo: Relatório Anual'
                                                                                    #  'IPE_-1_43_-1': 'Tipo: Relatório de Análise Gerencial'
                                                                                    #  'IPE_-1_91_-1': 'Tipo: Aviso ao Mercado'
                                                                                    #  'IPE_-1_138_-1': 'Tipo: Composição de carteira'
                                                                                    #  'IPE_-1_68_-1': 'Tipo: Causas e circunstâncias da falência'
                                                                                    #  'IPE_1_4_-1': 'Assembleia|AGESP|   TODAS'
                                                                                    #  'IPE_1_2_-1': 'Assembleia|AGO|   TODAS'
                                                                                    #  'IPE_1_3_-1': 'Assembleia|AGO/E|   TODAS'
                                                                                    #  'IPE_3_-1_-1': 'Aviso aos Acionistas|TODOS|   TODAS'
                                                                                    #  'IPE_9_-1_-1': 'Calendário de Eventos Corporativos|TODOS|   TODAS'
                                                                                    #  'IPE_91_-1_-1': 'Carta Anual de Governança Corporativa|TODOS|   TODAS'

                                                    

# Filtrar dataframe de busca para DFP, ITR, FCA, FE e IAN
search_result = search_result[
    (search_result['categoria']=="DFP - Demonstrações Financeiras Padronizadas") |
    (search_result['categoria']=="ITR - Informações Trimestrais")]# |
    # (search_result['categoria']=="FCA - Formulário Cadastral") |
    # (search_result['categoria']=="FRE - Formulário de Referência") |
    # (search_result['categoria']=="IAN - Informações Anuais")]

search_result = search_result[pd.to_numeric(search_result['numero_seq_documento'], errors='coerce').notnull()]

# reports_list = [
#     'Balanço Patrimonial Ativo',
#     'Balanço Patrimonial Passivo',
#     'Demonstração do Resultado',
#     'Demonstração do Resultado Abrangente',
#     'Demonstração do Fluxo de Caixa',
#     'Demonstração das Mutações do Patrimônio Líquido',
#     'Demonstração de Valor Adicionado'] # Se None retorna todos os demonstrativos disponíveis.

print(search_result)

agora = datetime.datetime.now().strftime("%Y%m%d__%H_%M_%S")

# Receber o valor do documento do usuário
valor_documento = input("Digite o número do documento que está buscando: ")

# Converter para inteiro
valor_documento = int(valor_documento)
# Obter demonstrativos
reports = cvm_httpclient.get_report(NumeroSequencialDocumento=valor_documento, CodigoTipoInstituicao=1, reports_list=None)

# Criar um dataframe vazio fora do loop
df_novo = pd.DataFrame()

for index, row in search_result.iterrows():
    global empresa
    empresa = f"{row['cod_cvm']} - {cvm_codes[row['cod_cvm']]}"
    print("*" * 20, empresa, "*" * 20)
    reports = cvm_httpclient.get_report(row["numero_seq_documento"], row["codigo_tipo_instituicao"], reports_list=['Demonstração do Resultado'])
    
    # Criar uma lista vazia para armazenar os dataframes de cada report
    dfs = []
    for report in reports:
        reports[report]["cod_cvm"] = row["cod_cvm"]
        print(reports[report].head())
        # Transformar o dicionário reports em um dicionário que tenha listas de tamanhos iguais, usando o método zip()
        reports = {k: dict (zip (v['Conta'], v['Valor'])) for k, v in reports.items ()}

        # Criar um DataFrame a partir do novo dicionário, usando o parâmetro orient='index' e columns=['Conta','Descrição','Valor','currency_unit','cod_cvm']
        df = pd.DataFrame.from_dict(reports, orient='index', columns=['Conta','Descrição','Valor','currency_unit','cod_cvm'])

        # Usar a coluna 'Conta' como índice
        # df = df.set_index('Conta')
        # Usar o método pd.DataFrame com os dados do df e o index da coluna 'Conta'
        df_ordem = pd.DataFrame(data=df, index=df['Conta'].values)
        print(df, '**********************************************')
        # Adicionar o dataframe df_ordem à lista dfs
        dfs.append(df_ordem)

    # Usar o método concat() para juntar os dataframes da lista dfs em um único dataframe
    # Usar o parâmetro ignore_index=False para preservar os índices originais
    df_concat = pd.concat(dfs, ignore_index=False)
    
    # Usar o método append() para adicionar o dataframe df_concat ao dataframe df_novo
    df_novo = df_novo.append(df_concat, ignore_index=True)

print(df_novo)

# Arquivo =f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Área de Trabalho\\Códigos B3\\Planilhas\\Lista Documentos De "+ str({empresa}) +".csv"
# search_result.to_csv(Arquivo, sep=';',decimal=',',index=True,encoding="utf-8")

# Salvar o dataframe df_novo em um arquivo CSV
df_novo.to_csv(sep=';',decimal=',',index=True,encoding="utf-8")

#Comando Para Criar O Arquivo Na Pasta Que Eu Escolher No Momento 

import openpyxl 
import tkinter as tk
from tkinter import filedialog

# Criar uma nova planilha em branco
wb = openpyxl.Workbook() # Criar um objeto Workbook
planilha = wb.active # Selecionar a planilha ativa
planilha.title = 'Resultado do REPORT' # Definir o título da planilha

# Adicionar os nomes das colunas à planilha
planilha.append(['Conta', 'Descrição', 'Valor', 'currency_unit', 'cod_cvm'])
# Salvar a planilha em um arquivo .xlsx
root = tk.Tk()
dirNome = tk.filedialog.askdirectory(parent=root, initialdir="/",title='Selecione a pasta')
wb.save(dirNome + '/Planilha.xlsx')