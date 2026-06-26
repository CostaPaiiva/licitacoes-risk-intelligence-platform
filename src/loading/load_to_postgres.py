import os

import pandas as pd
from sqlalchemy import text

from src.utils.database import get_engine


# ============================================================
# Configurações de caminhos
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Caminho da base processada que alimenta a carga.
PROCESSED_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "licitacoes_processed.csv",
)


# ============================================================
# Funções auxiliares
# ============================================================

def carregar_csv_processado() -> pd.DataFrame:
    """
    Carrega o arquivo processado de licitações.
    """
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(
            f"Arquivo processado não encontrado: {PROCESSED_DATA_PATH}. "
            "Execute primeiro o script src/transformation/transform_licitacoes.py"
        )

    # Carrega o CSV já tratado para preparar a inserção no banco.
    df = pd.read_csv(PROCESSED_DATA_PATH)

    print("Arquivo processado carregado com sucesso.")
    print(f"Total de registros para carga: {len(df)}")

    return df


def limpar_tabelas(engine) -> None:
    """
    Limpa as tabelas antes de uma nova carga.
    A ordem respeita as dependências da tabela fato com as dimensões.
    """
    # Limpa primeiro a fato e depois as dimensões para evitar conflito de FK.
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE fato_licitacoes RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_tempo RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_localidade RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_categoria RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_fornecedor RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_orgao RESTART IDENTITY CASCADE;"))

    print("Tabelas limpas com sucesso.")


def carregar_dim_orgao(df: pd.DataFrame, engine) -> pd.DataFrame:
    """
    Carrega a dimensão de órgãos públicos.
    """
    # Deduplica os órgãos antes de gravar a dimensão.
    dim_orgao = (
        df[["orgao"]]
        .drop_duplicates()
        .sort_values("orgao")
        .reset_index(drop=True)
    )

    dim_orgao["esfera"] = dim_orgao["orgao"].apply(
        lambda x: "Municipal" if "Municipal" in x or "Prefeitura" in x or "Câmara" in x else "Estadual"
    )

    # Classifica o órgão para facilitar análises por tipo institucional.
    dim_orgao["tipo_orgao"] = dim_orgao["orgao"].apply(classificar_tipo_orgao)

    dim_orgao = dim_orgao.rename(columns={"orgao": "nome_orgao"})

    dim_orgao.to_sql("dim_orgao", engine, if_exists="append", index=False)

    dim_orgao_db = pd.read_sql("SELECT * FROM dim_orgao", engine)

    print(f"dim_orgao carregada: {len(dim_orgao_db)} registros")

    return dim_orgao_db


def classificar_tipo_orgao(nome_orgao: str) -> str:
    """
    Classifica o tipo de órgão com base no nome.
    """
    nome = str(nome_orgao).lower()

    # Regras simples de classificação por palavras-chave.
    if "prefeitura" in nome:
        return "Prefeitura"
    if "secretaria" in nome:
        return "Secretaria"
    if "tribunal" in nome:
        return "Tribunal"
    if "câmara" in nome:
        return "Câmara"
    if "departamento" in nome:
        return "Departamento"
    if "instituto" in nome:
        return "Instituto"
    if "fundação" in nome:
        return "Fundação"

    return "Outros"


def carregar_dim_fornecedor(df: pd.DataFrame, engine) -> pd.DataFrame:
    """
    Carrega a dimensão de fornecedores.
    """
    # Garante um cadastro único de fornecedor por nome/CNPJ/porte.
    dim_fornecedor = (
        df[["fornecedor", "cnpj_formatado", "porte_empresa"]]
        .drop_duplicates()
        .sort_values("fornecedor")
        .reset_index(drop=True)
    )

    dim_fornecedor = dim_fornecedor.rename(
        columns={
            "fornecedor": "nome_fornecedor",
            "cnpj_formatado": "cnpj",
        }
    )

    dim_fornecedor.to_sql("dim_fornecedor", engine, if_exists="append", index=False)

    dim_fornecedor_db = pd.read_sql("SELECT * FROM dim_fornecedor", engine)

    print(f"dim_fornecedor carregada: {len(dim_fornecedor_db)} registros")

    return dim_fornecedor_db


def carregar_dim_categoria(df: pd.DataFrame, engine) -> pd.DataFrame:
    """
    Carrega a dimensão de categorias de contratação.
    """
    # Normaliza a combinação categoria + grupo_categoria.
    dim_categoria = (
        df[["categoria", "grupo_categoria"]]
        .drop_duplicates()
        .sort_values("categoria")
        .reset_index(drop=True)
    )

    dim_categoria.to_sql("dim_categoria", engine, if_exists="append", index=False)

    dim_categoria_db = pd.read_sql("SELECT * FROM dim_categoria", engine)

    print(f"dim_categoria carregada: {len(dim_categoria_db)} registros")

    return dim_categoria_db


def carregar_dim_localidade(df: pd.DataFrame, engine) -> pd.DataFrame:
    """
    Carrega a dimensão de localidades.
    """
    # Reduz a base para localidades únicas antes de persistir.
    dim_localidade = (
        df[["cidade", "estado", "regiao"]]
        .drop_duplicates()
        .sort_values(["estado", "cidade"])
        .reset_index(drop=True)
    )

    dim_localidade.to_sql("dim_localidade", engine, if_exists="append", index=False)

    dim_localidade_db = pd.read_sql("SELECT * FROM dim_localidade", engine)

    print(f"dim_localidade carregada: {len(dim_localidade_db)} registros")

    return dim_localidade_db


