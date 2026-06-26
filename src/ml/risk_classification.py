import os # Importa o módulo 'os' para interagir com o sistema operacional, como manipulação de caminhos de arquivo.

import pandas as pd # Importa a biblioteca pandas, essencial para manipulação e análise de dados, e a apelida de 'pd'.


# ============================================================
# Configurações de caminhos
# ============================================================

# Define a variável BASE_DIR para armazenar o caminho absoluto do diretório raiz do projeto.
# os.path.abspath(__file__) -> Obtém o caminho absoluto do script atual.
# os.path.dirname(...) -> Obtém o diretório pai do caminho fornecido. Isso é feito três vezes para subir da 'src/ml' para a raiz.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define o caminho do arquivo de entrada, que é o resultado da etapa de detecção de anomalias
INPUT_PATH = os.path.join(
    BASE_DIR, # Caminho raiz do projeto.
    "data", # Pasta de dados.
    "processed", # Subpasta de dados processados.
    "licitacoes_anomaly_detection.csv", # Nome do arquivo de entrada.
)

# Define o caminho do arquivo de saída, que conterá a classificação de risco final
OUTPUT_PATH = os.path.join(
    BASE_DIR, # Caminho raiz do projeto.
    "data", # Pasta de dados.
    "processed", # Subpasta de dados processados.
    "licitacoes_risk_classification.csv", # Nome do arquivo de saída.
)


# ============================================================
# Carregamento dos dados
# ============================================================

def carregar_dados() -> pd.DataFrame: # Define a função 'carregar_dados' que não recebe argumentos e retorna um DataFrame do pandas.
    """
    Carrega o arquivo gerado pela etapa de detecção de anomalias.
    """
    # Verifica se o arquivo de entrada existe antes de prosseguir
    if not os.path.exists(INPUT_PATH): # Verifica se o arquivo de entrada especificado em INPUT_PATH realmente existe no sistema de arquivos.
        # Se o arquivo não for encontrado, levanta uma exceção 'FileNotFoundError' com uma mensagem informativa.
        raise FileNotFoundError(
            f"Arquivo não encontrado: {INPUT_PATH}. " # Mensagem de erro indicando o caminho do arquivo ausente.
            "Execute primeiro o script src/ml/anomaly_detection.py" # Instrução para o usuário sobre como gerar o arquivo necessário.
        )

    # Carrega o arquivo CSV para um DataFrame do pandas
    df = pd.read_csv(INPUT_PATH) # Lê o arquivo CSV do caminho de entrada (INPUT_PATH) e o carrega em um DataFrame do pandas.

    # Imprime mensagens de status para o usuário
    print("Dados de anomalias carregados com sucesso.") # Imprime uma mensagem no console para confirmar que os dados foram carregados com sucesso.
    print(f"Total de registros: {len(df)}") # Imprime o número total de registros (linhas) no DataFrame carregado.

    return df # Retorna o DataFrame carregado para ser usado em outras partes do script.


# ============================================================
# Regras de classificação de risco
# ============================================================

