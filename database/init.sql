-- Criação do esquema público padrão caso não exista
CREATE SCHEMA IF NOT EXISTS public;

-- Tabela de Dimensão: Órgão Público
-- Armazena os dados dos órgãos públicos compradores/licitantes
CREATE TABLE IF NOT EXISTS dim_orgao (
    id_orgao SERIAL PRIMARY KEY,                     -- Chave primária autoincrementada
    nome_orgao VARCHAR(255) NOT NULL,               -- Nome oficial do órgão público
    esfera VARCHAR(50),                             -- Esfera administrativa (Federal, Estadual, Municipal)
    tipo_orgao VARCHAR(100)                         -- Tipo de órgão (Ministério, Secretaria, Autarquia, etc.)
);

-- Tabela de Dimensão: Fornecedor
-- Armazena informações dos licitantes, fornecedores e prestadores de serviço
CREATE TABLE IF NOT EXISTS dim_fornecedor (
    id_fornecedor SERIAL PRIMARY KEY,                -- Chave primária autoincrementada
    nome_fornecedor VARCHAR(255) NOT NULL,           -- Razão social ou nome fantasia do fornecedor
    cnpj VARCHAR(20),                               -- Cadastro Nacional da Pessoa Jurídica (CNPJ)
    porte_empresa VARCHAR(50)                       -- Porte da empresa (ME, EPP, Grande Porte, etc.)
);

-- Tabela de Dimensão: Categoria de Compra
-- Classifica os itens adquiridos nas licitações em categorias e grupos lógicos
CREATE TABLE IF NOT EXISTS dim_categoria (
    id_categoria SERIAL PRIMARY KEY,                -- Chave primária autoincrementada
    categoria VARCHAR(150) NOT NULL,                 -- Nome descritivo da categoria (ex: Tecnologia da Informação)
    grupo_categoria VARCHAR(150)                    -- Agrupador macro (ex: Bens de Consumo, Serviços de Engenharia)
);

-- Tabela de Dimensão: Localidade
-- Armazena dados geográficos do local onde ocorre a licitação ou entrega do objeto
CREATE TABLE IF NOT EXISTS dim_localidade (
    id_localidade SERIAL PRIMARY KEY,               -- Chave primária autoincrementada
    cidade VARCHAR(150),                            -- Nome do município
    estado VARCHAR(2),                              -- Sigla da Unidade Federativa (UF)
    regiao VARCHAR(50)                              -- Região geográfica do país (Norte, Nordeste, Sudeste, etc.)
);

-- Tabela de Dimensão: Tempo
-- Permite análises temporárias granulares por dia, mês, ano e trimestres
CREATE TABLE IF NOT EXISTS dim_tempo (
    id_tempo SERIAL PRIMARY KEY,                    -- Chave primária autoincrementada
    data DATE NOT NULL,                             -- Data exata da licitação/contratação
    ano INTEGER,                                    -- Ano com 4 dígitos (ex: 2026)
    mes INTEGER,                                    -- Número do mês (1 a 12)
    nome_mes VARCHAR(30),                           -- Nome do mês por extenso (ex: Junho)
    trimestre INTEGER                               -- Número do trimestre (1 a 4)
);

-- Tabela de Fatos: Licitações
-- Tabela central do modelo estrela (Star Schema) que consolida as métricas, chaves de dimensões e indicadores de risco
CREATE TABLE IF NOT EXISTS fato_licitacoes (
    id_licitacao SERIAL PRIMARY KEY,                           -- Chave primária autoincrementada
    numero_processo VARCHAR(100),                              -- Número de controle do processo de licitação
    id_orgao INTEGER REFERENCES dim_orgao(id_orgao),           -- Chave estrangeira para a dimensão de órgãos
    id_fornecedor INTEGER REFERENCES dim_fornecedor(id_fornecedor), -- Chave estrangeira para a dimensão de fornecedores
    id_categoria INTEGER REFERENCES dim_categoria(id_categoria), -- Chave estrangeira para a dimensão de categorias
    id_localidade INTEGER REFERENCES dim_localidade(id_localidade), -- Chave estrangeira para a dimensão de localidade
    id_tempo INTEGER REFERENCES dim_tempo(id_tempo),           -- Chave estrangeira para a dimensão de tempo
    modalidade VARCHAR(100),                                   -- Modalidade da licitação (Pregão Eletrônico, Concorrência, etc.)
    status VARCHAR(100),                                       -- Status atual do processo (Homologado, Cancelado, Em andamento)
    descricao TEXT,                                            -- Descrição detalhada do objeto da licitação
    valor_estimado NUMERIC(15,2),                              -- Valor máximo estimado/previsto pelo órgão público
    valor_contratado NUMERIC(15,2),                            -- Valor final fechado com o fornecedor vencedor
    diferenca_valor NUMERIC(15,2),                             -- Diferença entre o valor estimado e o contratado
    percentual_diferenca NUMERIC(10,2),                        -- Desconto ou sobrepreço percentual obtido
    score_risco NUMERIC(10,2),                                 -- Score de probabilidade de risco/fraude calculado pelos modelos de ML
    nivel_risco VARCHAR(50),                                   -- Classificação qualitativa do risco (Baixo, Médio, Alto)
    is_anomalia BOOLEAN DEFAULT FALSE                          -- Flag indicando se a licitação foi classificada como anômala pelo modelo
);