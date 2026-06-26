# Importa as bibliotecas necessárias
import os  # Para interagir com o sistema operacional, como variáveis de ambiente
import pandas as pd  # Para manipulação e análise de dados em formato de DataFrame
import plotly.express as px  # Para criação de gráficos interativos
import streamlit as st  # Framework para construção de aplicações web interativas
from dotenv import load_dotenv  # Para carregar variáveis de ambiente de um arquivo .env
from sqlalchemy import create_engine  # Para criar uma conexão com o banco de dados


# ============================================================
# Configuração inicial da aplicação Streamlit
# ============================================================

# Carrega as variáveis de ambiente do arquivo .env (ex: credenciais de banco de dados)
load_dotenv()

# Configurações da página principal do Streamlit
st.set_page_config(
    page_title="Licitações Risk Intelligence",  # Título da página exibido no navegador
    layout="wide",  # Define o layout da página como "wide" (mais largo)
)


# ============================================================
# Caminhos dos arquivos de dados de Machine Learning
# ============================================================

# Obtém o diretório base do projeto (dois níveis acima do arquivo atual)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho completo para o arquivo CSV de classificação de risco de licitações
RISK_CLASSIFICATION_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "licitacoes_risk_classification.csv",
)

# Caminho completo para o arquivo CSV de fornecedores clusterizados
SUPPLIER_CLUSTER_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "fornecedores_clusterizados.csv",
)


# ============================================================
# Conexão com o banco de dados e carregamento de dados
# ============================================================

# Função para obter a URL de conexão com o banco de dados
def get_database_url() -> str:
    # Tenta obter a URL do banco de dados das variáveis de ambiente
    database_url = os.getenv("DATABASE_URL")

    # Se a URL não estiver definida, constrói a partir de variáveis de ambiente individuais
    if not database_url:
        user = os.getenv("POSTGRES_USER", "admin")  # Usuário padrão: admin
        password = os.getenv("POSTGRES_PASSWORD", "admin")  # Senha padrão: admin
        host = os.getenv("POSTGRES_HOST", "localhost")  # Host padrão: localhost
        port = os.getenv("POSTGRES_PORT", "5433")  # Porta padrão: 5433
        database = os.getenv("POSTGRES_DB", "licitacoes_db")  # Banco de dados padrão: licitacoes_db

        # Formata a URL de conexão PostgreSQL
        database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    return database_url


# Função para criar e armazenar em cache o objeto engine de conexão com o banco de dados
@st.cache_resource
def get_engine():
    return create_engine(get_database_url())


# Função para carregar os dados analíticos das licitações do banco de dados
@st.cache_data
def carregar_dados_banco() -> pd.DataFrame:
    engine = get_engine()  # Obtém o engine de conexão

    # Query SQL para selecionar todos os dados da view analítica
    query = """
        SELECT *
        FROM vw_licitacoes_analytics;
    """

    # Executa a query e carrega os resultados em um DataFrame do Pandas
    df = pd.read_sql(query, engine)
    # Converte a coluna 'data' para o tipo datetime
    df["data"] = pd.to_datetime(df["data"])

    return df


# Função para carregar os dados de classificação de risco de ML
@st.cache_data
def carregar_risco_ml() -> pd.DataFrame:
    # Verifica se o arquivo de classificação de risco existe
    if not os.path.exists(RISK_CLASSIFICATION_PATH):
        return pd.DataFrame()  # Retorna um DataFrame vazio se o arquivo não for encontrado

    return pd.read_csv(RISK_CLASSIFICATION_PATH)  # Carrega o CSV em um DataFrame


# Função para carregar os dados de fornecedores clusterizados
@st.cache_data
def carregar_clusters_fornecedores() -> pd.DataFrame:
    # Verifica se o arquivo de clusters de fornecedores existe
    if not os.path.exists(SUPPLIER_CLUSTER_PATH):
        return pd.DataFrame()  # Retorna um DataFrame vazio se o arquivo não for encontrado

    return pd.read_csv(SUPPLIER_CLUSTER_PATH)  # Carrega o CSV em um DataFrame


# ============================================================
# Botão de atualização de dados e carregamento inicial
# ============================================================

# Adiciona um título à barra lateral para os controles
st.sidebar.title("Controles")

# Cria um botão na barra lateral para atualizar os dados
if st.sidebar.button("Atualizar dados"):
    st.cache_data.clear()  # Limpa o cache de dados do Streamlit
    st.cache_resource.clear()  # Limpa o cache de recursos do Streamlit
    st.rerun()  # Força o re-execução do script Streamlit para recarregar os dados


