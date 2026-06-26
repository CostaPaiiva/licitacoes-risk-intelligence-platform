-- Seleciona as colunas a serem exibidas no resultado, unindo informações da fato e das dimensões
SELECT
    f.numero_processo, -- Número do processo da licitação
    o.nome_orgao, -- Nome do órgão contratante
    l.cidade, -- Cidade da licitação
    l.estado, -- Estado da licitação
    fo.nome_fornecedor, -- Nome do fornecedor contratado
    fo.cnpj, -- CNPJ do fornecedor
    c.categoria, -- Categoria do objeto licitado
    c.grupo_categoria, -- Grupo da categoria
    t.data, -- Data de publicação da licitação
    f.modalidade, -- Modalidade da licitação
    f.status, -- Status atual da licitação
    f.valor_estimado, -- Valor estimado pela administração
    f.valor_contratado, -- Valor final contratado
    f.diferenca_valor, -- Diferença entre valor contratado e estimado
    f.percentual_diferenca, -- Percentual da diferença
    f.score_risco, -- Score de risco calculado
    f.nivel_risco, -- Nível de risco (Baixo, Médio, Alto, Crítico)
    f.is_anomalia -- Flag que indica se o modelo classificou como anomalia
FROM fato_licitacoes f -- Tabela de fatos das licitações (alias 'f')
INNER JOIN dim_orgao o -- Junta com a dimensão de órgãos para obter o nome do órgão
    ON f.id_orgao = o.id_orgao
INNER JOIN dim_fornecedor fo -- Junta com a dimensão de fornecedores para obter os dados do fornecedor
    ON f.id_fornecedor = fo.id_fornecedor
INNER JOIN dim_categoria c -- Junta com a dimensão de categorias para obter a descrição da categoria
    ON f.id_categoria = c.id_categoria
INNER JOIN dim_localidade l -- Junta com a dimensão de localidades para obter cidade e estado
    ON f.id_localidade = l.id_localidade
INNER JOIN dim_tempo t -- Junta com a dimensão de tempo para obter a data completa
    ON f.id_tempo = t.id_tempo
ORDER BY -- Ordena os resultados para criar o ranking
    f.score_risco DESC, -- Prioriza pelo maior score de risco
    f.valor_contratado DESC -- Em caso de empate no risco, prioriza pelo maior valor contratado
LIMIT 100; -- Limita o resultado às 100 licitações mais críticas segundo os critérios de ordenação