# Consultas Analíticas SQL

Esta pasta contém as consultas SQL utilizadas para análise das licitações públicas carregadas no PostgreSQL.

## Consultas disponíveis

| Arquivo | Descrição |
|---|---|
| 01_total_por_orgao.sql | Analisa o valor total contratado por órgão público |
| 02_fornecedores_recorrentes.sql | Identifica fornecedores com maior recorrência em contratos |
| 03_compras_por_categoria.sql | Analisa compras públicas por categoria |
| 04_evolucao_mensal.sql | Analisa a evolução mensal das licitações |
| 05_contratos_acima_media.sql | Identifica contratos com valores acima da média da categoria |
| 06_indicadores_risco.sql | Consolida indicadores por nível de risco |
| 07_ranking_geral_risco.sql | Lista as licitações com maior score de risco |
| 08_concentracao_fornecedor_orgao.sql | Analisa concentração entre fornecedor e órgão público |
| 09_view_licitacoes_analytics.sql | Cria uma view analítica para uso em dashboards |

## Objetivo

As consultas foram criadas para apoiar análises de auditoria, compliance, controle interno e inteligência em compras públicas.

## Principais indicadores

- Valor total contratado
- Quantidade de licitações
- Valor médio por contrato
- Fornecedores recorrentes
- Contratos acima da média
- Score médio de risco
- Distribuição por nível de risco
- Concentração de fornecedores por órgão