## Problema de negócio
O *customer churn*, também conhecido como rotatividade de clientes, é um problema que ocorre quando os clientes param de fazer negócios com uma empresa. Isso pode acontecer por uma variedade de razões, como preços altos, problemas de atendimento ao cliente, baixa qualidade do produto ou serviço, entre outros. O churn pode ser particularmente problemático para as empresas, pois a aquisição de novos clientes pode ser mais cara do que manter os já existentes. Portanto, entender as razões pelas quais os clientes estão deixando a empresa e identificar aqueles com maior probabilidade de deixá-la pode ser crucial para reduzir o churn e manter o faturamento que os clientes geram. A análise de dados e a modelagem preditiva podem ajudar a prever o churn dos clientes e ajudar uma empresa a agir antecipadamente a fim de evitar que eles saiam.

## Overview
**Objetivo**: criar e avaliar a performance de três modelos de classificação para o problema de customer chrun. São eles: Regressão Logística, Árvore de Decisão e Floresta Aleatória.

**Fonte de dados**: O dataset utilizado foi de uma empresa de telecomunicações e está disponível em: www.kaggle.com/competitions/customer-churn-prediction-2020/data. Ele possui 4250 linhas, 19 features e a variável alvo ‘churn’. 

**Métricas de avaliação:**

*Accuracy*: proporção de previsões corretas em relação ao total de previsões realizadas.

*Precision*: proporção de verdadeiros positivos (VP) em relação a todas as previsões positivas (VP + FP).

*Recall*: proporção de verdadeiros positivos (VP) em relação a todas as amostras positivas (VP + FN). É uma medida de quão bem o modelo detecta as amostras positivas.

*f1*: média harmônica entre precisão e recall. É uma medida de equilíbrio entre precisão e recall.

*AUC-ROC*: medida da qualidade geral do modelo que mede o desempenho do modelo em discriminar entre as classes positiva e negativa. Valores mais próximos de 1 indicam um modelo com melhor desempenho. Geralmente, considera-se que um modelo com AUC-ROC maior que 0,5 é melhor do que um modelo aleatório.

**Etapas do projeto**

**1.** Análise exploratória dos dados

**2.** Aplicação dos modelos

**3.** Avaliação dos resultados 

O notebook completo do projeto se encontra em: 

## 1. Análise exploratória dos dados 
Cabeçalho e todas as colunas do dataset

![Cabeçalho](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/1.%20cabecalho-dataset.png)
![Colunas](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/colunas.png)

Vamos explorar melhor nossos dados para analisar as correlações entre as variáveis, as medidas de tendência central e a forma como os dados estão distribuídos 

![MC](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/2.%20matriz%20de%20correlacao.png)

Vemos que existe uma fraca correlação, tanto negativa quanto positiva, entre a maioria das variáveis do dataset, exceto pelas variáveis de cobrança que estão perfeitamente correlacionadas com as variáveis de minutos gastos nos tipos de ligação, o que faz sentido nesse contexto de negócio.

Agora vamos ter uma base numérica das medidas estatísticas

![Describe](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/3.%20describe.png)

Vamos explorar mais a variável alvo (churn) e sua relação com as outras variáveis da base de dados

![Ch](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/4.%20porcentagem%20de%20churn%20vs%20nchurn.png)

A imagem acima mostra a porcentagem de clientes que não entraram em churn (aproximadamente 86%) e a porcentagem dos clientes que entraram em churn (14%).

Vamos visualizar graficamente como algumas dessas variáveis estão distribuídas

![Uni1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/5.%20uni-1.png)

![Uni2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/6.%20uni-2.png)

As variáveis 'num_meses_prov_atual', 'total_chams_dia' e 'total_chams noturnas' se aproximam bem de uma distribuição normal, enquanto que 'num_msgs_correio_de_voz' possui a maior parte dos dados distribuída no valor zero, e 'num_chams_atend_clien' e 'total_chams_inter' possuem valores variados com uma frequência alta.

Vamos visualizar as distribuições multivariadas em relação à variável 'churn'

![State](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/7.%20churn-estado.png)

Vemos que a distribuição dos clientes que entraram em churn possui semelhanças entre vários estados. Naturalmente, alguns estados possuem taxas de churn mais altas em relação a outros, isso pode levar em conta outros fatores além da qualidade do serviço da empresa em si.

![cod](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/8.%20churn-cod-area.png)

Clientes com código de área 415 possuem uma taxa de churn ligeiramente maior do que clientes com os outros dois códigos.

![plan](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/9.%20churn-plan-inter.png)

![correio](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/10.%20churn-plan-corr.png)

Com base no último gráfico, vemos que há uma diferença mais significativa com relação ao churn entre os clientes que não possuem plano de correio de voz e os que possuem.

A seguir, vamos agrupar a média e a mediana em relação aos clientes que entraram em churn (yes) e os que não entraram (no). Em seguida, iremos visualizar a distribuição de algumas variáveis de acordo com essas duas categorias

![]()

![]()

