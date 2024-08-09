# Importar a biblioteca scikit-learn e a classe LinearRegression
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from datetime import datetime

# Selecionando os dados do load_boston
goau = pd.read_csv('C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Área de Trabalho\\Códigos B3\\Planilhas\\Preços Empresa GOAU4_V1.csv', sep=';')

# Criar um objeto da classe LinearRegression
reg = LinearRegression()

# Separar os dados em variáveis independentes (X) e variável dependente (y)
# você precisa usar um colchete para juntar as duas colunas do dataframe goau, o que resulta em um array bidimensional.
X = goau[['Open', 'Volume', 'High']].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True)
y = goau['Close'].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True)
data = goau['Date']


# Definir a coluna data como o índice do dataframe goau
goau.set_index('Date', inplace=True)

# Converter os dados de X e y em arrays do numpy
X = np.array(X, dtype=float)
y = np.array(y, dtype=float)

# Remodelar os arrays para terem duas dimensões
# Usar o argumento 2 para que o numpy crie duas dimensões no array X
# Usar o argumento -1 para que o numpy calcule o tamanho automaticamente
X = X.reshape(-1, 4)
y = y.reshape(-1, 1)

# Criando um modelo KMeans com 2 clusters
kmeans = KMeans(n_clusters=4, n_init=5000)

# Treinando o modelo com os dados
kmeans.fit(X)

# Treinar o modelo com os dados usando o método fit
reg.fit(X, y)

# Obter os coeficientes e o intercepto do modelo
print("Coeficientes:", reg.coef_)
print("Intercepto:", reg.intercept_)

# Fazer previsões com novos dados usando o método predict

X_new = X
y_pred = reg.predict(X)
print("Previsão:", y_pred)

# Criar um dataframe com as datas e as previsões
df_pred = pd.DataFrame({'Date': goau.index, 'Previsão': y_pred.flatten()})

# Definir a coluna data como o índice do dataframe df_pred
df_pred.set_index('Date', inplace=True)

# Exibir o dataframe com as datas e as previsões
print(df_pred)

# Fazer o merge dos dataframes goau e df_pred pelo índice. Usar left_index=True e right_index=True como parâmetros
df_fim = goau.merge(df_pred, left_index=True, right_index=True, how='inner')

print(df_fim)

agora = datetime.now().strftime("%Y%m%d__%H_%M_%S")

Arquivo =f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Área de Trabalho\\Códigos B3\\Planilhas\\Regressao Linear "+ str(agora) +".csv"

#Arquivo=f"C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Autorregulação\\BBCE\\Acompanhamento de Mercado\\df_condicao2.csv"
df_fim.to_csv(Arquivo, sep=';',decimal=',',index=True,encoding="latin1")

# Converter as colunas 'Previsão' e '    Close    ' em dados numéricos usando o método astype() e tirar os R$ e , da coluna Close
df_fim['Previsão'] = df_fim['Previsão'].astype(float)
df_fim['    Close    '] = df_fim['    Close    '].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True)
df_fim['    Close    '] = df_fim['    Close    '].astype(float)

# Importar a biblioteca scipy e a função interp1d
from scipy import interpolate

# Criar uma função de interpolação com os dados de 'Previsão' e 'Close'
f = interpolate.interp1d(df_fim['Previsão'], df_fim['Close'])

# Criar um array de novos valores de X para interpolar
xnew = np.linspace(min(df_fim['Previsão']), max(df_fim['Previsão']), num=246)

# Calcular os valores interpolados de Y para os novos valores de X
ynew = f(xnew)

# Plotar o gráfico de análise por linhas, sendo uma de cor vermelha e a outra cor azul
plt.scatter(x=df_fim['Previsão'], y=df_fim['    Close    '], marker="o", color="red", s=200)
plt.scatter(x=df_fim['    Close    '], y=df_fim['Previsão'], marker="*", color="cyan", s=200)
plt.xlabel("Previsão\n", rotation=0, labelpad=-20, loc="left")
plt.ylabel("")
plt.grid(True, axis="y")


plt.title('Análise por linhas')
plt.legend()
plt.show()


'''Coeficiente de Determinação (R2 Score)
O coeficiente de Determinação (R²) varia entre 0 e 1 e expressa a quantidade da variância dos dados 
que é explicada pelo modelo linear. Explicando a variância da variável dependente a partir da 
variável independente. No nosso exemplo o R² = 0,99 significa que o modelo linear explica 99% da 
variância da variável dependente a partir da variável independente.'''

print('R2 Score: %.2f' % r2_score(y, y_pred))

'''Erro Médio Absoluto (Mean Absolute Error)
O erro médio absoluto (MAE) é a média da soma de todos os **E** do nosso gráfico de erros, as sua análise 
sofre uma interferência devido aos erros positivos e negativos se anularem.'''


print('MAE: %.2f' % mean_absolute_error(y, y_pred))

'''Erro Quadrado Médio (Mean Squared Error)
O erro quadrado médio (MSE) é a média da soma de todos os *E* elevados ao quadrado do nosso gráfico,
o fato de ele ter as diferenças elevadas ao quadrados resolve o problema de os erros positivos e
negativos se anulam, sendo mais preciso que o MAE.'''


print('Mean squared error: %.2f' % mean_squared_error(y, y_pred))
