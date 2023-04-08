# Churn Prediction
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

![11](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/11..png)

![12](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/12..png)

Notamos que as duas categorias possuem distribuições muito parecidas para diferentes variáveis, sendo, no geral, aproximações de distribuição normal.

Tendo adquirido um entendimento melhor de como os dados estão distribuídos, seguiremos para a etapa de construção dos modelos. Vamos observar como os classificadores se comportam com essas distribuições.

## 2. Aplicando diferentes modelos de classificação

É possível notar que o dataset está em um estado de desbalanceamento, isto é, a quantidade de clientes que não entraram em churn é muito maior dos que entraram, e possui features com pequenas nuances de classificação, podendo ser difícil para um modelo de classificação distinguir entre as duas classes.

### 2.1 Logistic Regression

Em primeiro momento, vamos utilizar o modelo de Regressão Logística e a técnica de validação cruzada para avaliar como o modelo se comporta com relação aos dados de treinamento. Em seguida, vamos saber como o modelo generaliza para os dados de teste ainda não vistos.

![13](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/13..png)

![14](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/14..png)

O desempenho do modelo na validação cruzada de 5 folds teve um desempenho bom de acurácia média, porém um desempenho muito ruim nas outras métricas, especialmente no recall. Isso ocorre porque em casos de datasets muito desbalanceados, como esse em que a maioria dos clientes estão classificados como 0 (não churn), o modelo apresenta uma alta acurácia simplesmente prevendo a classe majoritária, e não leva em conta a classe minoritária que é o principal interesse nesse caso. Logo, a acurácia não é um bom indicador de desempenho do modelo nessa situação.

O recall e a precisão apresentaram scores muito ruins na validação cruzada e ainda piores nos dados teste.

A matriz de confusão nos mostra que: 692 amostras foram classificadas corretamente como não-churn (verdadeiro negativo); 28 amostras foram classificadas corretamente como churn (verdadeiro positivo); 92 amostras foram erroneamente classificadas como não-churn (falso negativo); 32 amostras de não-churn foram erroneamente classificadas como churn (falso positivo).

#### Ajustando hiperparâmetros da RegLog

Com o objetivo de tentar obter um valor de recall mais alto para que o modelo preveja mais valores da classe minoritária, vamos tentar ajustar os hiperparâmetros da Regressão Logística

Primeiro vamos visualizar como a curva de validação em relação ao recall se comporta quando variamos os parâmetros 'C' e 'max_iter'

![15](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/15..png)

![16](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/16..png)

A sombra que é plotada na área preenchida representa o intervalo de confiança para a variação da pontuação do modelo entre as diferentes dobras de validação cruzada. Essa faixa sombreada é comumente usada para indicar a incerteza associada à estimativa da pontuação do modelo.

Vamos utilizar o StratifiedKFold para que a proporção de amostras de cada classe seja preservada em cada fold. Essa é uma abordagem mais adequada em problemas de classificação com dados desbalanceados.

Em seguida, vamos usar o GridSearchCV para tentar econtrar uma combinação de parâmetros que seja adequada para maximizar o recall

![17](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/17..png)

![18](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/18..png)

![19](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/19..png)

Observamos que a busca pelos melhores hiperparâmetros de fato maximizou o recall, porém, às custas da precisão. Isto é, o modelo classificou muito mais falsos positivos do que no caso anterior, decaindo, assim, a precisão e, consequentemente, o f1 score.

#### Aplicando SMOTE
Agora vamos tentar aplicar a técnica de oversampling SMOTE que consiste em criar novas amostras sintéticas da classe minoritária a partir das amostras já existentes a fim de balancear o conjunto de dados

![20](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/20..png)

![21](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/21..png)

![22](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/22..png)

O modelo treinado com o SMOTE e o grid search superestimou a classe positiva quando aplicado nos dados de teste. É possível que a configuração de parâmetros encontrada pelo GridSearchCV seja muito específica para o conjunto de treinamento, levando a um overfitting do modelo.

#### Adicionando algumas features
Como o SMOTE não se adequou bem a esse problema, vamos adicionar mais algumas features no conjunto de dados para tentar ajudar o modelo a entender as nuances da variável alvo.

Features adicionadas

'prop_minutos_dia': proporção de chamadas feitas durante o dia em relação ao total de chamadas.

'total_chams': total de chamadas feitas por cliente considerando chamadas noturnas, internacionais, etc.

'total_minutos': total de minutos gastos.

'avg_minutes_per_call': média de minutos por ligação.

'range_num_meses_prov_atual': faixas de valores para a coluna 'num_de_meses_prov_atual' ['0-25', '26-50', '51-75', '76-100', '+100']

