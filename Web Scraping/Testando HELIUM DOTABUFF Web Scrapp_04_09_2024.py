import pandas as pd
from helium import *
import itertools

# Inicia o navegador e abre a página
start_chrome('https://pt.dotabuff.com/players/36423302/matches?enhance=overview', headless=False)

list1 = []
list2 = []
list3 = []
list5 = []

try:
    while True:
        # Encontra todos os elementos que contêm os links e títulos das matérias
        articles = find_all(S('.cell-large', below='Herói'))
        resultados = find_all(S('a', below='Resultado'))
        emas = find_all(S('.kda-record', below='EMA'))

        for ema in emas:
            ema_text = ema.web_element.text
            list3.append(ema_text)
        
        for article in articles:
            title = article.web_element.text
            # Usando split() para separar a string
            partes = title.split('\n')
            heroi = partes[0].strip()  # Remove espaços em branco extras
            rank = partes[1].strip()   # Remove espaços em branco extras
            list1.append(heroi)
            list5.append(rank)

        for resultado in resultados:
            resultado_text = resultado.web_element.text
            result = resultado_text.capitalize()
            list2.append(result)

        # Verifica se há um botão de próxima página e clica nele
        next_button = S('.next')  # Use um seletor mais robusto, se possível
        if next_button.exists():
            print("Clicando no botão de próxima página...")
            click(next_button)
            wait_until(lambda: next_button.exists(), timeout_secs=5)  # Aumente o tempo de espera
        else:
            print("Botão de próxima página não encontrado ou não existe.")
            break
except Exception as e:
    print(f"Erro ao tentar navegar para a próxima página: {e}")

# Cria os DataFrames e exibe os resultados
df1 = pd.DataFrame(list1)
df2 = pd.DataFrame(list2)
df3 = pd.DataFrame(list3)
df5 = pd.DataFrame(list5)
df = list(itertools.zip_longest(list1, list5, list2, list3, fillvalue=None))

colunas = ['Herói', 'Rank', 'Resultado', 'KDA']
dfp = pd.DataFrame(df).dropna()

dfp.columns = colunas
print(dfp)

kill_browser()
