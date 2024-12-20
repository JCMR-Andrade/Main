# Importando as bibliotecas
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression, LassoLarsCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.cluster import KMeans
import numpy as np

goau = pd.read_csv('C:\\Users\\julio.andrade\\OneDrive - bbce.com.br\\Área de Trabalho\\Códigos B3\\Planilhas\\Preços Empresa GOAU4_V1.csv', sep=';')

# Atribuindo as variáveis data, abertura, fechamento e volume os seus valores correspondentes
data, abertura, fechamento, volume = goau['Date'],  goau['    Open    '].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True), / 
                                     goau['    Close    '].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True), /
                                     goau['    High    '].replace('\.', '', regex=True).replace('R\$', '', regex=True).replace(',', '.', regex=True)

# Transformamos os dados em DTYPE FLOAT 64 Para Análise
goau['Data'] = data
goau['Abertura'] = abertura.astype('float64')
goau['Price'] = fechamento.astype('float64')
goau['Volume'] = volume.astype('float64')
print(goau)

X = goau[['Abertura']]
y = goau.Price

# Criando um modelo KMeans com 2 clusters
kmeans = KMeans(n_clusters=2, n_init=5000)

# Treinando o modelo com os dados
kmeans.fit(X)

# Obtém os labels dos clusters para cada ponto
labels = kmeans.labels_

# Imprimindo os labels
print(labels)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.80, random_state=None, shuffle=False)

# Criando um objeto LASSOLARSCV
lasso_cv = LassoLarsCV(fit_intercept=True, cv=5, max_iter=5000)

# Ajustando o objeto LASSOLARSCV aos dados de treino
lasso_cv.fit(X_train, y_train)

# Obtendo o valor de alpha
alpha = lasso_cv.alpha_

# Criando o modelo LinearRegression com o mesmo valor de fit_intercept e normalize=False
regr = LinearRegression(fit_intercept=False, normalize=False)

# Ajustando o modelo LinearRegression aos dados de treino, usando o valor de alpha como pesos
regr.fit(X_train, y_train, sample_weight=alpha)

# Realizando predição com os dados separados para teste
y_pred = lasso_cv.predict(X_test)

# Visualização dos 20 primeiros resultados
y_pred[:20]

# Tirando INFOS dos Dados Inseridos No DataFrame
# goau.info()

'''Erro Médio Absoluto (Mean Absolute Error)
O erro médio absoluto (MAE) é a média da soma de todos os **E** do nosso gráfico de erros, as sua análise 
sofre uma interferência devido aos erros positivos e negativos se anularem.'''


print('MAE: %.2f' % mean_absolute_error(y_test, y_pred))

'''Erro Quadrado Médio (Mean Squared Error)
O erro quadrado médio (MSE) é a média da soma de todos os *E* elevados ao quadrado do nosso gráfico,
o fato de ele ter as diferenças elevadas ao quadrados resolve o problema de os erros positivos e
negativos se anulam, sendo mais preciso que o MAE.'''


print('Mean squared error: %.2f' % mean_squared_error(y_test, y_pred))

'''Coeficiente de Determinação (R2 Score)
O coeficiente de Determinação (R²) varia entre 0 e 1 e expressa a quantidade da variância dos dados 
que é explicada pelo modelo linear. Explicando a variância da variável dependente a partir da 
variável independente. No nosso exemplo o R² = 0,99 significa que o modelo linear explica 99% da 
variância da variável dependente a partir da variável independente.'''

print('R2 Score: %.2f' % r2_score(y_test, y_pred))

'''Visualizando os resultados da regressão linear com scikit-learn
Podemos no gráfico abaixo, os pontos pretos que representam os nossos dados reais e em azul a 
reta de regressão linear do nosso modelo.'''

plt.scatter(X_test, y_test,  color='black')
plt.plot(X_test, y_pred, color='blue', linewidth=3)
plt.show()

goau.head(2)

# Avaliando a acurácia do modelo
accuracy = accuracy_score(X_test, y_pred)
print('Acurácia:', accuracy)
