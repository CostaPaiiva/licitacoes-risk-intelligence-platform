import os

import pandas as pd
from dotenv import load_dotenv
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine


# ============================================================
# Configurações iniciais
# ============================================================

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define o caminho de saída para o arquivo CSV com os resultados da detecção de anomalias
OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "licitacoes_anomaly_detection.csv",
)


# ============================================================
# Conexão com banco
# ============================================================

def get_database_url() -> str:
    # Tenta obter a URL de conexão completa a partir da variável de ambiente DATABASE_URL
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        # Se a URL completa não estiver definida, monta a partir de variáveis individuais
        user = os.getenv("POSTGRES_USER", "admin")
        password = os.getenv("POSTGRES_PASSWORD", "admin")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5433")
        database = os.getenv("POSTGRES_DB", "licitacoes_db")

        database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    return database_url


def get_engine():
    # Cria a engine de conexão com o banco de dados usando a URL obtida
    return create_engine(get_database_url())


# ============================================================
# Carregamento dos dados
# ============================================================

def carregar_dados() -> pd.DataFrame:
    # Obtém a engine de conexão com o banco
    engine = get_engine()

    # Define a query para carregar os dados da view analítica, que já consolida as informações
    query = """
        SELECT
            id_licitacao,
            numero_processo,
            nome_orgao,
            nome_fornecedor,
            categoria,
            modalidade,
            status,
            valor_estimado,
            valor_contratado,
            diferenca_valor,
            percentual_diferenca,
            score_risco,
            nivel_risco,
            is_anomalia
        FROM vw_licitacoes_analytics;
    """

    # Executa a query e carrega os dados em um DataFrame do pandas
    df = pd.read_sql(query, engine)

    print("Dados carregados com sucesso.")
    print(f"Total de registros: {len(df)}")

    return df


# ============================================================
# Feature engineering
# ============================================================

def preparar_features(df: pd.DataFrame) -> pd.DataFrame:
    # Cria uma cópia do DataFrame para evitar alterações no original
    df_modelo = df.copy()

    # Converte colunas numéricas para o tipo correto, tratando erros como NaN que serão preenchidos
    df_modelo["valor_estimado"] = pd.to_numeric(df_modelo["valor_estimado"], errors="coerce")
    df_modelo["valor_contratado"] = pd.to_numeric(df_modelo["valor_contratado"], errors="coerce")
    df_modelo["diferenca_valor"] = pd.to_numeric(df_modelo["diferenca_valor"], errors="coerce")
    df_modelo["percentual_diferenca"] = pd.to_numeric(df_modelo["percentual_diferenca"], errors="coerce")
    df_modelo["score_risco"] = pd.to_numeric(df_modelo["score_risco"], errors="coerce")

    # Preenche valores nulos com 0 após a conversão, para garantir que o modelo possa processar
    df_modelo = df_modelo.fillna(0)

    # Frequência do fornecedor
    # Cria uma feature que conta quantas vezes cada fornecedor aparece na base
    frequencia_fornecedor = (
        df_modelo.groupby("nome_fornecedor")["id_licitacao"]
        .count()
        .rename("frequencia_fornecedor")
    )

    df_modelo = df_modelo.merge(
        frequencia_fornecedor,
        on="nome_fornecedor",
        how="left",
    )

    # Frequência do órgão
    # Cria uma feature que conta quantas vezes cada órgão aparece na base
    frequencia_orgao = (
        df_modelo.groupby("nome_orgao")["id_licitacao"]
        .count()
        .rename("frequencia_orgao")
    )

    df_modelo = df_modelo.merge(
        frequencia_orgao,
        on="nome_orgao",
        how="left",
    )

    # Valor médio por categoria
    # Cria uma feature que calcula o valor médio contratado para cada categoria
    media_categoria = (
        df_modelo.groupby("categoria")["valor_contratado"]
        .mean()
        .rename("media_valor_categoria")
    )

    df_modelo = df_modelo.merge(
        media_categoria,
        on="categoria",
        how="left",
    )

    # Calcula o percentual que o valor de um contrato está acima da média de sua categoria
    df_modelo["percentual_acima_media_categoria"] = (
        (
            df_modelo["valor_contratado"] - df_modelo["media_valor_categoria"]
        )
        / df_modelo["media_valor_categoria"]
        * 100
    ).round(2)

    # Trata casos de divisão por zero (inf) e valores nulos
    df_modelo["percentual_acima_media_categoria"] = (
        df_modelo["percentual_acima_media_categoria"]
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
    )

    return df_modelo