def calcular_score_risco_final(row) -> float: # Define a função 'calcular_score_risco_final' que recebe uma linha (row) de um DataFrame e retorna um float.
    """
    Calcula um score de risco final combinando regras de negócio
    com o resultado do modelo de anomalias.
    """
    # Inicializa o score em 0 para cada licitação
    score = 0 # Inicia a pontuação de risco com valor zero.

    # 1. Score original da base
    # Adiciona uma parcela do score de risco original, com um peso de 35%
    score += float(row.get("score_risco", 0)) * 0.35 # Pondera o score de risco original (baseado em regras) em 35% e o adiciona ao score final.

    # 2. Anomalia detectada pelo modelo
    # Adiciona uma pontuação fixa se o modelo de ML marcou a licitação como anomalia
    if bool(row.get("ml_is_anomalia", False)): # Verifica se a licitação foi marcada como uma anomalia pelo modelo de Machine Learning.
        score += 25 # Adiciona 25 pontos ao score se for uma anomalia.

    # 3. Diferença percentual entre valor estimado e contratado
    # Adiciona pontos progressivamente conforme o valor contratado excede o estimado
    percentual_diferenca = float(row.get("percentual_diferenca", 0)) # Obtém a diferença percentual entre o valor contratado e o estimado.

    if percentual_diferenca > 15: # Se a diferença for maior que 15%,
        score += 10 # adiciona 10 pontos.

    if percentual_diferenca > 40: # Se a diferença for maior que 40%,
        score += 15 # adiciona mais 15 pontos.

    if percentual_diferenca > 80: # Se a diferença for maior que 80%,
        score += 10 # adiciona mais 10 pontos.

    # 4. Valor contratado alto
    # Adiciona pontos para contratos de valores muito elevados
    valor_contratado = float(row.get("valor_contratado", 0)) # Obtém o valor contratado da licitação.

    if valor_contratado > 1_000_000: # Se o valor for maior que 1 milhão,
        score += 5 # adiciona 5 pontos.

    if valor_contratado > 5_000_000: # Se o valor for maior que 5 milhões,
        score += 10 # adiciona mais 10 pontos.

    # 5. Fornecedor recorrente
    # Adiciona pontos se o fornecedor tem um alto número de contratos, indicando concentração
    frequencia_fornecedor = int(row.get("frequencia_fornecedor", 0)) # Obtém a frequência (número de contratos) do fornecedor.

    if frequencia_fornecedor >= 10: # Se o fornecedor tiver 10 ou mais contratos,
        score += 5 # adiciona 5 pontos.

    if frequencia_fornecedor >= 20: # Se o fornecedor tiver 20 ou mais contratos,
        score += 10 # adiciona mais 10 pontos.

    # 6. Modalidades que exigem maior atenção analítica
    # Adiciona pontos para modalidades menos competitivas, como dispensa ou inexigibilidade
    modalidade = str(row.get("modalidade", "")) # Obtém a modalidade da licitação.

    if modalidade in ["Dispensa de Licitação", "Inexigibilidade"]: # Se a modalidade for 'Dispensa' ou 'Inexigibilidade',
        score += 15 # adiciona 15 pontos.

    # 7. Status problemático
    # Adiciona pontos se a licitação teve um desfecho problemático
    status = str(row.get("status", "")) # Obtém o status da licitação.

    if status in ["Cancelada", "Revogada", "Suspensa"]: # Se o status indicar um problema,
        score += 10 # adiciona 10 pontos.

    # Retorna o score final, garantindo que não ultrapasse 100
    return round(min(score, 100), 2) # Garante que o score não passe de 100, arredonda para 2 casas decimais e o retorna.


def classificar_nivel_risco_final(score: float) -> str: # Define a função 'classificar_nivel_risco_final' que recebe um score (float) e retorna uma string.
    """
    Classifica o nível de risco final.
    """
    # Converte o score numérico em uma categoria de risco textual
    if score < 25: # Se o score for menor que 25,
        return "Baixo" # o nível de risco é 'Baixo'.
    elif score < 50: # Se o score for menor que 50,
        return "Médio" # o nível de risco é 'Médio'.
    elif score < 75: # Se o score for menor que 75,
        return "Alto" # o nível de risco é 'Alto'.
    else: # Caso contrário (score >= 75),
        return "Crítico" # o nível de risco é 'Crítico'.


def classificar_prioridade_auditoria(row) -> str: # Define a função 'classificar_prioridade_auditoria' que recebe uma linha de DataFrame e retorna uma string.
    """
    Cria uma prioridade de auditoria.
    Essa coluna é útil para dashboards e relatórios executivos.
    """
    # Extrai as variáveis necessárias da linha do DataFrame
    risco = row["ml_nivel_risco_final"] # Obtém o nível de risco final da linha.
    is_anomalia = bool(row["ml_is_anomalia"]) # Verifica se a linha é marcada como anomalia.
    valor = float(row["valor_contratado"]) # Obtém o valor contratado da linha.

    # Define a prioridade máxima para casos críticos, anômalos e de alto valor
    if risco == "Crítico" and is_anomalia and valor > 1_000_000: # Se o risco for 'Crítico', for uma anomalia e o valor for alto,
        return "Prioridade Máxima" # a prioridade é 'Máxima'.

    # Define prioridades decrescentes com base na combinação de risco e anomalia
    if risco == "Crítico": # Se o risco for 'Crítico',
        return "Prioridade Alta" # a prioridade é 'Alta'.

    if risco == "Alto" and is_anomalia: # Se o risco for 'Alto' e for uma anomalia,
        return "Prioridade Alta" # a prioridade também é 'Alta'.

    if risco == "Alto": # Se o risco for 'Alto' (mas não necessariamente uma anomalia),
        return "Prioridade Média" # a prioridade é 'Média'.

    if risco == "Médio": # Se o risco for 'Médio',
        return "Prioridade Baixa" # a prioridade é 'Baixa'.

    # Define um nível base para licitações de baixo risco
    return "Monitoramento" # Para todos os outros casos (risco 'Baixo'), a recomendação é 'Monitoramento'.


