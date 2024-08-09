#Fundos Original

import comparar_fundos_br as comp
import pandas as pd

informe_diario_fundos_historico = comp.get_brfunds(anos=range(2022,2023), #somente 2021
                                              meses=range(1,3), #somente Jan e Fev,
                                              classe=["Fundo Multimercado"])

#Para obter as classes disponíveis:
comp.get_classes()

(  risco_retorno,
    cotas_normalizadas,
    rentabilidade_media_anualizada,
    rentabilidade_acumulada_por_ano,
    rentabilidade_fundos_total,
) = comp.calcula_rentabilidade_fundos(informe_diario_fundos_historico)

# Criar Arquivo CSV para comparação
fundos = pd.DataFrame(informe_diario_fundos_historico)
Arquivo="C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\fundos.csv"
fundos.to_csv(Arquivo, sep=',',decimal=',',index=True,encoding="latin1")
# Arquivo=pd.DataFrame(informe_diario_fundos_historico)

print(informe_diario_fundos_historico)