# ============================================================
# Modelo de anomalia
# ============================================================

def detectar_anomalias(df: pd.DataFrame) -> pd.DataFrame:
    # Prepara as features necessárias para o modelo
    df_modelo = preparar_features(df)

    # Define a lista de features (variáveis) que o modelo usará para aprender os padrões
    features = [
        "valor_estimado",
        "valor_contratado",
        "diferenca_valor",
        "percentual_diferenca",
        "score_risco",
        "frequencia_fornecedor",
        "frequencia_orgao",
        "media_valor_categoria",
        "percentual_acima_media_categoria",
    ]

    # Seleciona apenas as colunas de features para o treinamento
    X = df_modelo[features]

    # Normaliza os dados para que todas as features tenham a mesma escala (média 0, desvio padrão 1)
    # Isso é importante para modelos baseados em distância como o Isolation Forest
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Instancia o modelo Isolation Forest
    modelo = IsolationForest(
        n_estimators=200,  # Número de árvores na floresta
        contamination=0.08,  # Proporção esperada de anomalias no dataset (hiperparâmetro)
        random_state=42,  # Semente para reprodutibilidade
    )

    # Treina o modelo e faz a predição. O resultado é -1 para anomalias e 1 para dados normais.
    df_modelo["ml_anomaly_flag"] = modelo.fit_predict(X_scaled)

    # No Isolation Forest:
    # -1 = anomalia
    #  1 = normal
    # Cria uma coluna booleana para facilitar a filtragem e interpretação
    df_modelo["ml_is_anomalia"] = df_modelo["ml_anomaly_flag"].apply(
        lambda x: True if x == -1 else False
    )

    # Calcula o "score de anomalia" para cada ponto. Quanto menor o score, mais anômalo é o ponto.
    df_modelo["ml_anomaly_score"] = modelo.decision_function(X_scaled)

    # Cria um nível de alerta combinando a predição do modelo com o score de risco baseado em regras
    df_modelo["ml_nivel_alerta"] = df_modelo.apply(classificar_alerta_ml, axis=1)

    print("Detecção de anomalias concluída.")
    print("\nDistribuição de anomalias detectadas pelo modelo:")
    print(df_modelo["ml_is_anomalia"].value_counts())

    print("\nDistribuição por nível de alerta ML:")
    print(df_modelo["ml_nivel_alerta"].value_counts())

    return df_modelo


def classificar_alerta_ml(row) -> str:
    # Define regras para classificar o nível de alerta, combinando a detecção do ML com o score de risco existente
    if row["ml_is_anomalia"] and row["score_risco"] >= 75:
        return "Crítico"
    if row["ml_is_anomalia"] and row["score_risco"] >= 50:
        return "Alto"
    if row["ml_is_anomalia"]:
        return "Médio"
    return "Normal"


# ============================================================
# Salvamento
# ============================================================

def salvar_resultado(df: pd.DataFrame) -> None:
    # Salva o DataFrame com os resultados da detecção de anomalias em um arquivo CSV
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print(f"\nArquivo salvo em: {OUTPUT_PATH}")

    # Imprime um resumo com as 10 anomalias mais críticas detectadas
    print("\nTop 10 possíveis anomalias:")
    # Define as colunas de interesse para o resumo
    colunas = [
        "numero_processo",
        "nome_orgao",
        "nome_fornecedor",
        "categoria",
        "valor_contratado",
        "percentual_diferenca",
        "score_risco",
        "nivel_risco",
        "ml_is_anomalia",
        "ml_nivel_alerta",
    ]

    # Filtra apenas as anomalias, ordena por score de risco e valor, e exibe o top 10
    print(
        df[df["ml_is_anomalia"]]
        .sort_values(["score_risco", "valor_contratado"], ascending=False)
        [colunas]
        .head(10)
    )


if __name__ == "__main__":
    # Ponto de entrada do script
    # Carrega os dados do banco
    dados = carregar_dados()
    # Executa a detecção de anomalias
    resultado = detectar_anomalias(dados)
    # Salva o resultado em um arquivo
    salvar_resultado(resultado)