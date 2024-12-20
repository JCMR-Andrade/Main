# -*- coding: utf-8 -*-
#python -m pip install --upgrade certifi --trusted-host pypi.org --trusted-host files.pythonhosted.org ##### Para Atualizar Certificados Sem Usar o Pip Install Afetado
# Novo Código Reports

from brfinance.connector import CVMHttpClientConnector
from brfinance.http_client import CVMHttpClient
from brfinance import CVMAsyncBackend
import pandas as pd
from datetime import datetime, date
import datetime
import openpyxl # Importar a biblioteca openpyxl
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os

cvm_httpclient = CVMAsyncBackend()

# Criar uma instância da classe CVMAsyncBackend
cvm = CVMHttpClient(CVMHttpClientConnector)

# Dict de códigos CVM para todas as empresas
cvm_codes = cvm_httpclient.get_cvm_codes()

# Busca Notícias e Fatos Relevante, ITRs
search_result = cvm_httpclient.get_consulta_externa_cvm_results(start_date=date(2020, 1, 1),
                                            end_date=date.today(),
                                            last_ref_date=False,
                                            cod_cvm=['8656'],                      #last_ref_date = False # Se "True" retorna apenas o último report no intervalo de datas
                                            category=["EST_-1",                     #  'EST_-1': TODOS os Documentos Estruturados
                                                    "EST_3",                        #  'EST_1': 'FCA - Formulário Cadastral'
                                                    "EST_2",                        #  'EST_2': 'FRE - Formulário de Referência'
                                                    "EST_4",                        #  'EST_3': 'ITR - Informações Trimestrais'
                                                    "EST_13"]                       #  'EST_4': 'DFP - Demonstrações Financeiras Padronizadas' 
                                                )                                   #  'EST_11': 'Informe do Código de Governança'    
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

                                                                                    
search_result = search_result[
    (search_result['categoria']=="DFP - Demonstrações Financeiras Padronizadas") |
    (search_result['categoria']=="ITR - Informações Trimestrais") |
    (search_result['categoria']=="FCA - Formulário Cadastral") |
    (search_result['categoria']=="FRE - Formulário de Referência") |
    (search_result['categoria']=="IAN - Informações Anuais")]

                                                    
search_result = search_result[pd.to_numeric(search_result['numero_seq_documento'], errors='coerce').notnull()]


print(search_result, search_result.columns)


agora = datetime.datetime.now().strftime("%Y%m%d__%H_%M_%S")

# Receber o valor do documento do usuário
valor_documento = input("Digite o número do documento que está buscando: ")

# Converter para inteiro
valor_documento = int(valor_documento)

# Obter a data e a hora atual
current_datetime = datetime.datetime.now()

# Converter o objeto datetime em uma string com o formato desejado
str_current_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

search = pd.DataFrame(search_result)
empresa = f"{search.iloc[3]['empresa']}"
tipo_doc = f"{search.iloc[4]['categoria']}".strip().split(sep=' - ')[0]
data_ref = f"{search.iloc[8]['ref_date']}".split(sep=' ')[0]

print(data_ref)

# Concatenar o nome da empresa e a extensão do arquivo com a string da data e hora
file_name = r"C:\\Users\\HP\\Documents\\Python Scripts\\PythoN\\B3\\Documentos Empresas\\Doc. Tipo " + tipo_doc + " da Empresa " + empresa + ".xlsx"

# Criar um objeto ExcelWriter, passando o nome do arquivo como argumento
# writer = pd.ExcelWriter(file_name, engine='openpyxl', mode='w', if_sheet_exists='overlay')

reports_list = [
    'Balanço Patrimonial Ativo',
    'Balanço Patrimonial Passivo',
    'Demonstração do Resultado',
    'Demonstração do Resultado Abrangente',
    'Demonstração do Fluxo de Caixa',
    'Demonstração das Mutações do Patrimônio Líquido',
    'Demonstração de Valor Adicionado'] # Se None retorna todos os demonstrativos disponíveis.


# Percorrer os resultados e salvar os dados em planilhas diferentes
for index, row in search_result.iterrows():
    empresa = f"{row['cod_cvm']} - {cvm_codes[row['cod_cvm']]}"
    print("*" * 20, empresa, "*" * 20)


    with pd.ExcelWriter(file_name, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:

    # Usar um bloco try-except para capturar possíveis exceções
        try:
            lista_reports = {}

        # Especificar os nomes dos relatórios que quer obter
            reports = cvm_httpclient.get_report(row["numero_seq_documento"], row["codigo_tipo_instituicao"], reports_list=reports_list)

            for report in reports:
                    reports[report]["cod_cvm"] = row["cod_cvm"]
                    reports.update(lista_reports)
                    print(reports[report].head())

            # Salvar o dataframe em uma planilha, passando o objeto ExcelWriter e o nome da planilha como argumentos
                    reports[report].to_excel(writer, sheet_name=report)

        except ValueError as e:
        # Mostrar uma mensagem de aviso se o valor do documento não existir
            print(f"Valor do documento inválido: {e}")
        except IndexError as f:
        # Mostrar uma mensagem de aviso se houver algum problema na conexão
            print(f"Erro na requisição: {f}")
        except KeyError as g:
            print(f'Erro de Valor: {g}')


        print(lista_reports, '****************')
        
        # Salvar e fechar o arquivo .xlsx
        writer._save()

        # Obter o objeto Workbook do openpyxl
# wb = writer.book

#     # Obter a planilha vazia do workbook
# ws = wb['Sheet']

#     # Remover a planilha vazia do workbook
# wb.remove('Sheet')

# writer.close()

# # Salvar a planilha em um arquivo .xlsx
# root = tk.Tk()
# dirNome = tk.filedialog.askdirectory(parent=root, initialdir="/",title='Selecione a pasta')
# writer.save(file_name)
# writer.close()