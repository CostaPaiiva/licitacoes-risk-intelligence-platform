-- Seleciona as colunas a serem exibidas no resultado
SELECT
    f.nivel_risco, -- Nível de risco da licitação (Baixo, Médio, Alto, Crítico)
    COUNT(f.id_licitacao) AS total_licitacoes, -- Conta o número total de licitações para cada nível de risco
    SUM(f.valor_contratado) AS valor_total_contratado, -- Soma o valor total contratado para cada nível de risco
    AVG(f.valor_contratado) AS valor_medio_contratado, -- Calcula o valor médio contratado por licitação em cada nível
    AVG(f.score_risco) AS score_medio_risco, -- Calcula a média do score de risco para cada nível
    MIN(f.score_risco) AS menor_score, -- Encontra o menor score de risco dentro do nível
    MAX(f.score_risco) AS maior_score, -- Encontra o maior score de risco dentro do nível
    ROUND( -- Arredonda o resultado para 2 casas decimais
        COUNT(f.id_licitacao) * 100.0 / SUM(COUNT(f.id_licitacao)) OVER (), -- Calcula o percentual que cada nível representa do total de licitações
        2
    ) AS percentual_total
FROM fato_licitacoes f -- Tabela de fatos das licitações (alias 'f')
GROUP BY f.nivel_risco -- Agrupa os resultados pelo nível de risco
ORDER BY -- Ordena os resultados de forma personalizada, do maior para o menor risco
    CASE f.nivel_risco -- Define uma ordem de classificação específica para o nível de risco
        WHEN 'Crítico' THEN 1
        WHEN 'Alto' THEN 2
        WHEN 'Médio' THEN 3
        WHEN 'Baixo' THEN 4
        ELSE 5 -- Garante que outros valores (se existirem) fiquem no final
    END;