# -*- coding: utf-8 -*- 
import pandas as pd
import requests
import zipfile
import plotly.express as px

pd.options.display.float_format = '{:.4f}'.format

# Crie uma lista com os anos que você quer
anos = ["2021", "2022", "2023", "2024"] 

# Crie uma lista com os meses que você quer
meses = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

# Crie um dataframe vazio para armazenar todos os dados
df_final = pd.DataFrame()

# Use um loop for para iterar sobre os anos e os meses
for ano in anos:
    for mes in meses:
        # Gere a url do arquivo correspondente ao ano e ao mês
        url = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano}{mes}.zip'
        
        # Faça o download do arquivo
        download = requests.get(url)
        
        # Verifique o código de status da resposta
        if download.status_code == 200:
            # Salve o arquivo zip em seu computador
            with open(f"inf_diario_fi_{ano}{mes}.zip", "wb") as arquivo_cvm:
                arquivo_cvm.write(download.content) 
            
            # Extraia o arquivo zip e leia o arquivo csv dentro dele
            arquivo_zip = zipfile.ZipFile(f"inf_diario_fi_{ano}{mes}.zip")
            df = pd.read_csv(arquivo_zip.open(arquivo_zip.namelist()[0]), sep=';', encoding = 'ISO-8859-1')
            
            # Concatene o dataframe lido com o dataframe vazio
            df_final = df_final._append(df, ignore_index=True)
        else:
            # Ignore o arquivo zip inválido ou tente outra url
            print(f"O arquivo inf_diario_fi_{ano}{mes}.zip não existe ou é inválido.")

# Filtrar o dataframe final pelo CNPJ do fundo e remover as linhas com NaN
df_final = df_final.where(df_final['CNPJ_FUNDO'] == '36.771.708/0001-93').dropna()

# Salve o dataframe final em um arquivo csv
df_final.to_csv("inf_diario_fi_final.csv", index=False, sep=';')


# dados_fundos = pd.read_csv(arquivo_zip.open(arquivo_zip.namelist()[0]), sep = ";", encoding = 'ISO-8859-1')
# print(df_final)

# Agora acessamos a base de cadastro dos fundos para criar um DTFRAME com os nomes para que possa ser filtrado posteriormente
dados_cadastro = pd.read_csv('https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv', 
                             sep = ";", encoding = 'ISO-8859-1')
dados_cadastro = dados_cadastro[['CNPJ_FUNDO', 'DENOM_SOCIAL']]
dados_cadastro = dados_cadastro.drop_duplicates()
dados_cadastro

# Caso Queira Filtrar Um Período Dentro Dos Períodos Baixados Anteriormente
# data_inicio_mes = (dados_fundos['DT_COMPTC'].sort_values(ascending = True).unique())[0]
# data_fim_mes = (dados_fundos['DT_COMPTC'].sort_values(ascending = True).unique())[-1]  
# dados_fundos_filtrado = dados_fundos[(dados_fundos['DT_COMPTC'].isin([data_inicio_mes, data_fim_mes]))
# dados_fundos_filtrado

# Realizamos o Merge dos Frames Para Retornar Apenas O Fundo Selecionado, Podendo Ser Mais De Um Se Quiser
base_final = pd.merge(df_final, dados_cadastro, how = "left", 
                      left_on = ["CNPJ_FUNDO"], right_on = ["CNPJ_FUNDO"])
base_final = base_final[['DT_COMPTC', 'CNPJ_FUNDO', 'DENOM_SOCIAL', 'VL_QUOTA', 'VL_TOTAL', 'VL_PATRIM_LIQ', 'NR_COTST', 'CAPTC_DIA', 'RESG_DIA']]

# Filtramos O Fundo Que Queremos Com Base Em ALguma Palavra Do Nome, Não Precisa Ser Inteiro
fundo_stima = base_final[base_final['DENOM_SOCIAL'].str.contains("STIMA", na = False)]
print(fundo_stima)
# fundo_stima.to_excel('Fundo Stima.xlsx')

# fundo_stima_master = fundo_stima[(fundo_stima['CNPJ_FUNDO'] == "36.771.708/0001-93")] &
                                        #   ( fundo_stima['DT_COMPTC'] == "2022-12-30")]

patrimonio_do_fundo =  "R$ " + str((fundo_stima.iloc[0, fundo_stima.columns.get_loc('VL_PATRIM_LIQ')]/1000000).round(2)) + "MM"
print(patrimonio_do_fundo, '\nPATRIMONIO\n')

# fundo_stima_fic = fundo_stima[(fundo_stima['CNPJ_FUNDO'] == "36.771.708/0001-93")]

# Calculamos a Rentabilidade Total do Fundo, Baseado Na Diferença Entre o Primeiro Dia da Tabela Contra o Último Dia Da Mesma Tabela                                          
retorno_fundo = ("Retorno fundo: " +
            str(((fundo_stima['VL_QUOTA'].iloc[-1]/fundo_stima['VL_QUOTA'].iloc[0] - 1)
                 * 100).round(2)) 
               + "%")
print(retorno_fundo)

# Calcular a porcentagem da diferença entre os valores diários
fundo_stima['VL_QUOTA'].pct_change()
fundo_stima['VL_TOTAL'].pct_change()
fundo_stima['VL_PATRIM_LIQ'].pct_change()
fundo_stima['VL_PATRIM_LIQ'].pct_change()

# Agregar o resultado ao dataframe original
fundo_stima = fundo_stima.assign(Rentabilidade_Dia=fundo_stima['VL_QUOTA'].pct_change(fill_method='ffill'),
                                Rentabilidade_Cota=retorno_fundo,
                                Dif_Valor_Carteira=fundo_stima['VL_TOTAL'].pct_change(fill_method='ffill'), 
                                Dif_Patrimonio=fundo_stima['VL_PATRIM_LIQ'].pct_change(fill_method='ffill'),
                                Rent_Diaria_PL=fundo_stima['VL_PATRIM_LIQ'].pct_change(fill_method='ffill')
)
fundo_stima.rename(columns={'DT_COMPTC' : 'Data',
                            'CNPJ_FUNDO' : 'CNPJ',
                            'DENOM_SOCIAL' : 'Nome Fundo',
                            'VL_QUOTA' : 'Valor Cota',
                            'VL_TOTAL' : 'Valor Total',
                            'VL_PATRIM_LIQ' : 'Valor P.Líquido',
                            'NR_COTST' : 'Qtd Cotistas',
                            'CAPTC_DIA' : 'Captação $',
                            'RESG_DIA' : 'Resgate $'}                        
)
print(fundo_stima, 'FUNDO 1')

# Criamos o Arquivo XLMS Para Análises
fundo_stima.to_excel('Retorno Fundo.xlsx', sheet_name='Fundo STIMA')

# Criado um Gráfico Para Demonstrar A Evolução Do Fundo Com o Tempo
graf = px.line(data_frame=fundo_stima,
           x='DT_COMPTC',
           y='VL_QUOTA',
           markers=True,
           title='Evolução Fundo STIMA',
           labels={'DT_COMPTC' : 'Data',
                   'VL_QUOTA' : 'Valor Das Cotas'}
           
)
graf.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
graf.show()