import os
import re

import pandas as pd


# ============================================================
# Configurações de caminhos
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Caminhos da base bruta e do arquivo processado.
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "licitacoes_raw.csv")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
PROCESSED_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, "licitacoes_processed.csv")

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


# ============================================================
# Funções auxiliares
# ============================================================

def limpar_texto(valor: str) -> str:
    """
    Padroniza textos removendo espaços duplicados e ajustando capitalização.
    """
    if pd.isna(valor):
        return ""

    # Remove espaços repetidos e mantém o texto em uma forma consistente.
    valor = str(valor).strip()
    valor = re.sub(r"\s+", " ", valor)

    return valor


def limpar_cnpj(cnpj: str) -> str:
    """
    Remove caracteres especiais do CNPJ.
    Mantém apenas números.
    """
    if pd.isna(cnpj):
        return ""

    # Mantém apenas dígitos para permitir validação e formatação posterior.
    return re.sub(r"\D", "", str(cnpj))


def formatar_cnpj(cnpj_limpo: str) -> str:
    """
    Formata um CNPJ limpo com 14 dígitos.
    """
    if len(cnpj_limpo) != 14:
        return cnpj_limpo

    # Só aplica a máscara quando o CNPJ já está completo.
    return (
        f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/"
        f"{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
    )


def classificar_faixa_valor(valor: float) -> str:
    """
    Classifica a licitação por faixa de valor contratado.
    """
    if valor < 50_000:
        return "Até 50 mil"
    elif valor < 250_000:
        return "50 mil a 250 mil"
    elif valor < 1_000_000:
        return "250 mil a 1 milhão"
    elif valor < 5_000_000:
        return "1 milhão a 5 milhões"
    else:
        return "Acima de 5 milhões"


def classificar_variacao_percentual(percentual: float) -> str:
    """
    Classifica a diferença percentual entre valor contratado e valor estimado.
    """
    if percentual <= 0:
        return "Abaixo ou igual ao estimado"
    elif percentual <= 15:
        return "Até 15% acima"
    elif percentual <= 40:
        return "15% a 40% acima"
    else:
        return "Acima de 40%"


def validar_colunas_obrigatorias(df: pd.DataFrame) -> None:
    """
    Verifica se o arquivo bruto possui as colunas esperadas.
    """
    colunas_obrigatorias = [
        "id_licitacao",
        "numero_processo",
        "orgao",
        "cidade",
        "estado",
        "regiao",
        "categoria",
        "grupo_categoria",
        "descricao",
        "fornecedor",
        "cnpj_fornecedor",
        "porte_empresa",
        "valor_estimado",
        "valor_contratado",
        "diferenca_valor",
        "percentual_diferenca",
        "data_publicacao",
        "data_homologacao",
        "ano",
        "mes",
        "trimestre",
        "modalidade",
        "status",
        "fornecedor_recorrente",
        "possivel_outlier",
        "score_risco",
        "nivel_risco",
    ]

    colunas_ausentes = [col for col in colunas_obrigatorias if col not in df.columns]

    # Interrompe o pipeline cedo se o schema esperado não estiver presente.
    if colunas_ausentes:
        raise ValueError(f"Colunas ausentes no arquivo bruto: {colunas_ausentes}")


# ============================================================
# Pipeline de transformação
# ============================================================

def carregar_dados() -> pd.DataFrame:
    """
    Carrega os dados brutos de licitações.
    """
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Arquivo não encontrado: {RAW_DATA_PATH}")

    # Leitura da base de entrada em CSV.
    df = pd.read_csv(RAW_DATA_PATH)

    print("Dados brutos carregados com sucesso.")
    print(f"Total de registros brutos: {len(df)}")

    return df


