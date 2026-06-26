import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


# ============================================================
# Configuração inicial
# ============================================================
# Carrega as variáveis de ambiente do arquivo .env (se existir)

load_dotenv()

st.set_page_config(
    page_title="Licitações Risk Intelligence",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# Conexão com o banco
# ============================================================

def get_database_url() -> str:
    # Tenta obter a URL de conexão completa a partir da variável de ambiente DATABASE_URL
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        user = os.getenv("POSTGRES_USER", "admin")
        password = os.getenv("POSTGRES_PASSWORD", "admin")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5433")
        database = os.getenv("POSTGRES_DB", "licitacoes_db")

        # Monta a URL de conexão a partir das variáveis de ambiente individuais
        database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    return database_url


@st.cache_resource
def get_engine():
    # Cria e armazena em cache a engine de conexão com o banco de dados
    # O cache _resource garante que a conexão seja criada apenas uma vez
    return create_engine(get_database_url())


@st.cache_data(ttl=60)
def carregar_dados() -> pd.DataFrame:
    # Carrega os dados da view analítica e armazena em cache
    # O cache _data garante que a consulta ao banco seja executada apenas uma vez
    engine = get_engine()

    query = """
        SELECT *
        FROM vw_licitacoes_analytics;
    """

    df = pd.read_sql(query, engine)

    # Converte a coluna de data para o formato datetime do pandas
    df["data"] = pd.to_datetime(df["data"])

    return df


# ============================================================
# Carregamento dos dados
# ============================================================

# Executa a função para carregar o DataFrame principal do dashboard
if st.sidebar.button("Atualizar dados"):
    carregar_dados.clear()
    st.cache_resource.clear()
    st.rerun()

df = carregar_dados()

st.write("Total carregado do banco:", len(df))
st.write(df.head())

# ============================================================
# Sidebar
# ============================================================

# Título da barra lateral
st.sidebar.title("Filtros")

# Extrai listas de valores únicos para preencher os filtros
anos = sorted(df["ano"].dropna().unique())
orgaos = sorted(df["nome_orgao"].dropna().unique())
categorias = sorted(df["categoria"].dropna().unique())
niveis_risco = sorted(df["nivel_risco"].dropna().unique())

# Cria os widgets de filtro multiselect na barra lateral
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
    "Nível de risco",
    options=niveis_risco,
    default=list(niveis_risco),
)

# Aplica os filtros selecionados ao DataFrame principal
df_filtrado = df.copy()

if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado["ano"].isin(anos_selecionados)]

if orgaos_selecionados:
    df_filtrado = df_filtrado[df_filtrado["nome_orgao"].isin(orgaos_selecionados)]

if categorias_selecionadas:
    df_filtrado = df_filtrado[df_filtrado["categoria"].isin(categorias_selecionadas)]

if riscos_selecionados:
    df_filtrado = df_filtrado[df_filtrado["nivel_risco"].isin(riscos_selecionados)]


# ============================================================
# Cabeçalho
# ============================================================

# Título principal do dashboard
st.title("📊 Licitações Risk Intelligence Platform")

# Descrição do projeto
st.markdown(
    """
    Plataforma analítica para monitoramento de licitações públicas, identificação de padrões de risco,
    fornecedores recorrentes, contratos acima da média e anomalias em compras públicas.
    """
)


# ============================================================
# KPIs
# ============================================================

# Calcula os principais indicadores com base nos dados filtrados
total_licitacoes = len(df_filtrado)
valor_total = df_filtrado["valor_contratado"].sum()
valor_medio = df_filtrado["valor_contratado"].mean()
total_fornecedores = df_filtrado["nome_fornecedor"].nunique()
total_orgaos = df_filtrado["nome_orgao"].nunique()
total_alto_critico = df_filtrado[df_filtrado["nivel_risco"].isin(["Alto", "Crítico"])].shape[0]
percentual_alto_critico = (
    (total_alto_critico / total_licitacoes) * 100 if total_licitacoes > 0 else 0
)

# Organiza os KPIs em três colunas
col1, col2, col3 = st.columns(3)

with col1:
    # Exibe as métricas na primeira coluna
    st.metric("Total de licitações", f"{total_licitacoes:,}".replace(",", "."))
    st.metric("Total de órgãos", total_orgaos)

with col2:
    # Exibe as métricas na segunda coluna
    st.metric("Valor total contratado", f"R$ {valor_total:,.2f}")
    st.metric("Total de fornecedores", total_fornecedores)

with col3:
    # Exibe as métricas na terceira coluna
    st.metric("Valor médio contratado", f"R$ {valor_medio:,.2f}")
    st.metric("Risco alto/crítico", f"{percentual_alto_critico:.2f}%")


# Adiciona uma linha divisória
st.divider()


# ============================================================
# Gráficos principais
# ============================================================

st.subheader("Visão geral das licitações")

# Cria duas colunas para os gráficos principais
col1, col2 = st.columns(2)

with col1:
    # Agrupa os dados por órgão para calcular o valor total contratado
    valor_por_orgao = (
        df_filtrado.groupby("nome_orgao", as_index=False)["valor_contratado"]
        .sum()
        .sort_values("valor_contratado", ascending=False)
        .head(10) # Seleciona o top 10
    )

    # Cria o gráfico de barras com Plotly Express
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

    # Ordena as barras do gráfico do maior para o menor
    fig_orgao.update_layout(yaxis={"categoryorder": "total ascending"})

    st.plotly_chart(fig_orgao, use_container_width=True)

