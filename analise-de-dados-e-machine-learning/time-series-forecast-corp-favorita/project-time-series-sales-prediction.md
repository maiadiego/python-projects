# Sales Prediction
## Problema de negócio
A previsão de vendas adquiriu grande importância em diversos nichos de mercado e vem se mostrando um fator fundamental para uma empresa orientada a dados. Alguma das razões pelas quais a *sales prediction* é importate são:
* **Planejamento financeiro**: estimar o fluxo de caixa futuro e estar preparado para receitas e despesas esperadas, tais como: alocação de recursos, obtenção de financiamento e a gestão do capital de giro.
* **Tomadas de decisões estratégicas**: definir metas de vendas, desenvolver estratégias de marketing e definir preços futuros.
* **Gerenciamento de estoque e cadeia de suprimentos**: determinar os níveis adequados para atender a demanda dos clientes, evitando ao mesmo tempo excesso de estoque ou falta de produtos.
* **Planejamento de produção**: determinar a capacidade necessária, os recursos necessários e os cronogramas de produção. Isso ajuda a evitar gargalos na produção e a otimizar a eficiência operacional.
* **Atendimento ao cliente**: dimensionamento adequado do atendimento ao cliente, o planejamento de recursos humanos e a gestão da capacidade de atendimento.
## Overview
### Objetivo
Criar um modelo de previsão que nos gere uma margem confiável de vendas para certos períodos no futuro.
### Fonte de dados
Os dados usados são da *Corporación Favorita*, uma grande varejista de alimentos com sede no Equador. Eles operam centenas de supermercados, com mais de 200.000 produtos diferentes em suas prateleiras. 

https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting/data

### Etapas do projeto
1. **Análise exploratória dos dados**: visualização das categorias de produto, distribuição de vendas por cluster e atuação dos clusters nas diferentes cidades.
2. **Análise das séries temporais**: comportamento das vendas ao longo dos anos e a influência de variáveis exógenas.
3. **Modelagem e previsão**: configurar dois modelos que prevejam as vendas alguns passos no futuro e comparar a performance deles. 

### Modelos utilizados
Foram utilizados os modelos **ARIMA** e **SARIMAX**.

O notebook com o código completo do projeto se encontra em: 

## 1. Análise exploratória dos dados 
Os dados fornecidos possuem quatro datasets a serem explorados: **sales_df**, **stores_df**, **oil_df** e **holidays_df**.
O primeiro dataset, sales_df, possui colunas informando id, data, número da loja, categoria, receita e quantidade de produtos em promoção relacionados a uma determinada venda.  

![sales_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/1.png)

O dataset stores_df possui informações acerca da cidade e o estado em que uma determinada loja está situada, bem como o seu tipo e o número do cluster ao qual pertence.

![stores_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/2.png)

O dataset oil_df possui as variações do preço do petróleo ao longo do tempo. Como o Equador é um país produtor de petróleo, o a alta no preço do óleo pode afetar o preço final das mercadorias vendidas pela varejista, isto é, devido aos custos de produção, custos de transporte, condições econômicas gerais, entre outros.

![oil_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/3.png)

Já holidays_df possui especificações de todos os feriados ocorridos dentro do período em questão, lembrando que os feriados podem mudar o padrão de comportamento do consumidor e gerar comportamentos sazonais nas vendas.

![holidays_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/4.png)

Todos os datasets compreendem o período entre os anos de 2013 a 2017.

Vamos checar como estão distribuídas as categorias dos produtos vendidos pela varejista

![sales_cat](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/5.png)

Vemos que grande parte das vendas se concentra em produtos de mercado e mercearia, bem como no setor de bebidas.

A varejista se divide em clusters, isto é, agrupamento de lojas com características semelhantes com base em diferentes critérios, como localização, perfil demográfico dos clientes, comportamento de compra, concorrência local, entre outros. O objetivo de criar clusters é segmentar as lojas em grupos distintos para entender melhor o desempenho de cada grupo e desenvolver estratégias mais eficazes para alocar recursos, entender o ambiente competitivo local, analisar desempenho e traçar metas de expansão.

Como um insight inicial, vamos visualizar qual foi a média de vendas de cada cluster 

![cluster-mean](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/6.png)

Vemos que o cluster 5 possui uma grande performance em relação às vendas.

Vamos como os clusters estão distribuídos entre a cidades e a margem de vendas de cada um

![cluster_at](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/7.png)

Observamos que os clusters com maior concentração de vendas ficam na capital, Quito.

## 2. Análise das séries temporais
Vamos explorar explorar as séries de vendas em termos de anos disponíveis

![s_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/8.png)

Observamos que o ano de 2014 teve um aumento considerável na margem das vendas em relação ao ano anterior, porém com um comportamento instável. No segundo semestre de 2015 a margem de vendas subiu e se manteu estável, repetindo o comportamento para os anos de 2016 e 2017.

A fim de obter uma amostra dos dados menor e mais estável, vamos trabalhar somente com os dados do ano de 2016, filtrando pela categoria de bebidas, em rezão dos valores estarem em um escala não tão discrepante.

![s_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/9.png)

É possível notar um padrão sazonal claro nos dados, o que fica mais evidente quando filtramos somente para os meses de janeiro e fevereiro

![saso_2016](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/saso_2016.png)

Um ciclo de sazonalidade tem aproximadamente sete dias, uma informação importante para ajudar na modelagem futura.

Vamos agora verificar se a quantidade de produtos promocionais tem algum poder de influência nas vendas

![s_3](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/10.png)

Observamos que em alguns picos de preços promocionais, as vendas obtiveram uma margem alta, porém em outros não. O que pode significar que a quantidade de produtos promocionais não é um fator tão determinante para uma margem de vendas alta.

Vamos ver agora como as vendas se comportam com as flutuações no preço do óleo

![s_4](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/10b.png)

Durante meados de maio e começo de julho o preço do óleo teve grande aumento, concomitantemente a isso, a margem de vendas se estabeleceu em uma margem um pouco mais baixa.

![s_5](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/10c.png)

Ao marcar os dias de feriados, vemos que entre abril e maio houve uma grande concentração de feriados, fazendo as vendas alcancarem uma margem que não foi observada em nenhum ciclo sazonal posterior.

![s_6](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/11.png)
![s_7](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/12.png)
![s_8](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/13.png)
## 3. Modelagem e previsão
![adf_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/14.png)

![adf_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/15.png)

![aic_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/16.png)

![res_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/17.png)
![lb_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/18.png)
![ex_data](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/19.png)
![aic_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/20.png)
![res_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/21.png)
![lb_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/22.png)
![pred](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/23.png)
![mape](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/24.png)

## Avaliação dos resultados
## Conclusão
## Referências 

[1]. 

[2]. 

[3].

[4]. 