# ============================================================
# Carregamento dos dados principais
# ============================================================

# Carrega os dados analíticos do banco de dados
df = carregar_dados_banco()
# Carrega os dados de classificação de risco de ML
df_ml = carregar_risco_ml()
# Carrega os dados de fornecedores clusterizados
df_fornecedores = carregar_clusters_fornecedores()


# ============================================================
# Cabeçalho da aplicação Streamlit
# ============================================================

# Define o título principal da aplicação
st.title(" Licitações Risk Intelligence Platform")

# Adiciona uma descrição em Markdown
st.markdown(
    """
    Plataforma analítica para monitoramento de licitações públicas, identificação de padrões de risco,
    detecção de anomalias e clusterização de fornecedores.
    """
)


# ============================================================
# Sidebar - Configuração e aplicação dos filtros
# ============================================================

# Define o título da seção de filtros na barra lateral
st.sidebar.title("Filtros")

# Extrai os valores únicos para os filtros de Ano, Órgão, Categoria e Nível de Risco
anos = sorted(df["ano"].dropna().unique())
orgaos = sorted(df["nome_orgao"].dropna().unique())
categorias = sorted(df["categoria"].dropna().unique())
niveis_risco = sorted(df["nivel_risco"].dropna().unique())

# Cria multiselects na barra lateral para cada filtro, com todos os valores selecionados por padrão
anos_selecionados = st.sidebar.multiselect(
    "Ano",
    options=anos,
    default=list(anos),
)

orgaos_selecionados = st.sidebar.multiselect(
    "Órgão",
    options=orgaos,
    default=list(orgaos),
)

categorias_selecionadas = st.sidebar.multiselect(
    "Categoria",
    options=categorias,
    default=list(categorias),
)

riscos_selecionados = st.sidebar.multiselect(
    "Nível de risco original",
    options=niveis_risco,
    default=list(niveis_risco),
)

# Inicializa um DataFrame filtrado como uma cópia do DataFrame original
df_filtrado = df.copy()

# Aplica os filtros selecionados ao DataFrame
if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado["ano"].isin(anos_selecionados)]

if orgaos_selecionados:
    df_filtrado = df_filtrado[df_filtrado["nome_orgao"].isin(orgaos_selecionados)]

if categorias_selecionadas:
    df_filtrado = df_filtrado[df_filtrado["categoria"].isin(categorias_selecionadas)]

if riscos_selecionados:
    df_filtrado = df_filtrado[df_filtrado["nivel_risco"].isin(riscos_selecionados)]


# ============================================================
# Definição e criação das abas na interface do Streamlit
# ============================================================

# Cria quatro abas para organizar o conteúdo do dashboard
aba_geral, aba_anomalias, aba_risco, aba_fornecedores = st.tabs(
    [
        "Visão Geral",  # Título da primeira aba
        "Anomalias",  # Título da segunda aba
        "Classificação de Risco",  # Título da terceira aba
        "Fornecedores",  # Título da quarta aba
    ]
)


# ============================================================
# Aba 1 - Visão Geral: Exibição de métricas e gráficos gerais
# ============================================================

