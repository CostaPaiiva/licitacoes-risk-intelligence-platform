-- Seleciona as colunas a serem exibidas no resultado
SELECT
    o.nome_orgao, -- Nome do órgão
    o.esfera,     -- Esfera administrativa do órgão (Federal, Estadual, Municipal)
    o.tipo_orgao, -- Tipo do órgão (e.g., Executivo, Legislativo)
    COUNT(f.id_licitacao) AS total_licitacoes, -- Conta o número total de licitações para cada órgão
    SUM(f.valor_contratado) AS valor_total_contratado, -- Soma o valor total contratado nas licitações do órgão
    AVG(f.valor_contratado) AS valor_medio_contratado, -- Calcula o valor médio contratado por licitação do órgão
    SUM(CASE WHEN f.nivel_risco IN ('Alto', 'Crítico') THEN 1 ELSE 0 END) AS total_risco_alto_critico -- Soma o número de licitações com nível de risco 'Alto' ou 'Crítico'
FROM fato_licitacoes f -- Tabela de fatos das licitações (alias 'f')
INNER JOIN dim_orgao o -- Junta com a tabela de dimensão de órgãos (alias 'o')
    ON f.id_orgao = o.id_orgao -- Condição de junção: o ID do órgão na tabela de fatos deve ser igual ao ID do órgão na tabela de dimensão
GROUP BY
    o.nome_orgao, -- Agrupa os resultados pelo nome do órgão
    o.esfera,     -- Agrupa os resultados pela esfera
    o.tipo_orgao  -- Agrupa os resultados pelo tipo de órgão
ORDER BY valor_total_contratado DESC; -- Ordena os resultados pelo valor total contratado em ordem decrescente