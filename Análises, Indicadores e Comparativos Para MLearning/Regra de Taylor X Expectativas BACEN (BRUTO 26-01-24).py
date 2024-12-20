# coding=utf-8
from bcb import sgs
from bcb import Expectativas
import pandas as pd
import numpy as np
from functools import reduce
import statsmodels.api as sm
from plotnine import *


'''2. Coleta e Tratamento de dados
2.1 Selic
Abaixo, começamos importando a taxa básica de juros que é calibrada pelo Banco Central.'''


# Taxa de juros - Meta Selic definida pelo Copom - Freq. diária - Unid. % a.a.
selic = sgs.get({'selic' : "432"}, start = "1999-01-01")

# Trimestraliza a série
selic_t = (
    selic
    .resample('Q') # resample da data para trimestral
    .last() # captura o último valor do trimestre
    .reset_index()
    .assign(date_quarter = lambda x : pd.PeriodIndex(x.Date, freq = 'Q'))
    .drop('Date', axis = 1)
  )

selic_t

'''2.2 Meta de Inflação

# Meta para a inflação - CMN - Freq. anual - %'''
meta = sgs.get({'meta' : "13521"}, start = "1999-01-01")
meta

# Trimestraliza a série
meta_t = (
    meta
    .loc[np.repeat(meta.index.values, 4)]
    .reset_index()
    .assign(date_quarter = lambda x: pd.date_range(start = x['Date'].iloc[0],
                   periods = len(x),
                   freq = 'Q').to_period('Q')
    )
    .loc[:, ['date_quarter', 'meta']]
  )

meta_t

# Expandindo amostra com dados de meta futura de inflação
new_rows = pd.DataFrame({
    'date_quarter': pd.date_range(start = '2022-01-01', periods = 24, freq = 'Q').to_period('Q'),
    'meta': np.repeat([3.5, 3.25, 3, 3, 3, 3], 4)
  })

# Junta as metas
meta_inflacao = pd.concat([meta_t, new_rows]).drop_duplicates(subset = "date_quarter")


'''2.3 Hiato do Produto'''
# Coleta e tratamento do Hiato do Produto do BC
hiato = (
    pd.read_excel(
    "https://www.bcb.gov.br/content/ri/relatorioinflacao/202312/ri202312anp.xlsx",
    sheet_name = "Graf 2.2.4",
    skiprows = 8
    )
    .assign(date_quarter = lambda x: pd.PeriodIndex(x['Trimestre'], freq = 'Q'),
            hiato = lambda x: x.Hiato.astype(float))
    .loc[:, ['date_quarter', 'hiato']]
    .dropna()
  )

hiato


'''2.4 Inflação'''
[ ]
# Função para acumular os trimestres
def acum_quarter(x):
    """
    Acumula a variação percentual mensal em um trimestre.

    Argumentos:
    - x: lista, array ou série pandas contendo os valores de inflação.

    Retorno:
    - A inflação acumulada em um trimestre, em porcentagem.
    """

    # Transforma os valores em fatores de crescimento
    x_fac = 1 + (x / 100)

    # Calcula o produto acumulado dos últimos três valores
    x_cum = np.prod(x_fac[-3:])

    # Calcula o valor acumulado em um trimestre
    x_qr = (x_cum - 1) * 100

    return x_qr

# Função para anualizar os valores trimestrais
def acum_p(data, n):
    """
    Calcula a acumulação de variações percentuais em janelas móveis.

    Argumentos:
    - data: array-like
        Uma sequência de dados representando variações percentuais.

    - n: int
        O tamanho da janela móvel para o cálculo da acumulação.

    Retorno:
    - array
        Um array contendo a acumulação das variações percentuais em janelas móveis.
    """

    resultado = (((data / 100) + 1)
                 .rolling(window=n)
                 .apply(np.prod)
                 - 1) * 100
    return resultado

# Coleta dados do ipca mensal
ipca = sgs.get({'ipca' : 433}, start = '1999-01-01')

ipca_12m = (
    ipca
    .reset_index()
    # cria colunas de trimestre
    .assign(date_quarter = lambda x: pd.PeriodIndex(x['Date'], freq = 'Q'))
    # agrupa por trimestre e acumula os valores percentuais do período
    .groupby(by = 'date_quarter')
    .agg({
        'ipca': lambda x: acum_quarter(x)
    })
    .reset_index()
    # calcula o produto móvel de 4 trimestres
    .assign(ipca_12m = lambda x: acum_p(x.ipca, n = 4))
    .drop('ipca', axis = 1)
    )

ipca_12m