with aba_geral:
    # Calcula métricas principais
    total_licitacoes = len(df_filtrado)  # Número total de licitações após filtros
    valor_total = df_filtrado["valor_contratado"].sum()  # Soma total dos valores contratados
    valor_medio = df_filtrado["valor_contratado"].mean()  # Valor médio contratado
    total_fornecedores = df_filtrado["nome_fornecedor"].nunique()  # Número único de fornecedores
    total_orgaos = df_filtrado["nome_orgao"].nunique()  # Número único de órgãos
    # Contagem de licitações com nível de risco "Alto" ou "Crítico"
    total_alto_critico = df_filtrado[
        df_filtrado["nivel_risco"].isin(["Alto", "Crítico"])
    ].shape[0]

    # Calcula o percentual de licitações com risco alto/crítico
    percentual_alto_critico = (
        (total_alto_critico / total_licitacoes) * 100
        if total_licitacoes > 0
        else 0
    )

    # Cria colunas para exibir métricas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total de licitações", f"{total_licitacoes:,}".replace(",", ".")
        )  # Exibe o total de licitações formatado
        st.metric("Total de órgãos", total_orgaos)  # Exibe o total de órgãos

    with col2:
        st.metric(
            "Valor total contratado", f"R$ {valor_total:,.2f}"
        )  # Exibe o valor total contratado formatado
        st.metric("Total de fornecedores", total_fornecedores)  # Exibe o total de fornecedores

    with col3:
        st.metric(
            "Valor médio contratado", f"R$ {valor_medio:,.2f}"
        )  # Exibe o valor médio contratado formatado
        st.metric(
            "Risco alto/crítico", f"{percentual_alto_critico:.2f}%"
        )  # Exibe o percentual de risco alto/crítico

    st.divider()  # Adiciona um divisor visual

    # Cria colunas para exibir gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Agrupa dados por órgão e calcula o valor total contratado, pegando os top 10
        valor_por_orgao = (
            df_filtrado.groupby("nome_orgao", as_index=False)["valor_contratado"]
            .sum()
            .sort_values("valor_contratado", ascending=False)
            .head(10)
        )

        # Cria um gráfico de barras horizontais para o valor contratado por órgão
        fig_orgao = px.bar(
            valor_por_orgao,
            x="valor_contratado",
            y="nome_orgao",
            orientation="h",
            title="Top 10 órgãos por valor contratado",
            labels={
                "valor_contratado": "Valor contratado",
                "nome_orgao": "Órgão",
            },
        )

        # Inverte a ordem do eixo Y para que o maior valor fique no topo
        fig_orgao.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_orgao, use_container_width=True)  # Exibe o gráfico

    with col2:
        # Agrupa dados por fornecedor e calcula o total de contratos e valor total, pegando os top 10
        fornecedores_recorrentes = (
            df_filtrado.groupby("nome_fornecedor", as_index=False)
            .agg(
                total_contratos=("id_licitacao", "count"),
                valor_total=("valor_contratado", "sum"),
            )
            .sort_values("total_contratos", ascending=False)
            .head(10)
        )

        # Cria um gráfico de barras horizontais para os fornecedores mais recorrentes
        fig_fornecedor = px.bar(
            fornecedores_recorrentes,
            x="total_contratos",
            y="nome_fornecedor",
            orientation="h",
            title="Top 10 fornecedores recorrentes",
            labels={
                "total_contratos": "Total de contratos",
                "nome_fornecedor": "Fornecedor",
            },
        )

        # Inverte a ordem do eixo Y para que o maior valor fique no topo
        fig_fornecedor.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_fornecedor, use_container_width=True)  # Exibe o gráfico

    # Cria mais colunas para exibir gráficos adicionais
    col1, col2 = st.columns(2)

    with col1:
        # Agrupa dados por categoria e calcula o valor total contratado
        valor_categoria = (
            df_filtrado.groupby("categoria", as_index=False)["valor_contratado"]
            .sum()
            .sort_values("valor_contratado", ascending=False)
        )

        # Cria um gráfico de pizza para a distribuição de valor por categoria
        fig_categoria = px.pie(
            valor_categoria,
            names="categoria",
            values="valor_contratado",
            title="Distribuição de valor por categoria",
        )

        st.plotly_chart(fig_categoria, use_container_width=True)  # Exibe o gráfico

    with col2:
        # Agrupa dados por nível de risco original e conta o número de licitações
        risco_original = (
            df_filtrado.groupby("nivel_risco", as_index=False)["id_licitacao"]
            .count()
            .rename(columns={"id_licitacao": "total"})
        )

        # Cria um gráfico de barras para a distribuição por nível de risco original
        fig_risco = px.bar(
            risco_original,
            x="nivel_risco",
            y="total",
            title="Distribuição por nível de risco original",
            labels={
                "nivel_risco": "Nível de risco",
                "total": "Total",
            },
        )

        st.plotly_chart(fig_risco, use_container_width=True)  # Exibe o gráfico

    st.subheader("Evolução mensal dos contratos")  # Adiciona um subtítulo

    # Agrupa dados por ano e mês para calcular a evolução mensal do valor contratado
    evolucao_mensal = (
        df_filtrado.groupby(["ano", "mes"], as_index=False)["valor_contratado"]
        .sum()
        .sort_values(["ano", "mes"])
    )

    # Cria uma coluna para a combinação Ano-Mês para o eixo X
    evolucao_mensal["ano_mes"] = (
        evolucao_mensal["ano"].astype(str)
        + "-"
        + evolucao_mensal["mes"].astype(str).str.zfill(2)
    )

    # Cria um gráfico de linha para a evolução mensal do valor contratado
    fig_evolucao = px.line(
        evolucao_mensal,
        x="ano_mes",
        y="valor_contratado",
        markers=True,
        title="Evolução mensal do valor contratado",
        labels={
            "ano_mes": "Ano/Mês",
            "valor_contratado": "Valor contratado",
        },
    )

    st.plotly_chart(fig_evolucao, use_container_width=True)  # Exibe o gráfico


