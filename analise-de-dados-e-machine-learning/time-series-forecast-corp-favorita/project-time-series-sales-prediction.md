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
![sales_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/1.png)
![stores_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/2.png)
![oil_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/3.png)
![holidays_df](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/4.png)
![sales_cat](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/5.png)
![cluster-mean](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/6.png)
![cluster_at](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/7.png)
## 2. Análise das séries temporais
![s_1](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/8.png)
![s_2](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/9.png)
![s_3](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/10.png)
![s_4](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/10b.png)
![s_5](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/time-series-forecast-corp-favorita/img/10c.png)
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

