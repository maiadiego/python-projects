## Segmentação de Clientes de Cartão de Crédito para Otimização de Estratégias Financeiras
### Problema de negócio
<p align="justify"> A análise do comportamento de uso do cartão de crédito de aproximadamente 9.000 clientes ativos nos últimos seis meses revelou três perfis distintos de consumidores. Esses perfis foram identificados por meio de técnicas de segmentação de dados, permitindo uma compreensão mais profunda dos hábitos de consumo, padrões de pagamento e uso de crédito. O desafio do negócio consiste em utilizar esses insights para desenvolver estratégias personalizadas que maximizem a rentabilidade, reduzam riscos de inadimplência e aumentem a fidelização dos clientes, equilibrando a oferta de crédito com práticas sustentáveis para a instituição financeira.</p>

### Descrição do Conjunto de Dados
O dataset possui 18 variáveis ​​comportamentais por parte dos clientes quanto ao uso de seu cartão de crédito:

**CUST_ID:** Identificação do titular do cartão de crédito (categórica, ou seja, não possui valor numérico relevante para cálculos).

**BALANCE:** Saldo disponível na conta do cartão de crédito para realizar compras.

**BALANCE_FREQUENCY:** Com que frequência o saldo do cartão é atualizado (valor entre 0 e 1, onde 1 significa atualização frequente e 0 significa atualização rara).

**PURCHASES:** Valor total gasto em compras no período analisado.

**ONEOFF_PURCHASES:** Maior valor de uma única compra feita de uma só vez.

**INSTALLMENTS_PURCHASES:** Valor total de compras feitas parceladas.

**CASH_ADVANCE:** Valor total de dinheiro retirado como adiantamento no cartão de crédito (saques de crédito).

**PURCHASES_FREQUENCY:** Frequência com que as compras são realizadas (entre 0 e 1, sendo 1 = compras muito frequentes e 0 = compras raras).

**ONEOFFPURCHASESFREQUENCY:** Frequência das compras feitas de uma só vez (entre 0 e 1, sendo 1 = compras únicas frequentes e 0 = compras únicas raras).

**PURCHASESINSTALLMENTSFREQUENCY:** Frequência das compras parceladas (entre 0 e 1, sendo 1 = compras parceladas frequentes e 0 = compras parceladas raras).

**CASHADVANCEFREQUENCY:** Frequência com que o titular do cartão faz saques de crédito.

**CASHADVANCETRX:** Número de transações de saque de crédito realizadas.

**PURCHASES_TRX:** Número total de transações de compra feitas.

**CREDIT_LIMIT:** Limite de crédito disponível para o usuário.

**PAYMENTS:** Total de pagamentos feitos pelo usuário.

**MINIMUM_PAYMENTS:** Valor mínimo dos pagamentos feitos pelo usuário.

**PRCFULLPAYMENT:** Percentual de vezes em que o usuário quitou a fatura integralmente.

**TENURE:** Tempo de posse do cartão de crédito pelo usuário.

### Aplicação do Algoritmo de Clusterização

<p align="justify"> O algoritmo utilizado nessa etapa foi o K-Means. Após rodadas de teste, o número de clusters que dividiria o conjunto de dados foi pré-definido como 3. </p>
<p align="justify"> Em função da alta quantidade de variáveis do conjunto, foi aplicado o algoritmo Kernel PCA para reduzir as variáveis a dois componentes principais, possibilitando a visualização dos agrupamentos em duas dimensões, como mostra a figura a seguir: </p>

![pca](https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/clusterizacao-cartao-credito/img/kernel-pca.png) 

<p align="justify"> Esses dois componentes são responsáveis por explicar grande parte da variação nos dados. </p>

### Análise Estatística dos Clusters

Após a formação dos agrupamentos, foi realizada uma análise descritiva utilizando boxplots e gráficos de densidade considerando todas as variáveis de cada cluster. Análise foi focada no quartis do gráfico boxplot a fim de identificar as semelhanças e diferenças nas características dos clientes presentes em cada cluster.

#### Cluster 0