# ============================================================
# Aba 2 - Anomalias: Detecção de anomalias usando Machine Learning
# ============================================================

with aba_anomalias:
    st.subheader("Detecção de Anomalias")  # Subtítulo para a seção

    # Verifica se o DataFrame de ML (com anomalias) está vazio
    if df_ml.empty:
        st.warning(
            "Arquivo de ML não encontrado. Execute: python -m src.ml.risk_classification"
        )  # Mensagem de aviso
    else:
        # Calcula métricas relacionadas à detecção de anomalias
        total_registros_ml = len(df_ml)  # Total de registros analisados pelo ML
        # Conta o número de anomalias (onde 'ml_is_anomalia' é 'true')
        total_anomalias = df_ml[df_ml["ml_is_anomalia"].astype(str).str.lower() == "true"].shape[0]
        # Calcula o percentual de anomalias
        percentual_anomalias = (
            total_anomalias / total_registros_ml * 100
            if total_registros_ml > 0
            else 0
        )

        # Exibe as métricas em colunas
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Registros analisados", f"{total_registros_ml:,}".replace(",", ".")
            )  # Métrica de registros analisados

        with col2:
            st.metric("Anomalias detectadas", total_anomalias)  # Métrica de anomalias detectadas

        with col3:
            st.metric(
                "% de anomalias", f"{percentual_anomalias:.2f}%"
            )  # Métrica de percentual de anomalias

        st.divider()  # Adiciona um divisor visual

        # Converte a coluna 'ml_is_anomalia' para booleano para facilitar a filtragem
        df_ml["ml_is_anomalia_bool"] = (
            df_ml["ml_is_anomalia"].astype(str).str.lower() == "true"
        )

        # Filtra apenas os registros que são anomalias
        anomalias = df_ml[df_ml["ml_is_anomalia_bool"]].copy()

        # Cria colunas para exibir gráficos de anomalias
        col1, col2 = st.columns(2)

        with col1:
            # Agrupa por nível de alerta de ML e conta as licitações
            alerta = (
                df_ml.groupby("ml_nivel_alerta", as_index=False)["id_licitacao"]
                .count()
                .rename(columns={"id_licitacao": "total"})
            )

            # Cria um gráfico de barras para a distribuição por alerta de anomalia
            fig_alerta = px.bar(
                alerta,
                x="ml_nivel_alerta",
                y="total",
                title="Distribuição por alerta de anomalia",
                labels={
                    "ml_nivel_alerta": "Alerta ML",
                    "total": "Total",
                },
            )

            st.plotly_chart(fig_alerta, use_container_width=True)  # Exibe o gráfico

        with col2:
            # Agrupa anomalias por categoria e conta o total, pegando as top 10
            anomalias_categoria = (
                anomalias.groupby("categoria", as_index=False)["id_licitacao"]
                .count()
                .rename(columns={"id_licitacao": "total_anomalias"})
                .sort_values("total_anomalias", ascending=False)
                .head(10)
            )

            # Cria um gráfico de barras horizontais para as top categorias com anomalias
            fig_anomalias_categoria = px.bar(
                anomalias_categoria,
                x="total_anomalias",
                y="categoria",
                orientation="h",
                title="Top categorias com anomalias",
                labels={
                    "total_anomalias": "Total de anomalias",
                    "categoria": "Categoria",
                },
            )

            # Inverte a ordem do eixo Y
            fig_anomalias_categoria.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_anomalias_categoria, use_container_width=True)  # Exibe o gráfico

        st.subheader("Top anomalias detectadas")  # Subtítulo para a tabela

        # Define as colunas a serem exibidas na tabela de anomalias
        colunas_anomalias = [
            "numero_processo",
            "nome_orgao",
            "nome_fornecedor",
            "categoria",
            "modalidade",
            "valor_contratado",
            "percentual_diferenca",
            "score_risco",
            "nivel_risco",
            "ml_nivel_alerta",
        ]

        # Exibe um DataFrame com as 50 principais anomalias, ordenadas por score de risco e valor
        st.dataframe(
            anomalias.sort_values(
                ["score_risco", "valor_contratado"],
                ascending=False,
            )[colunas_anomalias].head(50),
            use_container_width=True,
        )