def gerar_motivos_risco(row) -> str: # Define a função 'gerar_motivos_risco' que recebe uma linha de DataFrame e retorna uma string.
    """
    Gera uma explicação textual dos motivos de risco.
    Isso deixa o projeto mais interpretável e profissional.
    """
    # Inicializa uma lista vazia para armazenar os motivos
    motivos = [] # Cria uma lista vazia para guardar as descrições dos motivos de risco.

    # Verifica cada condição de risco e adiciona uma descrição textual se for verdadeira
    if bool(row.get("ml_is_anomalia", False)): # Se for uma anomalia detectada pelo ML,
        motivos.append("Anomalia detectada pelo modelo") # adiciona o motivo correspondente.

    if float(row.get("percentual_diferenca", 0)) > 40: # Se a diferença percentual for muito alta,
        motivos.append("Valor contratado muito acima do estimado") # adiciona o motivo.
    elif float(row.get("percentual_diferenca", 0)) > 15: # Se a diferença for moderadamente alta,
        motivos.append("Valor contratado acima do estimado") # adiciona outro motivo.

    if float(row.get("valor_contratado", 0)) > 5_000_000: # Se o valor do contrato for muito elevado,
        motivos.append("Contrato de valor muito elevado") # adiciona o motivo.
    elif float(row.get("valor_contratado", 0)) > 1_000_000: # Se o valor for elevado,
        motivos.append("Contrato de valor elevado") # adiciona outro motivo.

    if int(row.get("frequencia_fornecedor", 0)) >= 20: # Se o fornecedor for muito recorrente,
        motivos.append("Fornecedor altamente recorrente") # adiciona o motivo.
    elif int(row.get("frequencia_fornecedor", 0)) >= 10: # Se o fornecedor for recorrente,
        motivos.append("Fornecedor recorrente") # adiciona outro motivo.

    if str(row.get("modalidade", "")) in ["Dispensa de Licitação", "Inexigibilidade"]: # Se a modalidade for de atenção,
        motivos.append("Modalidade exige maior atenção") # adiciona o motivo.

    if str(row.get("status", "")) in ["Cancelada", "Revogada", "Suspensa"]: # Se o status for problemático,
        motivos.append("Status sensível da licitação") # adiciona o motivo.

    # Se nenhum motivo de risco foi encontrado, adiciona uma mensagem padrão
    if not motivos: # Se a lista de motivos estiver vazia,
        motivos.append("Sem fator crítico identificado") # adiciona uma mensagem padrão.

    # Junta todos os motivos em uma única string, separados por "; "
    return "; ".join(motivos) # Concatena todos os motivos em uma única string, separados por "; ".


# ============================================================
# Pipeline de classificação
# ============================================================

