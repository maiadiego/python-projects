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

### Mapeamento dos Perfis de Clientes

Após a formação dos agrupamentos, foi realizada uma análise descritiva utilizando boxplots e gráficos de densidade considerando todas as variáveis de cada cluster. Análise foi focada no quartis do gráfico boxplot com o intuito de identificar as semelhanças e diferenças nas características dos clientes presentes em contidos nos clusters.

#### Cluster 0 – Cliente Moderado (Perfil Intermediário)

* <p align="justify"> Tem um saldo médio disponível e um limite de crédito relativamente alto. </p>
* <p align="justify"> Realiza compras e saques de crédito com uma frequência moderada. </p>
* <p align="justify"> Poucos clientes quitam a fatura integralmente.</p>
* <p align="justify"> Possui um volume considerável de pagamentos durante o período especificado, mas com variações significativas entre clientes.</p>

**Perfil:** Cliente que usa o cartão com regularidade, realizando tanto compras parceladas quanto de uma só vez, e faz saques de crédito de forma moderada. Pode não ser um cliente altamente endividado, mas também não é extremamente conservador. </p>

📌 Ações sugeridas para Incentivar Maior Uso e Fidelização:

- Cashback e recompensas: Programas de pontos e cashback em determinadas categorias de compra para incentivar maior uso.
- Ofertas exclusivas: Descontos em lojas parceiras para compras parceladas e à vista.
- Incentivo ao pagamento integral da fatura: Bonificações ou redução de tarifas para quem paga 100% da fatura.
- Ofertas de crédito personalizado: Aumento de limite para clientes que mantêm um histórico positivo.


#### Cluster 1 – Cliente Conservador (Baixo Uso)

* <p align="justify"> Possui saldo baixo e um limite de crédito relativamente reduzido. </p>
* <p align="justify"> Realiza poucas compras e quase não faz compras de alto valor. </p>
* <p align="justify"> Tem baixa frequência de compras, parcelamentos e saques de crédito.</p>
* <p align="justify"> Os valores médios de pagamentos e de pagamento mínimo são menores em relação aos outros clusters.</p>

**Perfil:** Cliente que utiliza o cartão de forma limitada, talvez por precaução financeira ou por preferência por outros meios de pagamento. Pode ser um usuário novo ou um cliente que não confia no crédito. </p>

📌 Ações sugeridas para Estimular o Uso do Cartão:

- Isenção de anuidade ou taxas reduzidas: Para incentivar mais transações.
- Campanhas de marketing: Mostrar benefícios do uso consciente do crédito e programas de fidelidade.
- Parcelamentos facilitados: Ofertas de parcelamento sem juros em compras de menor valor.
- Aumento gradual de limite: Para clientes que começarem a usar o cartão de forma consistente.

#### Cluster 2 – Cliente Gastador (Alto Uso)

* <p align="justify"> Faz compras com alta frequência e em grande volume, tanto parceladas quanto de uma só vez. </p>
* <p align="justify"> Praticamente não realiza saques de crédito. </p>
* <p align="justify"> Apresenta um número alto de transações de compra.</p>
* <p align="justify"> Tem um limite de crédito intermediário e faz pagamentos mais elevados.</p>

**Perfil:** Cliente que utiliza o cartão de forma intensa para compras, tanto parceladas quanto à vista. É um perfil de consumidor que pode ser um bom pagador, mas que também pode precisar de um gerenciamento de crédito adequado. </p>

📌 Ações sugeridas para Gerenciar Riscos e Oferecer Benefícios Premium:

- Ofertas de crédito premium: Cartões com benefícios exclusivos, como acesso a salas VIP e seguros.
- Monitoramento de crédito: Algoritmos para detectar sinais de risco de inadimplência e oferecer renegociação proativa.
- Promoções de alta exclusividade: Convites para eventos, descontos especiais e benefícios para compras acima de determinado valor.
- Pagamentos programados: Opções para facilitar a quitação da fatura, evitando inadimplência.

Cada cluster possui clientes com valores extremos que se distanciam do comportamento padrão dos outros clientes do cluster. Por conta disso, foi realizada uma filtragem da amostra geral com o objetivo de capturar clientes estratégicos, como **Clientes de Alto Valor**, **Clientes com Risco de Inadimplência** e **Clientes com Risco de Cancelamento**.

* **Clientes de Alto Valor** <p align="justify"> Alto nível e frequência de compras, não realizam saques emergenciais e possuem um bom limite.</p>
* **Clientes com Risco de Inadimplência** <p align="justify"> Usa muito adiantamento em dinheiro (indicador de emergência financeira), nunca paga a fatura integral e paga apenas o mínimo, mas valores altos</p>
* **Clientes com Risco de Cancelamento** <p align="justify"> Nível e frequência de compras baixo, limite alto mas não usa, tem muito saldo disponível, tem bastante tempo de posse do cartão mas sem engajamento.</p>

O filtro realizado apontou **330 clientes de alto valor (onde 92% pertencem ao Cluster 2)**, **632 clientes com risco de inadimplência (onde 90% pertencem ao Cluster 0)** e **237 com risco de cancelamento (onde 96% também pertencem ao Cluster 0)**. Portanto, o Cluster 0, em razão da sua alta diversidade de clientes, precisa de um pouco mais de atenção.

### Ações a serem Tomadas

Para os **Clientes de Alto Valor**:

🔹 Oferecer programas de recompensas exclusivos e personalizados (cashback, milhas, parcerias premium).

🔹 Disponibilizar atendimento prioritário e benefícios exclusivos (sala VIP, concierge, seguro viagem).

🔹 Ampliar limite de crédito de forma estratégica para incentivar mais compras.

🔹 Criar ofertas personalizadas baseadas no comportamento de consumo (ex: descontos em categorias de maior interesse).

Para os **Clientes com Risco de Inadimplência**:

🔹 Oferecer planos de renegociação com parcelamento da fatura em condições acessíveis.

🔹 Enviar notificações sobre impacto de juros e importância de pagar o valor total.

🔹 Criar alertas proativos para lembrar do vencimento da fatura e sugerir pagamentos parciais antes do fechamento.

🔹 Oferecer benefícios para pagamentos em dia, como redução temporária de juros ou cashback na fatura.

🔹 Monitorar comportamento e reduzir gradualmente o limite caso o risco aumente.

Para os **Clientes com Risco de Cancelamento**:

🔹 Criar ofertas personalizadas baseadas em histórico de compras e interesses (ex: cupons de desconto para primeiras compras).

🔹 Reduzir ou eliminar taxas de anuidade para incentivar o uso contínuo.

🔹 Enviar comunicações direcionadas mostrando os benefícios do cartão que o cliente não está utilizando.

🔹 Oferecer incentivos para uso do cartão, como cashback na primeira compra após um período sem uso.

🔹 Criar campanhas de ativação, como sorteios e desafios de gastos para desbloquear recompensas.



