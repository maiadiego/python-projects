# Sales Prediction
## Problema de negócio
<p align="justify"> A previsão de vendas adquiriu grande importância em diversos nichos de mercado ao longo do tempo, e vem se mostrando um fator fundamental para uma empresa que busca obter alguma margem de confiabilidade em relação a valores de receita futuros em seu negócio. Alguma das razões pelas quais a <em> sales prediction </em> é importate são: </p>

* **Planejamento financeiro** <p align="justify"> Estimar o fluxo de caixa futuro e estar preparado para receitas e despesas esperadas, tais como: alocação de recursos, obtenção de financiamento e a gestão do capital de giro. </p>
* **Tomadas de decisões estratégicas** <p align="justify"> Definir metas de vendas, desenvolver estratégias de marketing e definir preços futuros. </p>
* **Gerenciamento de estoque e cadeia de suprimentos** <p align="justify"> Determinar os níveis adequados para atender a demanda dos clientes, evitando ao mesmo tempo excesso de estoque ou falta de produtos.</p>
* **Planejamento de produção** <p align="justify"> Determinar a capacidade necessária, os recursos necessários e os cronogramas de produção. Isso ajuda a evitar gargalos na produção e a otimizar a eficiência operacional.</p>
* **Atendimento ao cliente** <p align="justify"> Dimensionamento adequado do atendimento ao cliente, o planejamento de recursos humanos e a gestão da capacidade de atendimento. </p>
## Overview
### Objetivo
Criar um modelo de previsão que nos gere uma margem confiável de vendas para certos períodos no futuro.
### Fonte de dados
<p align="justify"> Os dados usados são da <em> Corporación Favorita </em>, uma grande varejista de alimentos com sede no Equador. Eles operam centenas de supermercados, com mais de 200.000 produtos diferentes em suas prateleiras. </p>

https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting/data

### Etapas do projeto
**1. Análise exploratória dos dados** <p align="justify"> Visualização das categorias de produto, distribuição de vendas por cluster e atuação dos clusters nas diferentes cidades. </p>

**2. Análise das séries temporais** <p align="justify"> Comportamento das vendas ao longo dos anos e a influência de variáveis exógenas. </p>

**3. Modelagem e previsão** <p align="justify"> Configurar dois modelos que prevejam as vendas alguns passos no futuro e comparar a performance deles. </p>

### Modelos utilizados
Foram utilizados os modelos **ARIMA** e **SARIMAX**.

O notebook com o código completo do projeto se encontra em: 

## 1. Análise exploratória dos dados 
<p align="justify"> Os dados fornecidos possuem quatro datasets a serem explorados: <strong> sales_df, stores_df, oil_df e holidays_df </strong>.
O primeiro dataset, sales_df, possui colunas informando id, data, número da loja, categoria, receita e quantidade de produtos em promoção relacionados a uma determinada venda. </p>

![sales_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/1.png) 

<p align="justify"> O dataset stores_df possui informações acerca da cidade e o estado em que uma determinada loja está situada, bem como o seu tipo e o número do cluster ao qual pertence. </p>

![stores_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/2.png)

<p align="justify"> O dataset oil_df possui as variações do preço do petróleo ao longo do tempo. Como o Equador é um país produtor de petróleo, o a alta no preço do óleo pode afetar o preço final das mercadorias vendidas pela varejista, isto é, devido aos custos de produção, custos de transporte, condições econômicas gerais, entre outros. </p>

![oil_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/3.png)

<p align="justify"> Já holidays_df possui especificações de todos os feriados ocorridos dentro do período em questão, lembrando que os feriados podem mudar o padrão de comportamento do consumidor e gerar comportamentos sazonais nas vendas.</p>

![holidays_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/4.png)

Todos os datasets compreendem o período entre os anos de 2013 a 2017.

Vamos checar como estão distribuídas as categorias dos produtos vendidos pela varejista

![sales_cat](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/5.png)

Vemos que grande parte das vendas se concentra em produtos de mercado e mercearia, bem como no setor de bebidas.

&nbsp;

<p align="justify"> A varejista se divide em clusters, isto é, agrupamento de lojas com características semelhantes com base em diferentes critérios, como localização, perfil demográfico dos clientes, comportamento de compra, concorrência local, entre outros. O objetivo de criar clusters é segmentar as lojas em grupos distintos para entender melhor o desempenho de cada grupo e desenvolver estratégias mais eficazes para alocar recursos, entender o ambiente competitivo local, analisar desempenho e traçar metas de expansão. </p>

Como um insight inicial, vamos visualizar qual foi a média de vendas de cada cluster 

![cluster-mean](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/6.png)

Vemos que o cluster 5 possui uma grande performance em relação às vendas.

