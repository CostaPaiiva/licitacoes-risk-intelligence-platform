# Licitações Risk Intelligence Platform

Plataforma para análise de risco em licitações públicas, com foco em extração, transformação, carga em PostgreSQL, consultas analíticas e evolução futura para camadas de analytics, machine learning e dashboard.

## Status Atual

O projeto está em desenvolvimento. Até este ponto, a base principal já cobre:

- geração e extração de dados de amostra;
- transformação e enriquecimento da base bruta;
- carga estruturada no PostgreSQL;
- scripts SQL para análises exploratórias;
- base inicial para indicadores, modelos de ML e dashboard.

O trabalho ainda não foi finalizado. Este repositório deve seguir como uma versão em andamento, com espaço para novas regras, validações, modelos e visualizações.

## Visão Geral

A proposta do projeto é simular um fluxo completo de dados para licitações públicas:

1. extração ou geração da base;
2. limpeza e padronização dos dados;
3. persistência em banco relacional;
4. consultas analíticas e indicadores;
5. expansão para detecção de anomalias, classificação de risco e agrupamento de fornecedores;
6. visualização em dashboard.

## Estrutura do Projeto

```txt
.
├── dashboard/
├── database/
├── docs/
├── sql/
├── src/
│   ├── analytics/
│   ├── extraction/
│   ├── loading/
│   ├── ml/
│   ├── transformation/
│   └── utils/
├── docker-compose.yml
└── requirements.txt
```

## Tecnologias

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Docker
- Streamlit
- Scikit-learn

## Como Executar

### 1. Preparar o ambiente

Crie e ajuste o arquivo `.env` com as variáveis de conexão:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5433/licitacoes_db
```

Se preferir, também é possível usar:

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=licitacoes_db
```

### 2. Subir o banco

```bash
docker compose up -d
```

### 3. Gerar ou preparar a base

Execute a etapa de extração para criar a base bruta, quando necessário.

### 4. Transformar os dados

```bash
python src/transformation/transform_licitacoes.py
```

### 5. Carregar no PostgreSQL

```bash
python src/loading/load_to_postgres.py
```

## Resultados Já Implementados

- padronização de campos textuais;
- limpeza e formatação de CNPJ;
- conversão e enriquecimento de datas;
- cálculo de dias até homologação;
- recálculo de diferença e percentual entre valor estimado e contratado;
- criação de faixas de valor e faixa de variação;
- criação de indicadores booleanos de risco;
- montagem de dimensões e tabela fato para o modelo analítico.

## Próximos Passos

O projeto segue a partir daqui com:

1. validação mais robusta dos dados carregados;
2. evolução das consultas SQL analíticas;
3. consolidação dos KPIs;
4. implementação/ajuste dos modelos de machine learning;
5. construção do dashboard final;
6. refinamento da documentação técnica.

## Observação

Este README descreve o estado atual do projeto e deixa registrado que a implementação ainda vai continuar.

## Consultas analíticas SQL

O projeto possui uma camada de consultas SQL voltada para análise de licitações públicas e identificação de padrões de risco.

As consultas permitem analisar:

- valor total contratado por órgão;
- fornecedores mais recorrentes;
- compras por categoria;
- evolução mensal dos contratos;
- contratos acima da média da categoria;
- indicadores consolidados por nível de risco;
- ranking geral de risco;
- concentração entre fornecedores e órgãos públicos.

Também foi criada uma view analítica chamada:

`vw_licitacoes_analytics`

Essa view consolida a tabela fato com as dimensões, facilitando o consumo dos dados pelo dashboard e por ferramentas analíticas.

## Dashboard em Streamlit

O projeto possui um dashboard interativo desenvolvido em Streamlit para visualização dos principais indicadores de licitações públicas.

O dashboard consome os dados diretamente do PostgreSQL a partir da view analítica `vw_licitacoes_analytics`.

### Funcionalidades do dashboard

- filtros por ano, órgão, categoria e nível de risco;
- indicadores gerais de licitações;
- valor total contratado;
- quantidade de órgãos e fornecedores;
- percentual de contratos de alto risco ou críticos;
- ranking de órgãos por valor contratado;
- fornecedores mais recorrentes;
- distribuição por categoria;
- evolução mensal dos contratos;
- ranking das licitações com maior score de risco;
- análise consolidada por fornecedor.

### Executar dashboard

```bash
streamlit run dashboard/app.py


## Detecção de anomalias com Machine Learning

O projeto utiliza o algoritmo Isolation Forest para identificar licitações com comportamento atípico.

Foram consideradas variáveis como:

- valor estimado;
- valor contratado;
- diferença entre valor estimado e contratado;
- percentual de diferença;
- score de risco;
- frequência do fornecedor;
- frequência do órgão;
- média de valor por categoria;
- percentual acima da média da categoria.

O resultado da análise é salvo em:

`data/processed/licitacoes_anomaly_detection.csv`

Essa etapa permite identificar possíveis contratos fora do padrão, apoiando análises de auditoria, compliance e controle interno.

## Classificação de risco

Além da detecção de anomalias, o projeto possui uma etapa de classificação de risco das licitações.

A classificação combina regras de negócio com o resultado do modelo de anomalias, considerando fatores como:

- score de risco inicial;
- anomalia detectada pelo modelo;
- diferença percentual entre valor estimado e contratado;
- valor contratado;
- frequência do fornecedor;
- modalidade da licitação;
- status da licitação.

O resultado gera novas colunas analíticas, como:

- `ml_score_risco_final`;
- `ml_nivel_risco_final`;
- `prioridade_auditoria`;
- `motivos_risco`.

O arquivo final é salvo em:

`data/processed/licitacoes_risk_classification.csv`