'''2.5 Juro Neutro'''
# Cria uma função para a equação de fisher
def fisher(juros, inflacao):
    """
    Calcula a taxa de juros real neutra usando a equação de Fisher.

    Args:
        juros (float): A taxa de juros nominal em porcentagem (%).
        inflacao (float): A taxa de inflação em porcentagem (%).

    Returns:
        float: A taxa de juros real em porcentagem (%).

    Raises:
        TypeError: Se os argumentos `juros` e `inflacao` não forem do tipo `float`.

    Exemplo:
        >>> fisher(10, 3)
        6.796116504854364
    """
    juros = ((((1 + (juros / 100)) / (1 + inflacao / 100))) -1) * 100
    return juros

# Cria função para calcular a data de referência a partir da data de observação
def reference_date(date: str, n):
    """
    Calcula a data de referência adicionando 3 anos a uma data de observação.

    Args:
        date (str): Uma string que representa uma data no formato 'YYYY-MM-DD'.

    Returns:
        List[str]: Uma lista de strings com a data de referência no formato 'YYYY'.

    Raises:
        TypeError: Se o argumento `date` não for uma string.

    Examples:
        >>> reference_date('2022-01-01', n = 3)
        ['2025']
    """
    years = pd.DatetimeIndex(date).year.values + n # Calcula n anos a frente
    years = years.tolist()
    years = [str(i) for i in years]
    return years

'''Expectativa do IPCA'''
# instância a classe de Expectativas
em = Expectativas()

# Conecta com a API das Expectativas de Mercado Anuais
exp_anual = em.get_endpoint('ExpectativasMercadoAnuais')

# Importa as expectativas do IPCA anuais e realiza os filtros
ipca_e_raw = (
  exp_anual.query()
  .filter(exp_anual.Indicador == "IPCA")
  .filter(exp_anual.baseCalculo == 0)
  .select(exp_anual.Data, exp_anual.Mediana, exp_anual.DataReferencia)
  .collect()
  )

# Realiza o filtro para a data de referência 4 anos a frente das obs.
ipca_e_t4 = ipca_e_raw[(
            ipca_e_raw
            .DataReferencia == reference_date(ipca_e_raw['Data'], n = 4)
            )]


# Renomeia as colunas e mensaliza
ipca_e_t4 = (
              ipca_e_t4.rename(columns =
                                        {'Data' : 'date',
                                        'Mediana' : 'ipca_e_t4'})
              .drop(['DataReferencia'], axis = 1)
              .assign(date = lambda x: pd.PeriodIndex(x['date'], freq = 'M'))
              .loc[:, ['date', 'ipca_e_t4']]
              .groupby(by = 'date')
              .agg(ipca_e_t4 = ('ipca_e_t4', 'mean'))
              .reset_index()
              .assign(date = lambda x : x.date.dt.to_timestamp())
            )


'''Expectativa da SELIC'''
# Importa as expectativas da Selic anuais e realiza os filtros
selic_e_raw = (
   exp_anual.query()
  .filter(exp_anual.Indicador == "Selic")
  .filter(exp_anual.baseCalculo == 0)
  .select(exp_anual.Data, exp_anual.Mediana, exp_anual.DataReferencia)
  .collect()
  )

# Realiza o filtro para a data de referência 4 anos a frente das obs.
selic_e_t4 = selic_e_raw[(
                        selic_e_raw
                        .DataReferencia == reference_date(selic_e_raw['Data'], n = 4)
                        )]

# Renomeia as colunas
selic_e_t4 = (
              selic_e_t4.rename(columns =
                                        {'Data' : 'date',
                                        'Mediana' : 'selic_e_t4'})
              .drop(['DataReferencia'], axis = 1)
              .assign(date = lambda x: pd.PeriodIndex(x['date'], freq = 'M'))
              .loc[:, ['date', 'selic_e_t4']]
              .groupby(by = 'date')
              .agg(selic_e_t4 = ('selic_e_t4', 'mean'))
              .reset_index()
              .assign(date = lambda x : x.date.dt.to_timestamp())
            )

'''Proxy Neutro T4
Temos então a medida Rn|focus4t=Rfocus4t abaixo'''
# Junta os dados em um data frame
proxy_neutro_t4 = (
                pd.merge(left = ipca_e_t4,
                        right = selic_e_t4,
                        how = 'inner',
                        on = 'date')
                .assign(neutro_t4 = lambda x : fisher(x.selic_e_t4, x.ipca_e_t4))
                )

# Trimestraliza o juro neutro
proxy_neutro_t4 = (
    proxy_neutro_t4
    .assign(date_quarter = lambda x: pd.PeriodIndex(x['date'], freq = 'Q'))
    .loc[:, ['date_quarter', 'neutro_t4']]
    .groupby(by = 'date_quarter')
    .agg(neutro = ('neutro_t4', 'mean'))
)