Vamos como os clusters estão distribuídos entre a cidades e a margem de vendas de cada um

![cluster_at](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/7.png)

Observamos que os clusters com maior concentração de vendas ficam na capital, Quito.

## 2. Análise das séries temporais
Vamos explorar explorar as séries de vendas em termos de anos disponíveis

![s_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/8.png)

<p align="justify"> Observamos que o ano de 2014 teve um aumento considerável na margem das vendas em relação ao ano anterior, porém com um comportamento instável. No segundo semestre de 2015 a margem de vendas subiu e se manteu estável, repetindo o comportamento para os anos de 2016 e 2017.</p>

<p align="justify"> A fim de obter uma amostra dos dados menor e mais estável, vamos trabalhar somente com os dados do ano de 2016, filtrando pela categoria de bebidas, em rezão dos valores estarem em um escala não tão discrepante. </p>

![s_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/9.png)

<p align="justify"> É possível notar um padrão sazonal claro nos dados, o que fica mais evidente quando filtramos somente para os meses de janeiro e fevereiro </p>

![saso_2016](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/saso_2016.png)

Um ciclo sazonal tem aproximadamente sete dias, uma informação importante para ajudar na modelagem futura.

Vamos agora verificar se a quantidade de produtos promocionais tem algum poder de influência nas vendas

![s_3](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/10.png)

<p align="justify"> Observamos que em alguns picos de preços promocionais, as vendas obtiveram uma margem alta, porém em outros não. O que pode significar que a quantidade de produtos promocionais não é um fator tão determinante para uma margem de vendas alta.</p>

Vamos ver agora como as vendas se comportam com as flutuações no preço do óleo

![s_4](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/10b.png)

<p align="justify"> Durante meados de maio e começo de julho o preço do óleo teve grande aumento, concomitantemente a isso, a margem de vendas se estabeleceu em uma margem um pouco mais baixa.</p>

![s_5](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/10c.png)

<p align="justify"> Ao marcar os dias de feriados, vemos que entre abril e maio houve uma grande concentração de feriados, fazendo as vendas alcancarem uma margem que não foi observada em nenhum ciclo sazonal subsequente.</p>

Vamos decompor a série em tendência, sazonalidade e resíduos 

![s_6](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/11.png)

<p align="justify"> Como vemos, o primeiro gráfico é o valor real(observado) da série. No gráfico de tendência, é possível notar que não há nenhuma tendência constante ao longo dos anos. No gráfico sazonal, vemos qual a forma dos ciclos sazonais presentes, como observamos no gráfico mais acima. Com relação ao componente residual, ele representa a variação aleatória dos dados. É importante que não tenha nenhum padrão ou sazonalidade nos resíduos, tenham média zero e variação constante ao longo do tempo.</p>

<p align="justify"> O gráfico de autocorrelação (ACF) ajuda a identificar a presença de correlação entre os valores passados de uma série temporal e os valores atuais. Ele mostra como a série está correlacionada consigo mesma em diferentes defasagens.</p>

![s_7](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/12.png)

<p align="justify"> A presença de autocorrelação positiva em três defasagens seguidas seguida por autocorrelação negativa em quatro defasagens sugere um padrão cíclico recorrente na série temporal, mais especificamente, um período de sete dias, como vimos anteriormente. Isso pode indicar que os valores em uma semana são correlacionados positivamente com os valores três semanas anteriores, e correlacionados negativamente com os valores quatro semanas anteriores.</p>

<p align="justify"> Em relação às correlações positivas, uma correlação significativamente maior na defasagem do meio, em comparação com as duas defasagens, pode indicar a presença de um padrão específico na série temporal. Essa defasagem em destaque pode ter um efeito mais forte e relevante na previsão da série.Existem algumas possibilidades para esse padrão. Pode ser que haja um evento sazonal recorrente ou uma tendência específica que ocorre em uma determinada defasagem. Também pode ser uma indicação de que a série temporal tem uma dependência mais forte em uma defasagem específica, o que significa que a observação atual está correlacionada com uma observação passada exatamente nessa defasagem. </p>

<p align="justify"> Quando as autocorrelações estão dentro da faixa de confiança, isso indica que não há evidências estatísticas suficientes para concluir que essas autocorrelações são diferentes de zero. Portanto, elas são consideradas não significativas. Por outro lado, quando as autocorrelações extrapolam a faixa de confiança, isso indica que elas são estatisticamente significativas e sugerem uma dependência temporal na série.</p>

<p align="justify"> No contexto do  gráfico de autocorrelação, se as autocorrelações diminuem e entram dentro da faixa de confiança à medida que os lags aumentam, isso sugere que a dependência temporal na série se torna menos relevante à medida que o tempo avança. Em outras palavras, lags mais distantes têm autocorrelações não significativas, o que indica uma menor influência do passado distante na série temporal.</p>

