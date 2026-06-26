-- Seleciona as colunas a serem exibidas no resultado
SELECT
    c.grupo_categoria, -- Agrupador macro da categoria (e.g., Bens de Consumo, Serviços)
    c.categoria, -- Nome da categoria específica da compra (e.g., Material de escritório)
    COUNT(f.id_licitacao) AS total_licitacoes, -- Conta o número total de licitações para cada categoria
    SUM(f.valor_contratado) AS valor_total_contratado, -- Soma o valor total contratado para a categoria
    AVG(f.valor_contratado) AS valor_medio_contratado, -- Calcula o valor médio contratado por licitação na categoria
    MIN(f.valor_contratado) AS menor_valor, -- Encontra o menor valor contratado na categoria
    MAX(f.valor_contratado) AS maior_valor, -- Encontra o maior valor contratado na categoria
    AVG(f.score_risco) AS score_medio_risco -- Calcula a média do score de risco para a categoria
FROM fato_licitacoes f -- Tabela de fatos das licitações (alias 'f')
INNER JOIN dim_categoria c -- Junta com a tabela de dimensão de categorias (alias 'c')
    ON f.id_categoria = c.id_categoria -- Condição de junção: o ID da categoria na tabela de fatos deve ser igual ao ID na tabela de dimensão
GROUP BY
    c.grupo_categoria, -- Agrupa os resultados pelo grupo da categoria
    c.categoria -- Agrupa os resultados pelo nome da categoria
ORDER BY valor_total_contratado DESC; -- Ordena os resultados pelo valor total contratado em ordem decrescente