with col2:
    # Agrupa os dados por fornecedor para contar o número de contratos
    fornecedores = (
        df_filtrado.groupby("nome_fornecedor", as_index=False)
        .agg(
            total_contratos=("id_licitacao", "count"),
            valor_total=("valor_contratado", "sum"),
        )
        .sort_values("total_contratos", ascending=False)
        .head(10) # Seleciona o top 10
    )

    # Cria o gráfico de barras dos fornecedores mais recorrentes
    fig_fornecedor = px.bar(
        fornecedores,
        x="total_contratos",
        y="nome_fornecedor",
        orientation="h",
        title="Top 10 fornecedores recorrentes",
        labels={
            "total_contratos": "Total de contratos",
            "nome_fornecedor": "Fornecedor",
        },
    )

    fig_fornecedor.update_layout(yaxis={"categoryorder": "total ascending"})

    st.plotly_chart(fig_fornecedor, use_container_width=True)

# Cria mais duas colunas para os gráficos de pizza e de risco
col1, col2 = st.columns(2)

with col1:
    # Agrupa os dados por categoria para somar o valor contratado
    valor_categoria = (
        df_filtrado.groupby("categoria", as_index=False)["valor_contratado"]
        .sum()
        .sort_values("valor_contratado", ascending=False)
    )

    # Cria o gráfico de pizza para mostrar a distribuição de valor por categoria
    fig_categoria = px.pie(
        valor_categoria,
        names="categoria",
        values="valor_contratado",
        title="Distribuição de valor por categoria",
    )

    st.plotly_chart(fig_categoria, use_container_width=True)

with col2:
    # Agrupa os dados por nível de risco para contar o total de licitações
    risco = (
        df_filtrado.groupby("nivel_risco", as_index=False)["id_licitacao"]
        .count()
        .rename(columns={"id_licitacao": "total"})
    )

    # Define uma ordem personalizada para os níveis de risco no gráfico
    ordem_risco = ["Baixo", "Médio", "Alto", "Crítico"]
    risco["nivel_risco"] = pd.Categorical(
        risco["nivel_risco"],
        categories=ordem_risco,
        ordered=True,
    )
    risco = risco.sort_values("nivel_risco")

    # Cria o gráfico de barras para a distribuição por nível de risco
    fig_risco = px.bar(
        risco,
        x="nivel_risco",
        y="total",
        title="Distribuição por nível de risco",
        labels={
            "nivel_risco": "Nível de risco",
            "total": "Total de licitações",
        },
    )

    st.plotly_chart(fig_risco, use_container_width=True)


# ============================================================
# Evolução mensal
# ============================================================

st.subheader("Evolução mensal dos contratos")

# Agrupa os dados por ano e mês para somar o valor contratado
evolucao_mensal = (
    df_filtrado.groupby(["ano", "mes"], as_index=False)["valor_contratado"]
    .sum()
    .sort_values(["ano", "mes"])
)

# Cria uma coluna 'ano_mes' para ser usada como eixo X no gráfico
evolucao_mensal["ano_mes"] = (
    evolucao_mensal["ano"].astype(str)
    + "-"
    + evolucao_mensal["mes"].astype(str).str.zfill(2)
)

# Cria o gráfico de linha para mostrar a evolução mensal
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

st.plotly_chart(fig_evolucao, use_container_width=True)


# ============================================================
# Contratos acima da média
# ============================================================

st.subheader("Contratos com maior risco")

# Ordena o DataFrame pelo score de risco e valor contratado para criar um ranking
ranking_risco = df_filtrado.sort_values(
    by=["score_risco", "valor_contratado"],
    ascending=False,
).head(20) # Seleciona os 20 primeiros

# Exibe o ranking em uma tabela (DataFrame)
st.dataframe(
    # Seleciona e reordena as colunas a serem exibidas
    ranking_risco[
        [
            "numero_processo",
            "nome_orgao",
            "nome_fornecedor",
            "categoria",
            "modalidade",
            "valor_estimado",
            "valor_contratado",
            "percentual_diferenca",
            "score_risco",
            "nivel_risco",
            "is_anomalia",
        ]
    ],
    use_container_width=True,
)


# ============================================================
# Análise por fornecedor
# ============================================================

st.subheader("Análise de fornecedores")

# Agrupa os dados por fornecedor e calcula várias métricas agregadas
analise_fornecedor = (
    df_filtrado.groupby("nome_fornecedor", as_index=False)
    .agg(
        total_contratos=("id_licitacao", "count"),
        total_orgaos=("nome_orgao", "nunique"),
        valor_total=("valor_contratado", "sum"),
        valor_medio=("valor_contratado", "mean"),
        score_medio=("score_risco", "mean"),
    )
    .sort_values(["total_contratos", "valor_total"], ascending=False)
)

# Exibe a tabela de análise de fornecedores
st.dataframe(analise_fornecedor, use_container_width=True)


# ============================================================
# Rodapé
# ============================================================

# Adiciona uma legenda no final da página
st.caption(
    "Projeto de portfólio em Engenharia de Dados, Análise de Dados e Ciência de Dados aplicado a licitações públicas."
)
