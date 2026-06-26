-- Seleciona as colunas a serem exibidas no resultado
SELECT
    fo.nome_fornecedor, -- Nome do fornecedor
    fo.cnpj,            -- CNPJ do fornecedor
    fo.porte_empresa,   -- Porte da empresa do fornecedor
    COUNT(f.id_licitacao) AS total_contratos, -- Conta o número total de contratos que o fornecedor possui
    COUNT(DISTINCT f.id_orgao) AS total_orgaos_atendidos, -- Conta o número de órgãos distintos atendidos pelo fornecedor
    SUM(f.valor_contratado) AS valor_total_vencido, -- Soma o valor total dos contratos vencidos ou concluídos pelo fornecedor
    AVG(f.valor_contratado) AS valor_medio_contrato, -- Calcula o valor médio dos contratos do fornecedor
    AVG(f.score_risco) AS score_medio_risco, -- Calcula a média do score de risco dos contratos do fornecedor
    SUM(CASE WHEN f.nivel_risco IN ('Alto', 'Crítico') THEN 1 ELSE 0 END) AS contratos_alto_risco -- Conta o número de contratos com nível de risco 'Alto' ou 'Crítico'
FROM fato_licitacoes f -- Tabela de fatos das licitações (alias 'f')
INNER JOIN dim_fornecedor fo -- Junta com a tabela de dimensão de fornecedores (alias 'fo')
    ON f.id_fornecedor = fo.id_fornecedor -- Condição de junção: o ID do fornecedor na tabela de fatos deve ser igual ao ID do fornecedor na tabela de dimensão
GROUP BY
    fo.nome_fornecedor, -- Agrupa os resultados pelo nome do fornecedor
    fo.cnpj,            -- Agrupa os resultados pelo CNPJ do fornecedor
    fo.porte_empresa    -- Agrupa os resultados pelo porte da empresa
HAVING COUNT(f.id_licitacao) >= 5 -- Filtra apenas fornecedores que possuem 5 ou mais contratos
ORDER BY 
    total_contratos DESC,       -- Ordena os resultados pelo número total de contratos em ordem decrescente
    valor_total_vencido DESC; -- Em caso de empate, ordena pelo valor total vencido em ordem decrescente