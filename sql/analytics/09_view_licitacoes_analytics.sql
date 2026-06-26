-- Cria ou substitui uma VIEW para desnormalizar o modelo e facilitar a análise
CREATE OR REPLACE VIEW vw_licitacoes_analytics AS
-- Seleciona e combina colunas da tabela fato e de todas as dimensões relacionadas
SELECT
    f.id_licitacao, -- ID único da licitação (chave primária da fato)
    f.numero_processo, -- Número do processo licitatório
    o.nome_orgao, -- Nome do órgão contratante (da dim_orgao)
    o.esfera, -- Esfera do órgão (Municipal, Estadual)
    o.tipo_orgao, -- Tipo do órgão (Prefeitura, Secretaria)
    fo.nome_fornecedor, -- Nome do fornecedor contratado (da dim_fornecedor)
    fo.cnpj, -- CNPJ do fornecedor
    fo.porte_empresa, -- Porte da empresa do fornecedor
    c.categoria, -- Categoria do objeto licitado (da dim_categoria)
    c.grupo_categoria, -- Grupo da categoria
    l.cidade, -- Cidade da licitação (da dim_localidade)
    l.estado, -- Estado da licitação
    l.regiao, -- Região da licitação
    t.data, -- Data completa da publicação (da dim_tempo)
    t.ano, -- Ano da publicação
    t.mes, -- Mês da publicação
    t.nome_mes, -- Nome do mês por extenso
    t.trimestre, -- Trimestre da publicação
    f.modalidade, -- Modalidade da licitação (Pregão, Concorrência, etc.)
    f.status, -- Status atual da licitação (Homologada, Cancelada, etc.)
    f.descricao, -- Descrição do objeto da licitação
    f.valor_estimado, -- Valor estimado pela administração
    f.valor_contratado, -- Valor final contratado
    f.diferenca_valor, -- Diferença monetária entre valor contratado e estimado
    f.percentual_diferenca, -- Percentual dessa diferença
    f.score_risco, -- Pontuação de risco calculada
    f.nivel_risco, -- Nível de risco (Baixo, Médio, Alto, Crítico)
    f.is_anomalia -- Flag booleana que indica se a licitação é uma anomalia
FROM fato_licitacoes f -- Tabela principal com as métricas e chaves estrangeiras
INNER JOIN dim_orgao o -- Junta com a dimensão de órgãos para obter os detalhes do órgão
    ON f.id_orgao = o.id_orgao
INNER JOIN dim_fornecedor fo -- Junta com a dimensão de fornecedores
    ON f.id_fornecedor = fo.id_fornecedor
INNER JOIN dim_categoria c -- Junta com a dimensão de categorias
    ON f.id_categoria = c.id_categoria
INNER JOIN dim_localidade l -- Junta com a dimensão de localidades
    ON f.id_localidade = l.id_localidade
INNER JOIN dim_tempo t -- Junta com a dimensão de tempo para obter os detalhes da data
    ON f.id_tempo = t.id_tempo;