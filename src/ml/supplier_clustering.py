import os # Importa o módulo 'os' para interagir com o sistema operacional, como manipulação de caminhos de arquivo.

import pandas as pd # Importa a biblioteca pandas para manipulação e análise de dados.
from sklearn.cluster import KMeans # Importa o algoritmo de clusterização KMeans da biblioteca scikit-learn.
from sklearn.preprocessing import StandardScaler # Importa o normalizador de dados StandardScaler do scikit-learn.


# ============================================================
# Configurações de caminhos
# ============================================================

# Define o diretório raiz do projeto para construir os caminhos de forma relativa.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define o caminho do arquivo de entrada, que é o resultado da etapa de classificação de risco.
INPUT_PATH = os.path.join(
    BASE_DIR, # Caminho raiz do projeto.
    "data", # Pasta de dados.
    "processed", # Subpasta de dados processados.
    "licitacoes_risk_classification.csv", # Nome do arquivo de entrada.
)

# Define o caminho do arquivo de saída, que conterá a base de fornecedores com seus clusters.
OUTPUT_PATH = os.path.join(
    BASE_DIR, # Caminho raiz do projeto.
    "data", # Pasta de dados.
    "processed", # Subpasta de dados processados.
    "fornecedores_clusterizados.csv", # Nome do arquivo de saída.
)


# ============================================================
# Carregamento dos dados
# ============================================================

def carregar_dados() -> pd.DataFrame: # Define a função 'carregar_dados' que retorna um DataFrame.
    """
    Carrega a base com classificação final de risco.
    """
    if not os.path.exists(INPUT_PATH): # Verifica se o arquivo de entrada necessário existe.
        raise FileNotFoundError(
            f"Arquivo não encontrado: {INPUT_PATH}. " # Mensagem de erro se o arquivo não for encontrado.
            "Execute primeiro o script src/ml/risk_classification.py" # Instrução para o usuário.
        )

    df = pd.read_csv(INPUT_PATH) # Lê o arquivo CSV para um DataFrame do pandas.

    print("Dados classificados carregados com sucesso.") # Confirma o carregamento.
    print(f"Total de licitações: {len(df)}") # Exibe o total de registros carregados.

    return df # Retorna o DataFrame carregado.


# ============================================================
# Preparação da base de fornecedores
# ============================================================

def preparar_base_fornecedores(df: pd.DataFrame) -> pd.DataFrame: # Define a função que recebe o DataFrame de licitações e retorna um DataFrame agregado por fornecedor.
    """
    Agrega os dados por fornecedor para permitir clusterização.
    """
    # Garante que as colunas numéricas sejam do tipo correto, preenchendo valores nulos com 0.
    df["valor_contratado"] = pd.to_numeric(df["valor_contratado"], errors="coerce").fillna(0)
    df["score_risco"] = pd.to_numeric(df["score_risco"], errors="coerce").fillna(0)
    df["ml_score_risco_final"] = pd.to_numeric(df["ml_score_risco_final"], errors="coerce").fillna(0)
    # Converte a coluna de anomalia para um tipo booleano consistente (True/False).
    df["ml_is_anomalia"] = df["ml_is_anomalia"].astype(str).str.lower().isin(["true", "1", "sim"])
    # Preenche níveis de risco nulos com "Baixo" para evitar erros na agregação.
    df["ml_nivel_risco_final"] = df["ml_nivel_risco_final"].fillna("Baixo")

    # Agrupa o DataFrame por 'nome_fornecedor' para criar uma visão consolidada de cada um.
    fornecedores = (
        df.groupby(["nome_fornecedor"], as_index=False)
        .agg( # Aplica várias funções de agregação para criar features que descrevem o comportamento do fornecedor.
            total_contratos=("id_licitacao", "count"), # Conta o número total de contratos.
            total_orgaos=("nome_orgao", "nunique"), # Conta com quantos órgãos distintos o fornecedor contratou.
            total_categorias=("categoria", "nunique"), # Conta em quantas categorias distintas o fornecedor atuou.
            valor_total_contratado=("valor_contratado", "sum"), # Soma o valor de todos os contratos.
            valor_medio_contrato=("valor_contratado", "mean"), # Calcula o valor médio dos contratos.
            maior_contrato=("valor_contratado", "max"), # Encontra o valor do maior contrato.
            score_medio_original=("score_risco", "mean"), # Calcula a média do score de risco original.
            score_medio_final=("ml_score_risco_final", "mean"), # Calcula a média do score de risco final (pós-ML).
            total_anomalias=("ml_is_anomalia", "sum"), # Soma o total de contratos marcados como anomalia.
            contratos_alto_critico=( # Conta quantos contratos foram classificados como 'Alto' ou 'Crítico'.
                "ml_nivel_risco_final",
                lambda x: x.isin(["Alto", "Crítico"]).sum(),
            ),
            contratos_criticos=( # Conta quantos contratos foram classificados como 'Crítico'.
                "ml_nivel_risco_final",
                lambda x: x.eq("Crítico").sum(),
            ),
        )
    )

    # Calcula o percentual de contratos que são anomalias.
    fornecedores["percentual_anomalias"] = (
        fornecedores["total_anomalias"] / fornecedores["total_contratos"] * 100
    ).round(2)

    # Calcula o percentual de contratos com risco 'Alto' ou 'Crítico'.
    fornecedores["percentual_alto_critico"] = (
        fornecedores["contratos_alto_critico"] / fornecedores["total_contratos"] * 100
    ).round(2)

    # Cria uma coluna com o valor total em milhões para facilitar a leitura.
    fornecedores["valor_total_milhoes"] = (
        fornecedores["valor_total_contratado"] / 1_000_000
    ).round(2)

    print("Base agregada por fornecedor criada com sucesso.") # Confirma a criação da base.
    print(f"Total de fornecedores: {len(fornecedores)}") # Exibe o número de fornecedores únicos.

    return fornecedores # Retorna o DataFrame agregado.


