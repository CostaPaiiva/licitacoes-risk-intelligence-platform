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