def carregar_dim_tempo(df: pd.DataFrame, engine) -> pd.DataFrame:
    """
    Carrega a dimensão de tempo.
    """
    # Usa a data de publicação como grão da dimensão temporal.
    dim_tempo = (
        df[["data_publicacao", "ano_publicacao", "mes_publicacao", "nome_mes", "trimestre"]]
        .drop_duplicates()
        .sort_values("data_publicacao")
        .reset_index(drop=True)
    )

    dim_tempo = dim_tempo.rename(
        columns={
            "data_publicacao": "data",
            "ano_publicacao": "ano",
            "mes_publicacao": "mes",
        }
    )

    # Garante a mesma granularidade usada na comparação com a tabela fato.
    dim_tempo["data"] = pd.to_datetime(dim_tempo["data"]).dt.date

    dim_tempo.to_sql("dim_tempo", engine, if_exists="append", index=False)

    dim_tempo_db = pd.read_sql("SELECT * FROM dim_tempo", engine)

    print(f"dim_tempo carregada: {len(dim_tempo_db)} registros")

    return dim_tempo_db


def montar_fato_licitacoes(
    df: pd.DataFrame,
    dim_orgao: pd.DataFrame,
    dim_fornecedor: pd.DataFrame,
    dim_categoria: pd.DataFrame,
    dim_localidade: pd.DataFrame,
    dim_tempo: pd.DataFrame,
) -> pd.DataFrame:
    """
    Monta a tabela fato com as chaves das dimensões.
    """
    # Parte da base tratada e resolve as chaves surrogate de cada dimensão.
    fato = df.copy()
    fato["data_publicacao"] = pd.to_datetime(fato["data_publicacao"]).dt.date

    fato = fato.merge(
        dim_orgao[["id_orgao", "nome_orgao"]],
        left_on="orgao",
        right_on="nome_orgao",
        how="left",
    )

    fato = fato.merge(
        dim_fornecedor[["id_fornecedor", "nome_fornecedor", "cnpj"]],
        left_on=["fornecedor", "cnpj_formatado"],
        right_on=["nome_fornecedor", "cnpj"],
        how="left",
    )

    fato = fato.merge(
        dim_categoria[["id_categoria", "categoria", "grupo_categoria"]],
        on=["categoria", "grupo_categoria"],
        how="left",
    )

    fato = fato.merge(
        dim_localidade[["id_localidade", "cidade", "estado", "regiao"]],
        on=["cidade", "estado", "regiao"],
        how="left",
    )

    fato = fato.merge(
        dim_tempo[["id_tempo", "data"]],
        left_on="data_publicacao",
        right_on="data",
        how="left",
    )

    fato_final = fato[
        [
            "numero_processo",
            "id_orgao",
            "id_fornecedor",
            "id_categoria",
            "id_localidade",
            "id_tempo",
            "modalidade",
            "status",
            "descricao",
            "valor_estimado",
            "valor_contratado",
            "diferenca_valor",
            "percentual_diferenca",
            "score_risco",
            "nivel_risco",
            "possivel_outlier",
        ]
    ].copy()

    # Ajusta o nome do indicador para o formato esperado pela tabela fato.
    fato_final = fato_final.rename(
        columns={
            "possivel_outlier": "is_anomalia",
        }
    )

    print(f"fato_licitacoes montada: {len(fato_final)} registros")

    return fato_final


def carregar_fato_licitacoes(fato: pd.DataFrame, engine) -> None:
    """
    Carrega a tabela fato no PostgreSQL.
    """
    # Insere a fato já pronta para consulta analítica.
    fato.to_sql("fato_licitacoes", engine, if_exists="append", index=False)

    print(f"fato_licitacoes carregada: {len(fato)} registros")


def validar_carga(engine) -> None:
    """
    Valida a quantidade de registros carregados em cada tabela.
    """
    # Checagem simples para confirmar se cada tabela recebeu linhas.
    consultas = {
        "dim_orgao": "SELECT COUNT(*) AS total FROM dim_orgao;",
        "dim_fornecedor": "SELECT COUNT(*) AS total FROM dim_fornecedor;",
        "dim_categoria": "SELECT COUNT(*) AS total FROM dim_categoria;",
        "dim_localidade": "SELECT COUNT(*) AS total FROM dim_localidade;",
        "dim_tempo": "SELECT COUNT(*) AS total FROM dim_tempo;",
        "fato_licitacoes": "SELECT COUNT(*) AS total FROM fato_licitacoes;",
    }

    print("\nValidação da carga:")

    for tabela, query in consultas.items():
        resultado = pd.read_sql(query, engine)
        total = resultado.loc[0, "total"]
        print(f"{tabela}: {total} registros")


def executar_carga() -> None:
    """
    Executa o pipeline completo de carga no PostgreSQL.
    """
    # Orquestra a conexão, a limpeza e a carga das dimensões e da fato.
    engine = get_engine()

    df = carregar_csv_processado()

    limpar_tabelas(engine)

    dim_orgao = carregar_dim_orgao(df, engine)
    dim_fornecedor = carregar_dim_fornecedor(df, engine)
    dim_categoria = carregar_dim_categoria(df, engine)
    dim_localidade = carregar_dim_localidade(df, engine)
    dim_tempo = carregar_dim_tempo(df, engine)

    fato = montar_fato_licitacoes(
        df=df,
        dim_orgao=dim_orgao,
        dim_fornecedor=dim_fornecedor,
        dim_categoria=dim_categoria,
        dim_localidade=dim_localidade,
        dim_tempo=dim_tempo,
    )

    carregar_fato_licitacoes(fato, engine)

    validar_carga(engine)

    print("\nCarga no PostgreSQL concluída com sucesso!")


if __name__ == "__main__":
    executar_carga()