# ============================================================
# Aba 3 - Classificação de Risco: Exibição da classificação final de risco
# ============================================================

with aba_risco:
    st.subheader("Classificação Final de Risco")  # Subtítulo para a seção

    # Verifica se o DataFrame de ML (com classificação de risco) está vazio
    if df_ml.empty:
        st.warning(
            "Arquivo de classificação não encontrado. Execute: python -m src.ml.risk_classification"
        )  # Mensagem de aviso
    else:
        # Cria colunas para exibir gráficos de classificação de risco
        col1, col2 = st.columns(2)

        with col1:
            # Agrupa por nível de risco final de ML e conta as licitações
            risco_final = (
                df_ml.groupby("ml_nivel_risco_final", as_index=False)["id_licitacao"]
                .count()
                .rename(columns={"id_licitacao": "total"})
            )

            # Cria um gráfico de barras para a distribuição por risco final
            fig_risco_final = px.bar(
                risco_final,
                x="ml_nivel_risco_final",
                y="total",
                title="Distribuição por risco final",
                labels={
                    "ml_nivel_risco_final": "Risco final",
                    "total": "Total",
                },
            )

            st.plotly_chart(fig_risco_final, use_container_width=True)  # Exibe o gráfico

        with col2:
            # Agrupa por prioridade de auditoria e conta as licitações
            prioridade = (
                df_ml.groupby("prioridade_auditoria", as_index=False)["id_licitacao"]
                .count()
                .rename(columns={"id_licitacao": "total"})
                .sort_values("total", ascending=False)
            )

            # Cria um gráfico de barras para a distribuição por prioridade de auditoria
            fig_prioridade = px.bar(
                prioridade,
                x="prioridade_auditoria",
                y="total",
                title="Distribuição por prioridade de auditoria",
                labels={
                    "prioridade_auditoria": "Prioridade",
                    "total": "Total",
                },
            )

            st.plotly_chart(fig_prioridade, use_container_width=True)  # Exibe o gráfico

        st.subheader("Licitações com maior prioridade de auditoria")  # Subtítulo para a tabela

        # Lista de prioridades de auditoria
        prioridades = [
            "Prioridade Máxima",
            "Prioridade Alta",
            "Prioridade Média",
            "Prioridade Baixa",
            "Monitoramento",
        ]

        # Cria um selectbox para filtrar a tabela por prioridade
        prioridade_selecionada = st.selectbox(
            "Filtrar por prioridade",
            options=["Todas"] + prioridades,
        )

        # Copia o DataFrame de ML para aplicar o filtro
        df_risco_filtrado = df_ml.copy()

        # Aplica o filtro de prioridade, se uma opção diferente de "Todas" for selecionada
        if prioridade_selecionada != "Todas":
            df_risco_filtrado = df_risco_filtrado[
                df_risco_filtrado["prioridade_auditoria"] == prioridade_selecionada
            ]

        # Define as colunas a serem exibidas na tabela de classificação de risco
        colunas_risco = [
            "numero_processo",
            "nome_orgao",
            "nome_fornecedor",
            "categoria",
            "valor_contratado",
            "percentual_diferenca",
            "ml_is_anomalia",
            "ml_score_risco_final",
            "ml_nivel_risco_final",
            "prioridade_auditoria",
            "motivos_risco",
        ]

        # Exibe um DataFrame com as 100 principais licitações, ordenadas por score de risco final e valor
        st.dataframe(
            df_risco_filtrado.sort_values(
                ["ml_score_risco_final", "valor_contratado"],
                ascending=False,
            )[colunas_risco].head(100),
            use_container_width=True,
        )


# ============================================================
# Aba 4 - Fornecedores: Exibição de informações sobre a clusterização de fornecedores
# ============================================================