Com base no gráfico acima, temos um  SAR (Seasonal AutoRegressive).

<p align="justify"> O PACF (Partial Autocorrelation Function) ajuda a identificar os termos autorregressivos significativos que contribuem para a estrutura da série temporal. </p>

![s_8](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/13.png)

<p align="justify"> As correlações são significativas nos primeiros lags e depois diminuem, tornando-se pouco significativas e dentro da faixa de confiança a partir do lag 20, isso pode indicar que há uma estrutura de autocorrelação significativa nos primeiros lags da sua série temporal, mas essa autocorrelação diminui à medida que as defasagens aumentam. </p>

<p align="justify"> A diminuição das correlações e sua entrada na faixa de confiança a partir do lag 20 indicam que as defasagens mais distantes não possuem uma influência significativa na série temporal. </p>

<p align="justify"> Portanto, com base no gráfico de autocorrelação parcial, um modelo AR com um número relativamente baixo de termos autorregressivos (provavelmente dentro dos primeiros lags significativos) pode ser suficiente para modelar e prever a série temporal. </p>


## 3. Modelagem e previsão

<p align="justify"> O teste ADF (Augmented Dickey-Fuller) é um teste estatístico usado para determinar se uma série temporal possui raiz unitária, o que indica a presença de tendência não estacionária nos dados. Esse teste é comumente usado para avaliar a estacionariedade de uma série temporal antes de aplicar modelos de séries temporais. </p>

<p align="justify"> No teste ADF, a hipótese nula (H0) assume que a série temporal possui uma raiz unitária e, portanto, não é estacionária. Se o valor-p calculado no teste for menor que um determinado nível de significância pré-definido (geralmente 0,05), a hipótese nula é rejeitada, o que indica que a série é estacionária. Por outro lado, se o valor-p for maior que o nível de significância, não há evidências suficientes para rejeitar a hipótese nula, indicando que a série é não estacionária.</p>

![adf_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/14.png)

<p align="justify"> No teste acima, vemos que o p-value(0.13) é maior que o nível de significância 0.05, indicando que a série é não estacionária.</p>

<p align="justify"> Para lidar com isso, vamos aplicar o processo de diferenciação, que é uma técnica comumente utilizada para transformar uma série temporal não estacionária em uma série estacionária. Envolve subtrair valores consecutivos da série temporal original, o que resulta em uma nova série composta pelas diferenças entre os valores. O objetivo é remover a tendência e a sazonalidade presente nos dados, tornando a série estacionária.</p>

![adf_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/15.png)

<p align="justify"> Após aplicar a diferenciação, o p-value se tornou muito menor que o nível de significância, concluindo que agora a série é estacionária.</p>

### 3.1 ARIMA
O proxímo passo é escolher um modelo que gere o menor AIC a partir dos parâmetros fornecidos.

<p align="justify"> O AIC (Akaike Information Criterion) é uma métrica utilizada para comparar diferentes modelos estatísticos e determinar qual deles apresenta o melhor equilíbrio entre ajuste aos dados e complexidade do modelo. O AIC é baseado na ideia de que um bom modelo deve fornecer um bom ajuste aos dados, mas também deve ser o mais parcimonioso possível, ou seja, não deve ser excessivamente complexo. Quanto menor o valor do AIC, melhor é o modelo, indicando um bom ajuste aos dados com menor complexidade.</p>

<p align="justify"> Usaremos uma função para treinar um modelo ARIMA com diferentes valores de p e q, parâmetros do ARIMA, a fim de visualizar qual que gera o menor AIC. </p>

O dataframe abaixo nos mostra o resultado

![aic_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/16.png)

<p align="justify"> Vemos que os parâmetros p=7 e q=7 gerou o menor AIC entre o range de valores, indicando que, dentre os modelos treinados, o que possui melhor equilíbrio entre ajuste e complexidade é aquele com os parâmetros p e q setados em 7. </p>

<p align="justify"> Antes de fazer as previsões, é necessário fazer uma análise residual no nosso modelo a fim de verificar se os nossos resíduos são classificados como ruído branco, isto é, se eles não estão correlacionados e são apenas flutuações aleatórias restantes que não podem ser modeladas.</p>

![res_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/17.png)

<p align="justify"> O primeiro gráfico mostra os resíduos do modelo ao longo do tempo. Espera-se que os resíduos sejam aproximadamente aleatórios, com média zero e variância constante. Se houver algum padrão nos resíduos, como tendência ou sazonalidade remanescente, isso pode indicar que o modelo não está capturando adequadamente a estrutura dos dados.</p>

