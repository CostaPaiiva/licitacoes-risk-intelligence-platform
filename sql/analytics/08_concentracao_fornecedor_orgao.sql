-- Seleciona as colunas a serem exibidas no resultado
SELECT
    o.nome_orgao, -- Nome do órgão contratante
    fo.nome_fornecedor, -- Nome do fornecedor contratado
    COUNT(f.id_licitacao) AS total_contratos, -- Conta o número total de contratos entre o órgão e o fornecedor
    SUM(f.valor_contratado) AS valor_total_contratado, -- Soma o valor total contratado entre o par
    AVG(f.valor_contratado) AS valor_medio_contrato, -- Calcula o valor médio dos contratos entre o par
    AVG(f.score_risco) AS score_medio_risco, -- Calcula a média do score de risco para os contratos do par
    SUM(CASE WHEN f.nivel_risco IN ('Alto', 'Crítico') THEN 1 ELSE 0 END) AS contratos_alto_risco -- Conta quantos contratos de risco 'Alto' ou 'Crítico' existem entre o par
FROM fato_licitacoes f -- Tabela de fatos das licitações (alias 'f')
INNER JOIN dim_orgao o -- Junta com a dimensão de órgãos para obter o nome do órgão
    ON f.id_orgao = o.id_orgao
INNER JOIN dim_fornecedor fo -- Junta com a dimensão de fornecedores para obter o nome do fornecedor
    ON f.id_fornecedor = fo.id_fornecedor
GROUP BY
    o.nome_orgao, -- Agrupa os resultados pelo nome do órgão
    fo.nome_fornecedor -- Agrupa os resultados pelo nome do fornecedor
HAVING COUNT(f.id_licitacao) >= 3 -- Filtra e exibe apenas os pares (órgão, fornecedor) que contrataram 3 ou mais vezes
ORDER BY
    total_contratos DESC, -- Ordena pelo maior número de contratos em ordem decrescente
    valor_total_contratado DESC; -- Em caso de empate, ordena pelo maior valor total contratado