# Calcula o filtro HP
filtro_hp = sm.tsa.filters.hpfilter(x = proxy_neutro_t4['neutro'], lamb = 1600)

# Salva a tendência calculada
proxy_neutro_hp = pd.DataFrame(filtro_hp[1]).reset_index() # posição 1 é a tendência (0=ciclo);


'''2.5 Reunir os dados'''

# lista de dataframes
dados_regs = [selic_t, meta_inflacao, hiato, ipca_12m, proxy_neutro_hp]
print(dados_regs, '01')

# reduz os dataframes pela chave 'date_quarter' com left join
dados_reg = reduce(lambda left, right: pd.merge(left, right, on = 'date_quarter', how = 'outer'), dados_regs)
dados_reg

'''2.5 Cria defasagens'''
# cria as colunas com os lags
## Defasagens da Selic
dados_reg['selic_lag1'] = dados_reg['selic'].shift(1)
dados_reg['selic_lag2'] = dados_reg['selic'].shift(2)
dados_reg['selic_lag3'] = dados_reg['selic'].shift(3)
dados_reg['selic_lag4'] = dados_reg['selic'].shift(4)
# Desvio da Meta (IPCA)
dados_reg['desvio_ipca'] = dados_reg['ipca_12m'] - dados_reg['meta']
# Defasagem do Hiato
dados_reg['hiato_lag1'] = dados_reg['hiato'].shift(1)

# Remove as linhas com valores ausentes
dados_reg_na = dados_reg.dropna()

# Transforma data em datetime
dados_reg_na_copy = dados_reg_na.copy ()
dados_reg_na_copy ['date_quarter'] = dados_reg_na_copy ['date_quarter'].dt.to_timestamp (freq = 'Q')


# Coloca a data no índice
dados_reg_na = dados_reg_na_copy.set_index('date_quarter')

dados_reg_na

'''3. Criação dos Modelos'''
# Especificação
eq_taylor_simples = sm.OLS.from_formula('selic ~ 1 + desvio_ipca + hiato', data = dados_reg_na, subset = dados_reg_na.index >= '2015-01-01').fit()
[ ]
# Especificação
eq_taylor_bcb = sm.OLS.from_formula('selic ~ -1 + selic_lag1 + selic_lag2 + desvio_ipca + hiato_lag1', data = dados_reg_na, subset = dados_reg_na.index >= '2015-01-01').fit()
[ ]
theta1 = eq_taylor_bcb.params['selic_lag1']
theta2 = eq_taylor_bcb.params['selic_lag2']
theta3 = eq_taylor_bcb.params['desvio_ipca']
theta4 = eq_taylor_bcb.params['hiato_lag1']

eq_taylor1 = theta1 * dados_reg_na['selic_lag1'] + theta2 * dados_reg_na['selic_lag2']

eq_taylor2 = (1 - theta1 - theta2) * ((dados_reg_na['neutro_trend'] + dados_reg_na['meta']) + theta3 * (dados_reg_na['desvio_ipca']) + theta4 * (dados_reg_na['hiato_lag1']))

eq_taylor = eq_taylor1 + eq_taylor2 + eq_taylor_bcb.resid
'''Visualiza os Resultados'''
# Cria o df com valores ajustados e a selic real
results = pd.DataFrame({'taylor_simples' : eq_taylor_simples.fittedvalues,
              'taylor_bcb' : eq_taylor,
              'Selic' : dados_reg_na.selic})

# Transforma de wide para long
results_long = results.melt(ignore_index = False).reset_index()
results_long = results_long.query('date_quarter > "2015-01-01"')

# Criação do gráfico
graf = ggplot(results_long, aes(x = 'date_quarter', y = 'value', color = 'variable')) + \
        geom_line(size = 1) + \
        theme_minimal() + \
        scale_color_manual(values = ['#eace3f', '#224f20', '#b22200', 'black', "#666666"]) + \
        scale_x_datetime(date_breaks = '6 months', date_labels = "%Y") + \
        labs(
            title = 'Meta da Taxa de Juros Nominal do Brasil (Selic) x Ajustes da Regra de Taylor',
            subtitle = 'Regra de Taylor Simples e Regra de Taylor com Suavização (BCB)',
            x = "",
            y = 'a.a.%',
            color = "",
            caption = 'Elaborado por analisemacro.com.br | Fonte: BCB') + \
        theme(legend_position = 'bottom',
                figure_size = (10, 7))

ggplot.draw(graf, show=True)