with aba_fornecedores:
    st.subheader("Clusterização de Fornecedores")  # Subtítulo para a seção

    # Verifica se o DataFrame de fornecedores clusterizados está vazio
    if df_fornecedores.empty:
        st.warning(
            "Arquivo de fornecedores clusterizados não encontrado. Execute: python -m src.ml.supplier_clustering"
        )  # Mensagem de aviso
    else:
        # Calcula métricas relacionadas à clusterização de fornecedores
        total_fornecedores_cluster = len(
            df_fornecedores
        )  # Total de fornecedores analisados
        # Conta fornecedores com perfil de "Atenção Especial"
        fornecedores_atencao = df_fornecedores[
            df_fornecedores["perfil_cluster"] == "Fornecedor com atenção especial"
        ].shape[0]

        # Exibe as métricas em colunas
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Fornecedores analisados", total_fornecedores_cluster
            )  # Métrica de fornecedores analisados

        with col2:
            st.metric(
                "Fornecedores com atenção especial", fornecedores_atencao
            )  # Métrica de fornecedores com atenção especial

        with col3:
            # Calcula o percentual de fornecedores com atenção especial
            percentual_atencao = (
                fornecedores_atencao / total_fornecedores_cluster * 100
                if total_fornecedores_cluster > 0
                else 0
            )
            st.metric(
                "% atenção especial", f"{percentual_atencao:.2f}%"
            )  # Métrica de percentual

        st.divider()  # Adiciona um divisor visual

        # Cria colunas para exibir gráficos de clusterização
        col1, col2 = st.columns(2)

        with col1:
            # Agrupa por perfil de cluster e conta o número de fornecedores
            perfil = (
                df_fornecedores.groupby("perfil_cluster", as_index=False)[
                    "nome_fornecedor"
                ]
                .count()
                .rename(columns={"nome_fornecedor": "total"})
                .sort_values("total", ascending=False)
            )

            # Cria um gráfico de pizza para a distribuição dos perfis de fornecedores
            fig_perfil = px.pie(
                perfil,
                names="perfil_cluster",
                values="total",
                title="Distribuição dos perfis de fornecedores",
            )

            st.plotly_chart(fig_perfil, use_container_width=True)  # Exibe o gráfico

        with col2:
            # Agrupa por perfil de cluster e calcula o valor total contratado
            valor_perfil = (
                df_fornecedores.groupby("perfil_cluster", as_index=False)[
                    "valor_total_contratado"
                ]
                .sum()
                .sort_values("valor_total_contratado", ascending=False)
            )

            # Cria um gráfico de barras para o valor total contratado por perfil de fornecedor
            fig_valor_perfil = px.bar(
                valor_perfil,
                x="perfil_cluster",
                y="valor_total_contratado",
                title="Valor total contratado por perfil de fornecedor",
                labels={
                    "perfil_cluster": "Perfil",
                    "valor_total_contratado": "Valor total contratado",
                },
            )

            st.plotly_chart(fig_valor_perfil, use_container_width=True)  # Exibe o gráfico

        st.subheader("Base de fornecedores clusterizados")  # Subtítulo para a tabela

        # Cria um selectbox para filtrar a tabela por perfil de cluster
        perfil_selecionado = st.selectbox(
            "Filtrar por perfil",
            options=["Todos"]
            + sorted(df_fornecedores["perfil_cluster"].unique().tolist()),
        )

        # Copia o DataFrame de fornecedores para aplicar o filtro
        df_fornecedor_filtrado = df_fornecedores.copy()

        # Aplica o filtro de perfil, se uma opção diferente de "Todos" for selecionada
        if perfil_selecionado != "Todos":
            df_fornecedor_filtrado = df_fornecedor_filtrado[
                df_fornecedor_filtrado["perfil_cluster"] == perfil_selecionado
            ]

        # Define as colunas a serem exibidas na tabela de fornecedores
        colunas_fornecedores = [
            "nome_fornecedor",
            "total_contratos",
            "total_orgaos",
            "total_categorias",
            "valor_total_contratado",
            "valor_medio_contrato",
            "score_medio_final",
            "total_anomalias",
            "contratos_alto_critico",
            "percentual_anomalias",
            "percentual_alto_critico",
            "perfil_cluster",
            "descricao_cluster",
        ]

        # Exibe um DataFrame com os fornecedores, ordenados por valor total contratado e score médio final
        st.dataframe(
            df_fornecedor_filtrado.sort_values(
                ["valor_total_contratado", "score_medio_final"],
                ascending=False,
            )[colunas_fornecedores],
            use_container_width=True,
        )


# ============================================================
# Rodapé da aplicação
# ============================================================

# Exibe uma pequena legenda no rodapé da página
st.caption(
    "Projeto de portfólio em Engenharia de Dados, Análise de Dados e Ciência de Dados aplicado a licitações públicas."
)