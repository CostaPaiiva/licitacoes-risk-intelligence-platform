# Licitações Risk Intelligence Platform

Plataforma de inteligência analítica para análise de licitações públicas, identificação de padrões suspeitos, detecção de anomalias e classificação de risco em contratos públicos.

## Objetivo

Este projeto tem como objetivo construir uma solução completa de dados aplicada ao contexto de compras públicas e licitações. A plataforma realiza extração, tratamento, carga em banco PostgreSQL, análises SQL, detecção de anomalias com Machine Learning e visualização em dashboard interativo.

## Tecnologias utilizadas

- Python
- Pandas
- PostgreSQL
- Docker
- SQLAlchemy
- Scikit-learn
- Streamlit
- Plotly
- SQL

## Principais funcionalidades

- Extração de dados de licitações
- Tratamento e padronização dos dados
- Modelagem analítica em PostgreSQL
- Consultas SQL para indicadores de negócio
- Dashboard interativo em Streamlit
- Detecção de anomalias
- Classificação de risco
- Clusterização de fornecedores

## Indicadores analisados

- Valor total contratado por órgão
- Fornecedores mais recorrentes
- Compras por categoria
- Evolução mensal dos contratos
- Contratos com valores acima da média
- Licitações com maior score de risco
- Concentração de fornecedores por órgão

## Estrutura do projeto

```txt
licitacoes-risk-intelligence-platform/
├── data/
├── database/
├── docker/
├── notebooks/
├── src/
├── sql/
├── dashboard/
├── docs/
├── docker-compose.yml
├── requirements.txt
└── README.md