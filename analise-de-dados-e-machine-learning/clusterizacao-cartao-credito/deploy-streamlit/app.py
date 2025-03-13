import streamlit as st
import pandas as pd
import joblib  
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import KernelPCA
import plotly.express as px
import os


def carregar_dados():
    # Carregar dataset 
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "dados_clientes.csv"))
    # Carregar modelo treinado
    kmeans = joblib.load("modelo_cluster.pkl")

    mapeamento_colunas = {
        'CUST_ID': 'CLIENTE_ID',
        'BALANCE': 'SALDO_DISPONIVEL',
        'BALANCE_FREQUENCY': 'FREQ_SALDO',
        'PURCHASES': 'COMPRAS',
        'ONEOFF_PURCHASES': 'MAIOR_COMPRA_DE_UMA_VEZ',
        'INSTALLMENTS_PURCHASES': 'COMPRAS_PARCELADAS',
        'CASH_ADVANCE': 'SAQUES_DE_CREDITO',
        'PURCHASES_FREQUENCY': 'FREQ_COMPRAS',
        'ONE_OFF_PURCHASES_FREQUENCY': 'FREQ_COMPRAS_DE_UMA_VEZ',
        'PURCHASES_INSTALLMENTS_FREQUENCY': 'FREQ_COMPRAS_PARCELADAS',
        'CASH_ADVANCE_FREQUENCY': 'FREQ_SAQUES_DE_CREDITO',
        'CASH_ADVANCE_TRX': 'N_TRAN_SAQUES_DE_CREDITO',
        'PURCHASES_TRX': 'N_TRAN_COMPRAS',
        'CREDIT_LIMIT': 'LIMITE_CREDITO',
        'PAYMENTS': 'PAGAMENTOS',
        'MINIMUM_PAYMENTS': 'PAGAMENTOS_MINIMOS',
        'PRC_FULL_PAYMENT': 'PERC_PAGAMENTO_INTEGRAL',
        'TENURE': 'TEMPO_POSSE'
    }
    df.rename(columns=mapeamento_colunas, inplace=True)
    df.fillna(df.mode().iloc[0], inplace=True)
    cust_id = df['CLIENTE_ID']
    df.drop(columns=['CLIENTE_ID'], inplace=True)  # ID não é relevante para clusters
    return df, cust_id, kmeans



def criar_dfs_plot(df, kmeans, cust_id):
    # Normalizar os dados para que fiquem na mesma escala
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    # 1. Aplicar Kernel PCA com kernel RBF
    kpca = KernelPCA(n_components=2, kernel='rbf', gamma=0.01, eigen_solver='auto')  # Ajuste gamma se necessário
    X_kpca = kpca.fit_transform(df_scaled)

    # 2. Aplicar K-Means para encontrar os clusters
    clusters = kmeans.fit_predict(X_kpca)

    # Criar DataFrame para visualização
    df_plot = pd.DataFrame({
        'Componente 1': X_kpca[:, 0],
        'Componente 2': X_kpca[:, 1],
        'Cluster': clusters,
        'CUST_ID': cust_id
    })

    # Dicionário de mapeamento dos clusters para os grupos
    cluster_map = {0: "Clientes Moderados", 1: "Clientes Conservadores", 2: "Clientes Gastadores"}

    # Criar a nova coluna "Grupo" com base no mapeamento
    df_plot["Grupo"] = df_plot["Cluster"].map(cluster_map)

    # Criar uma cópia do dataset original para não modificar os dados originais
    data_with_clusters = df.copy()

    # Adicionar a coluna de clusters ao dataset e retornar com a coluna CUST_ID
    data_with_clusters['Cluster'] = clusters
    data_with_clusters['CLIENTE_ID'] = cust_id
    data_with_clusters["Grupo"] = data_with_clusters["Cluster"].map(cluster_map)

    return df_plot, data_with_clusters, cluster_map



