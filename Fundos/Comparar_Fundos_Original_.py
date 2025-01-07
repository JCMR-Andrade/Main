import comparar_fundos_br as comp
import matplotlib.pyplot as plt
import pandas as pd

# informe_diario_fundos_historico = comp.get_brfunds(anos=range(2021,2022), #somente 2021
#                                               meses=range(1,3), #somente Jan e Fev
#                                               classe="Fundo de Ações", 
#                                               num_minimo_cotistas=10, 
#                                               patriminio_liquido_minimo=1e6)

df_ini = comp.get_brfunds(anos=range(2022,2024), #somente 2021
                                              meses=range(1,12), #somente Jan e Fev,
                                              classe=["Fundo Multimercado"])
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

#Para obter as classes disponíveis:
comp.get_classes()

(   risco_retorno,
    cotas_normalizadas,
    rentabilidade_media_anualizada,
    rentabilidade_acumulada_por_ano,
    rentabilidade_fundos_total,
) = comp.calcula_rentabilidade_fundos(df_ini)

df4 = risco_retorno[
                    (risco_retorno["volatilidade"] <= 40)
                    & (risco_retorno["rentabilidade"] >= 0)
                    & (risco_retorno["rentabilidade"] <= 100)
                    ]

comp.plotar_comparacao_risco_retorno(
                                df4,
                                (21, 18), #(risco, retorno) da minha carteira
                                (19, 15), #(risco, retorno) do benchmark
                                nome_carteira="Minha Carteira",
                                nome_benchmark="Benchmark",
                                figsize=(15, 5),
                                posicao_texto_carteira=(30, 25),
                                posicao_texto_benchmark=(31, -25),
                                )
plt.title("Risco x Retorno - Fundos de Ações")
plt.ylim(-10, 140)
plt.xlim(-3, 60)
plt.show()

cdi, cdi_acumulado = comp.get_benchmark("2021-01-01", 
                                        "2023-12-25", 
                                        benchmark = "cdi")
                                        

data = comp.plotar_evolucao(
                cotas_normalizadas,
                lista_fundos=["36.771.708/0001-93"],
                figsize=(12, 5),
                color="darkblue",
                alpha=0.8
                )
plt.title("Evolução dos Fundos")
plt.plot(cdi_acumulado*100, label="CDI")
plt.legend(frameon=False, loc="center right")
plt.show()

indice_ibov, indice_ibov_acumulado = comp.get_benchmark("2021-01-01", 
                                                        "2023-12-25", 
                                                        benchmark = "CDI")
                                                    

data = comp.plotar_evolucao(
                cotas_normalizadas,
                lista_fundos=["Stima"],
                figsize=(12, 5),
                color="gray",
                alpha=0.2,
                color_maximo="orange",
                color_minimo="blue",
                color_seta_maximo="orange",
                color_seta_minimo="blue",
                posicao_texto_maximo=(-100, -45),
                posicao_texto_minimo=(-100, 40),
                )
plt.title("Evolução do Fundo STIMA FIM")
plt.plot(indice_ibov_acumulado*100, label="Ibovespa", color="red", lw=3)
plt.legend(frameon=False, loc="upper center")
plt.show()

melhores = data.iloc[-1:].T.dropna().sort_values(data.index[-1], ascending=False)
melhores.columns = ["Evolução"]
melhores = melhores.reset_index()
melhores[['CNPJ', 'DENOM SOCIAL']] = melhores['CNPJ - Nome'].str.split(' // ', 1, expand=True)
melhores = melhores.drop('CNPJ - Nome', axis=1)
melhores.head()

melhores_fundos, piores_fundos = comp.melhores_e_piores_fundos(rentabilidade_fundos_total, num=10)

fundos_maior_risco, fundos_menor_risco = comp.melhores_e_piores_fundos(risco_retorno[["volatilidade"]], num=10)