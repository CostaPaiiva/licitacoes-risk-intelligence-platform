-- Define uma Common Table Expression (CTE) para calcular a média de valor por categoria
WITH media_categoria AS (
    SELECT
        id_categoria, -- ID da categoria
        AVG(valor_contratado) AS media_valor_categoria -- Calcula o valor médio contratado para cada categoria
    FROM fato_licitacoes -- Usa a tabela de fatos como base
    GROUP BY id_categoria -- Agrupa os resultados por categoria para o cálculo da média
)

-- Seleciona as colunas a serem exibidas no resultado final
SELECT
    f.numero_processo, -- Número do processo da licitação
    o.nome_orgao, -- Nome do órgão contratante
    fo.nome_fornecedor, -- Nome do fornecedor contratado
    c.categoria, -- Categoria do objeto licitado
    f.modalidade, -- Modalidade da licitação
    f.status, -- Status atual da licitação
    f.valor_estimado, -- Valor estimado pela administração pública
    f.valor_contratado, -- Valor final contratado com o fornecedor
    mc.media_valor_categoria, -- Média de valor para a categoria (calculada na CTE)
    ROUND( -- Arredonda o resultado para 2 casas decimais
        ((f.valor_contratado - mc.media_valor_categoria) / mc.media_valor_categoria) * 100, -- Calcula o percentual que o valor contratado está acima da média da categoria
        2
    ) AS percentual_acima_media_categoria,
    f.score_risco, -- Score de risco da licitação
    f.nivel_risco -- Nível de risco (Baixo, Médio, Alto, Crítico)
FROM fato_licitacoes f -- Tabela de fatos das licitações (alias 'f')
INNER JOIN media_categoria mc -- Junta com a CTE que calculou a média por categoria
    ON f.id_categoria = mc.id_categoria -- Condição de junção pelo ID da categoria
INNER JOIN dim_orgao o -- Junta com a dimensão de órgãos para obter o nome do órgão
    ON f.id_orgao = o.id_orgao
INNER JOIN dim_fornecedor fo -- Junta com a dimensão de fornecedores para obter o nome do fornecedor
    ON f.id_fornecedor = fo.id_fornecedor
INNER JOIN dim_categoria c -- Junta com a dimensão de categorias para obter o nome da categoria
    ON f.id_categoria = c.id_categoria
WHERE f.valor_contratado > mc.media_valor_categoria * 1.5 -- Filtra apenas licitações cujo valor contratado é 50% maior que a média da categoria
ORDER BY percentual_acima_media_categoria DESC; -- Ordena os resultados pelo maior percentual de desvio em ordem decrescente