def desc_clientes():
    # Definição dos perfis
    perfis_clientes = {
        "Clientes Moderados": {
            "nome": "Cliente Moderado (Perfil Intermediário)",
            "descricao": "Usa o cartão regularmente, mas sem excessos. Realiza compras parceladas e à vista, "
                        "com saques moderados. Pode não ser altamente endividado, mas também não é extremamente conservador.",
            "cor": "#440154",
            "icone": "🟣"
        },
        "Clientes Conservadores": {
            "nome": "Cliente Conservador (Baixo Uso)",
            "descricao": "Usa o cartão de forma limitada. Faz poucas compras e evita parcelamentos. Faz poucos (ou nenhum) saques de crédito. "
                        "Pode ser um usuário novo ou alguém que prefere outros meios de pagamento.",
            "cor": "#66c2a5",
            "icone": "🔵"
        },
        "Clientes Gastadores": {
            "nome": "Cliente Gastador (Alto Uso)",
            "descricao": "Usa o cartão intensamente para compras parceladas e à vista. "
                        "Não faz saques de crédito, mas tem alto volume de transações e realiza pagamentos elevados.",
            "cor": "#fde725",
            "icone": "🟡"
        }
    }

    # Mapeamento fixo de cores para os clusters
    cores_clusters = {
        "Clientes Moderados": "#440154",  # Roxo
        "Clientes Conservadores": "#66c2a5",  # Azul
        "Clientes Gastadores": "#fde725"   # Amarelo
    }
    return perfis_clientes, cores_clusters