def classificar_risco(df: pd.DataFrame) -> pd.DataFrame: # Define a função 'classificar_risco' que recebe um DataFrame e retorna um DataFrame modificado.
    """
    Aplica classificação de risco final nas licitações.
    """
    # Cria uma cópia do DataFrame para evitar modificar o original
    df_classificado = df.copy() # Cria uma cópia do DataFrame de entrada para evitar alterações no original (efeitos colaterais).

    # Aplica a função para calcular o score final em cada linha do DataFrame
    df_classificado["ml_score_risco_final"] = df_classificado.apply( # Cria uma nova coluna 'ml_score_risco_final'.
        calcular_score_risco_final, # Aplica a função 'calcular_score_risco_final'
        axis=1, # para cada linha (axis=1) do DataFrame.
    )

    # Aplica a função para classificar o nível de risco com base no score final
    df_classificado["ml_nivel_risco_final"] = df_classificado[ # Cria a coluna 'ml_nivel_risco_final'.
        "ml_score_risco_final" # Pega a coluna com o score final
    ].apply(classificar_nivel_risco_final) # e aplica a função 'classificar_nivel_risco_final' para cada valor.

    # Aplica a função para definir a prioridade de auditoria
    df_classificado["prioridade_auditoria"] = df_classificado.apply( # Cria a coluna 'prioridade_auditoria'.
        classificar_prioridade_auditoria, # Aplica a função 'classificar_prioridade_auditoria'
        axis=1, # para cada linha do DataFrame.
    )

    # Aplica a função para gerar os motivos textuais do risco
    df_classificado["motivos_risco"] = df_classificado.apply( # Cria a coluna 'motivos_risco'.
        gerar_motivos_risco, # Aplica a função 'gerar_motivos_risco'
        axis=1, # para cada linha do DataFrame.
    )

    # Imprime resumos no console para acompanhamento
    print("Classificação de risco concluída.") # Informa ao usuário que o processo terminou.

    print("\nDistribuição por risco final:") # Imprime um cabeçalho para o resumo a seguir.
    print(df_classificado["ml_nivel_risco_final"].value_counts()) # Mostra a contagem de licitações para cada nível de risco final.

    print("\nDistribuição por prioridade de auditoria:") # Imprime outro cabeçalho.
    print(df_classificado["prioridade_auditoria"].value_counts()) # Mostra a contagem de licitações para cada prioridade de auditoria.

    return df_classificado # Retorna o DataFrame final com as novas colunas de classificação.


def salvar_resultado(df: pd.DataFrame) -> None: # Define a função 'salvar_resultado' que recebe um DataFrame e não retorna nada (None).
    """
    Salva o resultado da classificação.
    """
    # Salva o DataFrame final em um novo arquivo CSV
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig") # Exporta o DataFrame para um arquivo CSV no caminho definido por OUTPUT_PATH.

    print(f"\nArquivo salvo em: {OUTPUT_PATH}") # Informa ao usuário onde o arquivo foi salvo.

    # Imprime um ranking das 10 licitações mais arriscadas para uma análise rápida
    print("\nTop 10 licitações com maior risco final:") # Imprime um cabeçalho para o ranking.
    # Define as colunas mais relevantes para exibir no resumo
    colunas = [ # Define uma lista com os nomes das colunas de interesse para o resumo.
        "numero_processo", # Número do processo da licitação.
        "nome_orgao", # Nome do órgão público.
        "nome_fornecedor", # Nome do fornecedor contratado.
        "categoria", # Categoria do objeto licitado.
        "valor_contratado", # Valor final do contrato.
        "percentual_diferenca", # Diferença percentual em relação ao valor estimado.
        "ml_is_anomalia", # Flag que indica se é uma anomalia.
        "ml_score_risco_final", # Score de risco final calculado.
        "ml_nivel_risco_final", # Nível de risco final (categórico).
        "prioridade_auditoria", # Prioridade de auditoria sugerida.
        "motivos_risco", # Descrição textual dos motivos do risco.
    ]

    # Ordena por score e valor, e exibe as 10 primeiras
    print( # Imprime o resultado da operação a seguir.
        df.sort_values( # Ordena o DataFrame.
            ["ml_score_risco_final", "valor_contratado"], # Usa o score final e o valor contratado como critérios de ordenação.
            ascending=False, # Ordena em ordem decrescente (do maior para o menor).
        )[colunas].head(10) # Seleciona as colunas de interesse e exibe apenas as 10 primeiras linhas (o top 10).
    )


if __name__ == "__main__": # Bloco de código que só é executado quando o script é rodado diretamente (não quando é importado).
    # Ponto de entrada do script
    # Carrega os dados da etapa anterior
    dados = carregar_dados() # Chama a função para carregar os dados do arquivo de anomalias.
    # Executa a classificação de risco
    resultado = classificar_risco(dados) # Chama a função principal para executar a classificação de risco.
    # Salva o resultado final
    salvar_resultado(resultado) # Chama a função para salvar o DataFrame resultante em um arquivo CSV.