# ============================================================
# Clusterização
# ============================================================

def aplicar_clusterizacao(fornecedores: pd.DataFrame) -> pd.DataFrame: # Define a função que aplica o algoritmo de clusterização.
    """
    Aplica KMeans para agrupar fornecedores por comportamento.
    """
    df_cluster = fornecedores.copy() # Cria uma cópia para não modificar o DataFrame original.

    # Define a lista de features (variáveis) que serão usadas pelo modelo para encontrar os grupos.
    features = [
        "total_contratos",
        "total_orgaos",
        "total_categorias",
        "valor_total_contratado",
        "valor_medio_contrato",
        "maior_contrato",
        "score_medio_original",
        "score_medio_final",
        "total_anomalias",
        "contratos_alto_critico",
        "contratos_criticos",
        "percentual_anomalias",
        "percentual_alto_critico",
    ]

    X = df_cluster[features].fillna(0) # Seleciona as features e preenche possíveis NaNs com 0.

    # Normaliza os dados para que todas as features tenham a mesma escala (média 0, desvio padrão 1).
    # Isso é crucial para algoritmos baseados em distância como o KMeans.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Instancia o modelo KMeans.
    modelo = KMeans(
        n_clusters=4, # Define o número de clusters (grupos) a serem encontrados.
        random_state=42, # Garante que os resultados sejam reprodutíveis.
        n_init=10, # Executa o algoritmo 10 vezes com diferentes centróides iniciais para encontrar o melhor resultado.
    )

    # Treina o modelo e atribui a cada fornecedor o número do cluster ao qual ele pertence.
    df_cluster["cluster_fornecedor"] = modelo.fit_predict(X_scaled)

    # Aplica uma função para dar um nome inicial e interpretável a cada cluster.
    df_cluster["perfil_cluster"] = df_cluster["cluster_fornecedor"].apply(
        nomear_cluster
    )

    # Aplica uma função para adicionar uma descrição textual para cada perfil de cluster.
    df_cluster["descricao_cluster"] = df_cluster["perfil_cluster"].apply(
        descrever_cluster
    )

    print("Clusterização de fornecedores concluída.") # Confirma a finalização do processo.

    print("\nDistribuição por cluster:") # Exibe um resumo da distribuição.
    print(df_cluster["perfil_cluster"].value_counts()) # Conta quantos fornecedores caíram em cada perfil.

    return df_cluster # Retorna o DataFrame com os clusters atribuídos.


def nomear_cluster(cluster: int) -> str: # Define a função para nomear os clusters.
    """
    Nomeia os clusters de forma interpretável.
    Observação: a numeração do KMeans pode variar conforme os dados.
    Esta nomenclatura é inicial e será ajustada pela função de interpretação.
    """
    nomes = { # Mapeia o número do cluster (inteiro) para um nome (string).
        0: "Fornecedor recorrente",
        1: "Fornecedor de alto valor",
        2: "Fornecedor de baixo risco",
        3: "Fornecedor com atenção especial",
    }

    return nomes.get(cluster, "Perfil não classificado") # Retorna o nome ou um valor padrão.


def descrever_cluster(perfil: str) -> str: # Define a função para descrever os perfis.
    """
    Descreve cada perfil de fornecedor.
    """
    descricoes = { # Mapeia o nome do perfil para uma descrição detalhada.
        "Fornecedor recorrente": (
            "Fornecedor com quantidade relevante de contratos e presença frequente na base."
        ),
        "Fornecedor de alto valor": (
            "Fornecedor associado a contratos de maior valor financeiro."
        ),
        "Fornecedor de baixo risco": (
            "Fornecedor com comportamento mais estável e menor exposição a indicadores críticos."
        ),
        "Fornecedor com atenção especial": (
            "Fornecedor com maior presença de anomalias, contratos críticos ou indicadores de risco."
        ),
    }

    return descricoes.get(perfil, "Descrição não disponível.") # Retorna a descrição ou um valor padrão.


# ============================================================
# Interpretação automática dos clusters
# ============================================================