<p align="justify"> O histograma dos resíduos é plotado para verificar se eles seguem uma distribuição normal. Idealmente, os resíduos devem se aproximar de uma distribuição normal com média zero. Desvios significativos da normalidade podem indicar a presença de padrões não capturados pelo modelo.</p>

<p align="justify"> O gráfico de densidade dos resíduos gráfico exibe a estimativa da densidade dos resíduos em comparação com uma distribuição normal teórica. Se os resíduos estiverem próximos da curva normal teórica, isso sugere que o modelo está capturando adequadamente a distribuição dos dados. Se os resíduos se aproximarem de uma reta que fica perto de y=x, então os resíduos se aproximam de uma distribuição normal. </p>

<p align="justify"> Por fim, o gráfico de autocorrelação dos resíduos nos mostra as autocorrelações dos resíduos em diferentes defasagens. Espera-se que as autocorrelações sejam próximas de zero e não apresentem padrões significativos.</p>

<p align="justify"> Ao analisar os quatro gráficos em conjunto, vamos que os resíduos se aproximam de uma distribuição normal no geral, apesar de não ser uma distribuição normal perfeita. </p>

<p align="justify"> Por fim, vamos aplicar o teste Ljung-Box. Ele é um teste estatístico utilizado para avaliar a autocorrelação residual em um modelo. É aplicado aos resíduos do modelo e é útil para verificar se há autocorrelação serial não capturada pelo modelo. A hipótese nula em relação ao teste afirma que os dados são independentemente distribuídos, o que significa que não há autocorrelação. Se o p-value for maior que 0.05, nós não podemos rejeitar a hipótese nula, significando que os resíduos são independentemente distribuídos e o modelo está pronto para fazer previsões. </p>

![lb_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/18.png)

<p align="justify"> Na figura acima, vemos que todos os valores de lb_pvalue dentro de um range de 10 lags são maiores que 0.05, o que significa que nosso modelo está pronto para fazer previsões. </p>

### 3.2 SARIMAX
<p align="justify"> Vamos agora examinar a performance do modelo SARIMAX utilizando variáveis exógenas. Como vimos na nossa análise anterior, as vendas no varejo podem ser afetadas por diferentes fatores, incluindo feriados, flutuações no preço do óleo, comportamento do consumidor, qualidade do produto, etc. Por conta disso, vamos selecionar algumas variáveis exógenas fornecidas na fonte de dados para passar para o modelo e tentar melhorar as previsões. </p>

<p align="justify"> Filtramos um dataset contendo as colunas feriado, preço do óleo e a quantidade de produtos em promoção para um certo dia dentro do ano de 2016. </p>

![ex_data](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/19.png)

Vamos checar quais parâmetros de p, q, P e Q nos gera o menor AIC

![aic_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/20.png)

Checando a análise residual

![res_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/21.png)

![lb_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/22.png)

<p align="justify"> Podemos ver que nos lags de 2 a 6 os p-values são menores que 0.05, indicando que ainda pode haver correlação entre os resíduos. No entanto, os últimos valores são maiores que 0.05 e, observando o gráfico de correlação residual, esse caso não nos impede necessariamente de fazer previsões, só nos diz que talvez o modelo não tenha capturado todos os padrões dentro dos dados de treinamento. </p>

<p align="justify"> Vamos ver agora como as previsões se comportam para alguns meses do segundo semestre de 2016 com base nos dados de treinamento do primeiro semestre.</p>

![pred](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/23.png)

![mape](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/24.png)

## Avaliação dos resultados
<p align="justify"> Vemos que, de fato, o ARIMA se ajustou um pouco melhor nesse caso, e o SARIMAX acabou superestimando as previsões em alguns pontos. O MAPE nos informa o percentual médio que as previsões se afastaram dos valores reais. A diferença de 2% pode ser muito importante num contexto de negócio que envolve milhares de dólares, por exemplo. No contexto da varejista que estamos tratando, essa diferença pode significar estoques superabastecidos ou até mesmo a falta de produtos para uma alta demanda. </p>

## Conclusão
<p align="justify"> Alguns insights interessantes que podemos extrair dessa análise é que prever vendas no varejo para uma quantidade longa no futuro pode ser desafiador. Há diversos fatores que influenciam no comportamento do consumidor e, em função disso, prever para quantidades cada vez menores de tempo pode gerar previsões mais acuradas, devido à alta volatilidade dos dados. Ao passo que, pode ser um tanto complicado no que se refere à menor quantidade do set de treinamento e a uma falta de tendência clara nos dados. </p>

## Referências 

[1]. Peixeiro, M. (2022). Time Series Forecasting in Python. Shelter Island, NY: Manning Publications.

[2]. https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html

[3]. https://www.statsmodels.org/devel/generated/statsmodels.tsa.arima.model.ARIMA.html
