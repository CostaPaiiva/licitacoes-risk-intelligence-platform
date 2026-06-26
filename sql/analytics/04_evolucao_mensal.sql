-- Seleciona as colunas a serem exibidas no resultado
SELECT
    t.ano, -- Ano da data de publicação da licitação
    t.mes, -- Mês da data de publicação (numérico)
    t.nome_mes, -- Nome do mês por extenso (e.g., Janeiro, Fevereiro)
    COUNT(f.id_licitacao) AS total_licitacoes, -- Conta o número total de licitações para cada mês/ano
    SUM(f.valor_contratado) AS valor_total_contratado, -- Soma o valor total contratado no período
    AVG(f.valor_contratado) AS valor_medio_contratado, -- Calcula o valor médio contratado por licitação no período
    SUM(CASE WHEN f.nivel_risco IN ('Alto', 'Crítico') THEN 1 ELSE 0 END) AS total_risco_alto_critico, -- Conta o número de licitações com risco 'Alto' ou 'Crítico'
    AVG(f.score_risco) AS score_medio_risco -- Calcula a média do score de risco para o período
FROM fato_licitacoes f -- Tabela de fatos das licitações (alias 'f')
INNER JOIN dim_tempo t -- Junta com a tabela de dimensão de tempo (alias 't')
    ON f.id_tempo = t.id_tempo -- Condição de junção: o ID de tempo na tabela de fatos deve ser igual ao ID na tabela de dimensão
GROUP BY
    t.ano, -- Agrupa os resultados pelo ano
    t.mes, -- Agrupa os resultados pelo mês
    t.nome_mes -- Agrupa os resultados pelo nome do mês
ORDER BY
    t.ano, -- Ordena os resultados pelo ano em ordem crescente
    t.mes; -- Ordena os resultados pelo mês em ordem crescente