def transformar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica tratamentos, padronizações e criação de novas colunas analíticas.
    """
    validar_colunas_obrigatorias(df)

    # Trabalha sobre uma cópia para não alterar o DataFrame original.
    df_transformado = df.copy()

    # Padronização textual
    colunas_texto = [
        "numero_processo",
        "orgao",
        "cidade",
        "estado",
        "regiao",
        "categoria",
        "grupo_categoria",
        "descricao",
        "fornecedor",
        "porte_empresa",
        "modalidade",
        "status",
        "nivel_risco",
    ]

    for coluna in colunas_texto:
        df_transformado[coluna] = df_transformado[coluna].apply(limpar_texto)

    # Tratamento de CNPJ
    df_transformado["cnpj_limpo"] = df_transformado["cnpj_fornecedor"].apply(limpar_cnpj)
    df_transformado["cnpj_formatado"] = df_transformado["cnpj_limpo"].apply(formatar_cnpj)

    # Tratamento de datas
    df_transformado["data_publicacao"] = pd.to_datetime(df_transformado["data_publicacao"])
    df_transformado["data_homologacao"] = pd.to_datetime(df_transformado["data_homologacao"])

    # Cria atributos temporais úteis para agregações e filtros.
    df_transformado["ano_publicacao"] = df_transformado["data_publicacao"].dt.year
    df_transformado["mes_publicacao"] = df_transformado["data_publicacao"].dt.month
    df_transformado["dia_publicacao"] = df_transformado["data_publicacao"].dt.day
    df_transformado["nome_mes"] = df_transformado["data_publicacao"].dt.month_name(locale="pt_BR")
    df_transformado["ano_mes"] = df_transformado["data_publicacao"].dt.to_period("M").astype(str)

    # Mede o tempo entre publicação e homologação em dias.
    df_transformado["dias_ate_homologacao"] = (
        df_transformado["data_homologacao"] - df_transformado["data_publicacao"]
    ).dt.days

    # Tratamento numérico
    colunas_numericas = [
        "valor_estimado",
        "valor_contratado",
        "diferenca_valor",
        "percentual_diferenca",
        "score_risco",
    ]

    for coluna in colunas_numericas:
        df_transformado[coluna] = pd.to_numeric(df_transformado[coluna], errors="coerce")

    # Remoção de registros inválidos
    # Remove linhas sem valores essenciais ou com valores não positivos.
    df_transformado = df_transformado.dropna(subset=["valor_estimado", "valor_contratado"])
    df_transformado = df_transformado[df_transformado["valor_estimado"] > 0]
    df_transformado = df_transformado[df_transformado["valor_contratado"] > 0]

    # Recalcular diferença para garantir consistência
    # Recalcula diferença e percentual com base nos dados já limpos.
    df_transformado["diferenca_valor"] = (
        df_transformado["valor_contratado"] - df_transformado["valor_estimado"]
    ).round(2)

    df_transformado["percentual_diferenca"] = (
        (df_transformado["diferenca_valor"] / df_transformado["valor_estimado"]) * 100
    ).round(2)

    # Novas colunas analíticas
    df_transformado["faixa_valor"] = df_transformado["valor_contratado"].apply(classificar_faixa_valor)
    df_transformado["faixa_variacao"] = df_transformado["percentual_diferenca"].apply(
        classificar_variacao_percentual
    )

    # Cria uma versão do valor contratado em milhões para leitura analítica.
    df_transformado["valor_milhoes"] = (df_transformado["valor_contratado"] / 1_000_000).round(2)

    # Indicadores booleanos para segmentação e regras de risco.
    df_transformado["is_valor_acima_estimado"] = df_transformado["valor_contratado"] > df_transformado["valor_estimado"]
    df_transformado["is_risco_alto_ou_critico"] = df_transformado["nivel_risco"].isin(["Alto", "Crítico"])
    df_transformado["is_dispensa_ou_inexigibilidade"] = df_transformado["modalidade"].isin(
        ["Dispensa de Licitação", "Inexigibilidade"]
    )

    # Ordenação final
    # Ordena o resultado por data e identificador para manter o output estável.
    df_transformado = df_transformado.sort_values(by=["data_publicacao", "id_licitacao"])

    print("Transformação concluída com sucesso.")
    print(f"Total de registros processados: {len(df_transformado)}")

    return df_transformado


def salvar_dados_processados(df: pd.DataFrame) -> None:
    """
    Salva os dados transformados em CSV.
    """
    # Exporta o dataset final em CSV com BOM para melhor compatibilidade.
    df.to_csv(PROCESSED_DATA_PATH, index=False, encoding="utf-8-sig")

    print(f"Arquivo processado salvo em: {PROCESSED_DATA_PATH}")

    print("\nResumo dos dados processados:")
    print(f"Total de licitações: {len(df)}")
    print(f"Valor total contratado: R$ {df['valor_contratado'].sum():,.2f}")
    print(f"Valor médio contratado: R$ {df['valor_contratado'].mean():,.2f}")
    print(f"Total de fornecedores únicos: {df['fornecedor'].nunique()}")
    print(f"Total de órgãos únicos: {df['orgao'].nunique()}")

    print("\nDistribuição por nível de risco:")
    print(df["nivel_risco"].value_counts())

    print("\nDistribuição por faixa de valor:")
    print(df["faixa_valor"].value_counts())


if __name__ == "__main__":
    dados_brutos = carregar_dados()
    dados_processados = transformar_dados(dados_brutos)
    salvar_dados_processados(dados_processados)