def reinterpretar_clusters(df_cluster: pd.DataFrame) -> pd.DataFrame: # Define a função para reinterpretar e nomear os clusters de forma dinâmica.
    """
    Reinterpreta os clusters com base nas médias reais de cada grupo.
    Isso evita depender da numeração arbitrária do KMeans.
    """
    # Agrupa os dados pelo número do cluster e calcula as médias das principais features para cada grupo.
    resumo = (
        df_cluster.groupby("cluster_fornecedor")
        .agg(
            total_fornecedores=("nome_fornecedor", "count"), # Total de fornecedores no cluster.
            media_contratos=("total_contratos", "mean"), # Média de contratos por fornecedor.
            media_valor_total=("valor_total_contratado", "mean"), # Média do valor total contratado.
            media_score_final=("score_medio_final", "mean"), # Média do score de risco.
            media_anomalias=("total_anomalias", "mean"), # Média de anomalias.
            media_alto_critico=("contratos_alto_critico", "mean"), # Média de contratos de alto risco.
        )
        .reset_index()
    )

    # Identifica o cluster com a maior média de valor total contratado.
    cluster_alto_valor = resumo.sort_values("media_valor_total", ascending=False).iloc[0][
        "cluster_fornecedor"
    ]

    # Identifica o cluster com a maior média de número de contratos.
    cluster_recorrente = resumo.sort_values("media_contratos", ascending=False).iloc[0][
        "cluster_fornecedor"
    ]

    # Identifica o cluster com os maiores indicadores de risco (score, anomalias, etc.).
    cluster_atencao = resumo.sort_values(
        ["media_score_final", "media_anomalias", "media_alto_critico"],
        ascending=False,
    ).iloc[0]["cluster_fornecedor"]

    mapa = {} # Cria um dicionário para mapear o número do cluster para o nome do perfil correto.

    # Itera sobre os clusters e atribui o nome correto com base nas características identificadas.
    for cluster in resumo["cluster_fornecedor"]:
        if cluster == cluster_atencao:
            mapa[cluster] = "Fornecedor com atenção especial"
        elif cluster == cluster_alto_valor:
            mapa[cluster] = "Fornecedor de alto valor"
        elif cluster == cluster_recorrente:
            mapa[cluster] = "Fornecedor recorrente"
        else:
            mapa[cluster] = "Fornecedor de baixo risco" # O que sobrar é considerado de baixo risco.

    # Aplica o mapeamento para atualizar os nomes dos perfis no DataFrame principal.
    df_cluster["perfil_cluster"] = df_cluster["cluster_fornecedor"].map(mapa)
    # Atualiza as descrições com base nos novos perfis.
    df_cluster["descricao_cluster"] = df_cluster["perfil_cluster"].apply(descrever_cluster)

    print("\nResumo dos clusters:") # Exibe o resumo das médias de cada cluster.
    print(resumo)

    print("\nPerfis reinterpretados:") # Exibe a nova contagem de fornecedores por perfil.
    print(df_cluster["perfil_cluster"].value_counts())

    return df_cluster # Retorna o DataFrame com os clusters nomeados corretamente.


# ============================================================
# Salvamento
# ============================================================

def salvar_resultado(df: pd.DataFrame) -> None: # Define a função para salvar o resultado final.
    """
    Salva a base de fornecedores clusterizados.
    """
    # Ordena o DataFrame pelo perfil e pelo valor total para uma melhor visualização no arquivo de saída.
    df = df.sort_values(
        ["perfil_cluster", "valor_total_contratado"],
        ascending=[True, False],
    )

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig") # Salva o DataFrame em um arquivo CSV.

    print(f"\nArquivo salvo em: {OUTPUT_PATH}") # Informa o local do arquivo salvo.

    print("\nTop 15 fornecedores por valor total contratado:") # Imprime um cabeçalho para o ranking.
    # Define as colunas mais relevantes para exibir no resumo do ranking.
    colunas = [
        "nome_fornecedor",
        "total_contratos",
        "total_orgaos",
        "valor_total_contratado",
        "score_medio_final",
        "total_anomalias",
        "contratos_alto_critico",
        "perfil_cluster",
    ]

    # Imprime as 15 primeiras linhas do DataFrame ordenado por valor, mostrando os fornecedores mais relevantes.
    print(
        df.sort_values("valor_total_contratado", ascending=False)[colunas].head(15)
    )


if __name__ == "__main__": # Bloco principal que orquestra a execução do script.
    dados = carregar_dados() # 1. Carrega os dados de licitações.
    fornecedores = preparar_base_fornecedores(dados) # 2. Agrega os dados por fornecedor.
    fornecedores_clusterizados = aplicar_clusterizacao(fornecedores) # 3. Aplica o modelo de clusterização.
    fornecedores_clusterizados = reinterpretar_clusters(fornecedores_clusterizados) # 4. Interpreta e nomeia os clusters.
    salvar_resultado(fornecedores_clusterizados) # 5. Salva o resultado final.