def explorar_grupos(perfis_clientes, cores_clusters, df_plot, data_with_clusters):
    # Seletor de cluster
    cluster_selecionado = st.sidebar.selectbox("Selecione um Grupo:", ["Clientes Moderados", "Clientes Conservadores", "Clientes Gastadores", "Todos"], index=3)

    # Slider para ajustar tamanho dos pontos
    tamanho_pontos = st.sidebar.slider("Tamanho dos pontos", min_value=5, max_value=15, value=8)

    # Filtrar dados do cluster selecionado
    if cluster_selecionado == "Todos":
        df_plot_filtrado = df_plot  # Sem filtro, mostra todos os pontos
        
        # Exibe todas as descrições
        for perfil, info in perfis_clientes.items():
            st.markdown(
                f"<h4 style='color: {info['cor']}'>{info['icone']} {info['nome']}</h4>"
                f"<p>{info['descricao']}</p>",
                unsafe_allow_html=True
            )
    else:
        df_plot_filtrado = df_plot[df_plot["Grupo"] == cluster_selecionado]  # Filtra pelo cluster escolhido
        
        # Exibe a descrição do cluster correspondente
        info = perfis_clientes[cluster_selecionado]
        st.markdown(
                f"<h4 style='color: {info['cor']}'>{info['icone']} {info['nome']}</h4>"
                f"<p>{info['descricao']}</p>",
                unsafe_allow_html=True
            )

    # Scatter Plot interativo com cores fixas
    fig = px.scatter(
        df_plot_filtrado,
        x='Componente 1',
        y='Componente 2',
        color=df_plot_filtrado['Grupo'].astype(str),
        title="",
        labels={'Grupo': 'Grupo'},
        hover_data=['CUST_ID'],
        color_discrete_map=cores_clusters  # Aplica cores fixas
    )

    # Ajustes para melhorar a visibilidade dos pontos
    fig.update_traces(
        marker=dict(
            size=tamanho_pontos,            # Define tamanho dos pontos
            opacity=0.8,                    # Torna pontos um pouco mais transparentes
            line=dict(width=1, color="black")  # Adiciona borda preta nos pontos
        )
    )

    fig.update_layout(
        xaxis_title='Componente Principal 1 (Kernel PCA)',
        yaxis_title='Componente Principal 2 (Kernel PCA)',
        legend_title='Grupo',
        template='plotly_dark'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Filtrar dados para estatísticas e gráficos
    if cluster_selecionado == "Todos":
        cluster_data = data_with_clusters  # Mostra todos os dados sem filtragem
    else:
        cluster_data = data_with_clusters[data_with_clusters["Grupo"] == cluster_selecionado]

    # Exibir estatísticas descritivas
    st.subheader(f"📊 Estatísticas do Grupo {cluster_selecionado}")
    colunas_numericas = cluster_data.select_dtypes(include=["number"]).columns.drop(["Cluster", "CUST_ID", "Grupo"], errors="ignore")
    st.write(cluster_data[colunas_numericas].describe().round(1))

    # Criar gráficos para cada coluna numérica
    for coluna in colunas_numericas:
        st.subheader(f"📈 {coluna} - Grupo {cluster_selecionado}")

        # Boxplot com Plotly
        fig_box = px.box(cluster_data, y=coluna, title=f"Boxplot de {coluna} - Grupo {cluster_selecionado}",
                         width=600, height=400)
        st.plotly_chart(fig_box, use_container_width=True)

        # Histograma com Plotly
        fig_hist = px.histogram(cluster_data, x=coluna, nbins=20, title=f'Distribuição de {coluna} - Grupo {cluster_selecionado}',
                                width=600, height=400, color_discrete_sequence=["blue"])
        fig_hist.update_layout(bargap=0.1)
        st.plotly_chart(fig_hist, use_container_width=True)



def clientes_chave(data_with_clusters, df_plot):

    # Filtrar clientes de alto valor
    clientes_alto_valor = data_with_clusters[
        (data_with_clusters["COMPRAS"] > 2000) &  # Gastam bastante
        (data_with_clusters["FREQ_COMPRAS"] >= 0.8) &  # Compram frequentemente
        (data_with_clusters["FREQ_SAQUES_DE_CREDITO"] == 0) &  # Não fazem saques emergenciais
        (data_with_clusters["LIMITE_CREDITO"] >= 7000) #&  # Têm um bom limite
    ]

    # Filtrar clientes com risco de inadimplência
    clientes_risco_inadimplencia = data_with_clusters[
        (data_with_clusters["SAQUES_DE_CREDITO"] > 2000) &  # Usa muito adiantamento em dinheiro (indicador de emergência financeira)
        (data_with_clusters["PERC_PAGAMENTO_INTEGRAL"] == 0) &  # Nunca paga a fatura integral
        (data_with_clusters["PAGAMENTOS_MINIMOS"] > 1000)  # Está pagando apenas o mínimo, mas valores altos
    ]

    # Filtrar clientes com risco de churn ou com baixo engajamento
    clientes_risco_churn = data_with_clusters[
        (data_with_clusters["COMPRAS"] < 500) &  # Quase não compra
        (data_with_clusters["FREQ_COMPRAS"] < 0.3) &  # Frequência de compras muito baixa
        (data_with_clusters["LIMITE_CREDITO"] > 7000) &  # Tem um limite alto, mas não usa
        (data_with_clusters["SALDO_DISPONIVEL"] > 4000) &  # Tem muito saldo disponível (não precisa do cartão)
        (data_with_clusters["TEMPO_POSSE"] == 12)  # Já está há um tempo na base, mas sem engajamento
    ]

    # Concatenando os datasets (empilhando as linhas)
    clientes_est_todos = pd.concat([clientes_alto_valor, clientes_risco_inadimplencia, clientes_risco_churn], ignore_index=True)

    # Cria um subconjunto de df_plot contendo apenas os clientes que existem em clientes_est_todos
    clientes_est_todos_pca = df_plot[df_plot['CUST_ID'].isin(clientes_est_todos['CLIENTE_ID'])]

    return clientes_alto_valor, clientes_risco_inadimplencia, clientes_risco_churn, clientes_est_todos, clientes_est_todos_pca



def explorar_clientes_chave(cores_clusters, df_plot, clientes_alto_valor, clientes_risco_inadimplencia, 
                            clientes_risco_churn, clientes_est_todos, clientes_est_todos_pca):
    tipo_cliente = st.selectbox("Selecione um Tipo de Cliente Estratégico:", ["Clientes de Alto Valor", "Clientes Risco Inadimplência", "Clientes Risco de Cancelamento", "Todos"], index=3)

    # Lógica para filtrar os dados com base na escolha do usuário
    if tipo_cliente == "Clientes de Alto Valor":
        df_plot_filtrado = df_plot[df_plot['CUST_ID'].isin(clientes_alto_valor['CLIENTE_ID'])]
        clientes_est = clientes_alto_valor.copy()
    
    elif tipo_cliente == "Clientes Risco Inadimplência":
        df_plot_filtrado = df_plot[df_plot['CUST_ID'].isin(clientes_risco_inadimplencia['CLIENTE_ID'])]
        clientes_est = clientes_risco_inadimplencia.copy()
    
    elif tipo_cliente == "Clientes Risco de Cancelamento":
        df_plot_filtrado = df_plot[df_plot['CUST_ID'].isin(clientes_risco_churn['CLIENTE_ID'])]
        clientes_est = clientes_risco_churn.copy()
    
    else:
        df_plot_filtrado = clientes_est_todos_pca  # Mostrar todos os clientes se "Todos" for selecionado
        clientes_est = clientes_est_todos.copy()

    # Slider para ajustar tamanho dos pontos
    tamanho_pontos = st.sidebar.slider("Tamanho dos pontos", min_value=5, max_value=15, value=8)

    # Scatter Plot interativo com cores fixas
    fig = px.scatter(
        df_plot_filtrado,
        x='Componente 1',
        y='Componente 2',
        color=df_plot_filtrado['Grupo'].astype(str),
        title="",
        labels={'Grupo': 'Grupo'},
        hover_data=['CUST_ID'],
        color_discrete_map=cores_clusters  # Aplica cores fixas
    )

    # Ajustes para melhorar a visibilidade dos pontos
    fig.update_traces(
        marker=dict(
            size=tamanho_pontos,            # Define tamanho dos pontos
            opacity=0.8,                    # Torna pontos um pouco mais transparentes
            line=dict(width=1, color="black")  # Adiciona borda preta nos pontos
        )
    )

    fig.update_layout(
        xaxis_title='Componente Principal 1 (Kernel PCA)',
        yaxis_title='Componente Principal 2 (Kernel PCA)',
        legend_title='Grupo',
        template='plotly_dark'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Exibir estatísticas descritivas
    st.subheader(f"📊 Estatísticas dos Clientes {tipo_cliente}")
    colunas_numericas = clientes_est.select_dtypes(include=["number"]).columns.drop(["Cluster", "CUST_ID", "Grupo"], errors="ignore")
    st.write(clientes_est[colunas_numericas].describe().round(1))

    # Criar gráficos para cada coluna numérica
    for coluna in colunas_numericas:
        st.subheader(f"📈 {coluna} - Clientes {tipo_cliente}")

        # Boxplot com Plotly
        fig_box = px.box(clientes_est, y=coluna, title=f"Boxplot de {coluna} - Clientes {tipo_cliente}",
                         width=600, height=400)
        st.plotly_chart(fig_box, use_container_width=True)

        # Histograma com Plotly
        fig_hist = px.histogram(clientes_est, x=coluna, nbins=20, title=f'Distribuição de {coluna} - Clientes {tipo_cliente}',
                                width=600, height=400, color_discrete_sequence=["blue"])
        fig_hist.update_layout(bargap=0.1)
        st.plotly_chart(fig_hist, use_container_width=True)



def prever_cliente(kmeans, df, scaler, kpca, cluster_map):
    st.subheader("🔮 Previsão do Grupo de um Novo Cliente")

    # Criar entrada de valores para o novo cliente
    st.sidebar.subheader("📌 Insira os Dados do Novo Cliente")

    # Inicializar estado da sessão para armazenar os inputs e controle do botão
    if "valores_cliente" not in st.session_state:
        st.session_state.valores_cliente = {col: 0.0 for col in df.columns}

    if "prever" not in st.session_state:
        st.session_state.prever = False  # Controlador para evitar execução automática

    # Criar campos de entrada SEM acionar a execução imediata
    for col in df.columns:
        st.session_state.valores_cliente[col] = st.sidebar.number_input(
            f"{col}",
            value=st.session_state.valores_cliente[col],
            key=f"input_{col}"
        )

    # Botão para submeter os dados
    if st.sidebar.button("Prever Grupo 🚀"):
        st.session_state.prever = True  # Ativar a previsão

    # Rodar a previsão SOMENTE quando o botão for pressionado
    if st.session_state.prever:
        with st.spinner("Calculando..."):
            # Normalizar os dados para que fiquem na mesma escala
            df_scaled = scaler.fit_transform(df)

            # Ajustar Kernel PCA com kernel RBF
            X_kpca = kpca.fit_transform(df_scaled)

            # Normalizar os dados do novo cliente
            novo_cliente_scaled = scaler.transform([list(st.session_state.valores_cliente.values())])

            # Aplicar Kernel PCA
            novo_cliente_kpca = kpca.transform(novo_cliente_scaled)

            # Prever o cluster
            cluster_predito = kmeans.predict(novo_cliente_kpca)[0]

            # Exibir o resultado
            st.success(f"🎯 O Novo Cliente foi classificado no **Grupo de {cluster_map.get(cluster_predito, 'Desconhecido')}**")

            # Resetar a variável para evitar reexecuções indesejadas
            st.session_state.prever = False


def main():
    # URL do repositório no GitHub
    GITHUB_URL = "https://github.com/maiadiego/python-projects/blob/master/analise-de-dados-e-machine-learning/" \
    "clusterizacao-cartao-credito/clusterizacao.md"  

    df, cust_id, kmeans = carregar_dados()
    df_plot, data_with_clusters, cluster_map = criar_dfs_plot(df, kmeans, cust_id)
    perfis_clientes, cores_clusters = desc_clientes()
    clientes_alto_valor, clientes_risco_inadimplencia, clientes_risco_churn, clientes_est_todos, clientes_est_todos_pca = clientes_chave(data_with_clusters, df_plot)
    scaler = StandardScaler()
    kpca = KernelPCA(n_components=2, kernel='rbf', gamma=0.01, eigen_solver='auto')  

    # Configuração do layout do Streamlit
    st.set_page_config(page_title="Segmentação de Clientes", layout="wide")

    # Criar um botão estilizado que redireciona para o GitHub
    st.markdown(
        f"""
        <a href="{GITHUB_URL}" target="_blank">
            <button style="
                background-color: transparent; 
                color: #555; 
                font-size: 16px; 
                padding: 10px 24px; 
                border: 2px solid #CCC; 
                border-radius: 5px; 
                cursor: pointer;
            ">
                🔗 Ver Descrição Completa do Projeto
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    # Seção principal do app
    st.title("Segmentação de Clientes - Cartão de Crédito")

    st.sidebar.header("Opções de Visualização")
    opcao = st.sidebar.radio("Escolha uma opção:", ["Exploração dos Grupos de Clientes", "Previsão de Novo Cliente", "Exploração de Clientes Estratégicos"])

    if opcao == "Exploração dos Grupos de Clientes":
        explorar_grupos(perfis_clientes, cores_clusters, df_plot, data_with_clusters)
    elif opcao == "Exploração de Clientes Estratégicos":
        explorar_clientes_chave(cores_clusters, df_plot, clientes_alto_valor, clientes_risco_inadimplencia, 
                                clientes_risco_churn, clientes_est_todos, clientes_est_todos_pca)
    else:
        prever_cliente(kmeans, df, scaler, kpca, cluster_map)


if __name__ == "__main__":
    main()