'avg_cobr_dia_por_min': média de cobrança dia por minuto.

'avg_cobr_notu_por_min': média de cobrança noturna por minuto.

'avg_cobr_noit_por_min': média de cobrança noite por minuto.

'avg_cobr_inter_por_min': média de cobrança internacional por minuto.

![23](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/23..png)

![24](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/24..png)

Embora a adição de algumas features tenha melhorado razoavelmente a performance do modelo, a precisão e o recall ainda ficaram abaixo de um valor razoável.

Vamos avaliar a performance de outros modelos mais robustos para lidar com a questão do desbalanceamento

### 2.2 Decision Tree
![25](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/25..png)

![26](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/26..png)

Percebemos uma melhora no equilibro entre precisão e recall, além de uma melhoria na precisão e recall em relação a classe 0, e também na acurácia total do modelo. Porém, ainda há espaço para tentar melhorar os valores em relação à classe 1.

Vamos visualizar como essas métricas se comportam com a variação de alguns hiperparâmetros importantes da árvore de decisão

![27](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/27..png)

![28](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/28..png)

![29](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/29..png)

Agora que temos uma base dos valores dos parâmetros que maximizam cada métrica, vamos fazer uma busca no GridSearchCV para achar uma combinação que maximize o recall

![30](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/30..png)

![31](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/31..png)

![32](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/32..png)

Observamos que a média de recall na validação cruzada foi de 0.73, e nos dados de teste o modelo acertou 71% das previsões positivas corretamente, não muito diferente da versão anterior. A precisão para a classe 1, no entanto, teve uma melhora significativa com o ajuste, tornando-se um pouco melhor do que a versão anterior.

Por fim, vamos analisar o desempenho do modelo de floresta aleatória e ver como ele se comporta

### 2.3 Random Forest

![33](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/33..png)

![34](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/34..png)

Vemos que o Random Forest obteve 0.99 de precisão para a classe 1 e recall máximo para a classe 0 nos dados de teste. Entretanto, o recall para a classe 1 se mostrou um pouco abaixo se comparado com a Árvore de Decisão.

Vamos aplicar a técnica de balanceamento SMOTETomek dessa vez. Ela combina o algoritmo SMOTE com o algoritmo Tomek Links, tendo por objetivo gerar novas amostras sintéticas da classe minoritária e em seguida remover as amostras da classe majoritária que estão próximas a amostras da classe minoritária.

Vamos usar também a técnica de RepeatedStratifiedKFold para a validação cruzada. A vantagem em relação à StratifiedKFold é que a RepeatedStratifiedKFold realiza a validação cruzada várias vezes, criando uma divisão aleatória do conjunto de dados em cada repetição, ajudando a reduzir a variância do processo.

![35](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/35..png)

![36](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/36..png)

#### Ajustando alguns hiperparâmetros

![37](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/37..png)
![38](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/churn-prediction-2020-project/imagens-churn-prediction-2020/38..png)

## Avaliação dos resultados

Com relação aos modelos utilizados, enquanto a Regressão Logística apresentou baixa performance para o problema de desbalanceamento de classes, a Árvore de Decisão e o Random Forest conseguiram lidar um pouco melhor com esse problema, sendo o Random Forest o modelo que melhor conseguiu equilibrar o trade-off entre recall e precisão com um valor razoável em relação a classe positiva, fazendo o uso da técnica de over-sampling e ajustando alguns hiperparâmetros.

## Conclusão

Ao final deste projeto, pudemos observar, de modo geral, que os três modelos tiveram suas dificuldades em detectar a classe positiva, o que nos leva a considerar a importância do tratamento de dados desbalanceados em problemas de classificação e a utilização de modelos mais avançados e robustos. A falta de representatividade de uma classe pode levar a modelos tendenciosos e com baixa capacidade de generalização. No entanto, ainda que com valores não totalmente satisfatórios de recall, o modelo de Random Forest, a exemplo, pode ser utilizado para ajudar a reter uma certa quantidade de faturamento para a empresa em questão. Isto é, uma porcentagem de 80 no recall e 96 na acurácia pode reter 'x' milhões de faturamento, bem como uma porcentagem de 90 no recall reterá 'y' milhões, e assim por diante.

A utilização de modelos mais avançados como Gradient Boosting e Redes Neurais pode ser utilizado para avaliação de performance nesse conjunto de dados, visto que são classificadores que lidam bem com o problema de desbalanceamento, porém essa abordagem está fora do escopo desse projeto. 

## Referências 

[1]. Rahim Baig, Mirza, et al. Data Science for Marketing Analytics. 2st ed. Birmingham B3 2PB, UK: Packt Publishing Ltd, 2021.

[2]. https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

[3]. https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html

[4]. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
