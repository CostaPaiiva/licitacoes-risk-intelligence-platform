# SQL Analytics

Este diretório concentra as consultas analíticas do projeto para apoio a auditoria, compliance e exploração executiva dos dados de licitações.

As queries foram escritas para trabalhar sobre o modelo dimensional em PostgreSQL e sobre a view consolidada `vw_licitacoes_analytics`, usada pelo dashboard em `dashboard/app.py`.

## O que existe aqui

| Arquivo | Finalidade |
| --- | --- |
| `01_total_por_orgao.sql` | Consolida o valor total contratado por órgão público |
| `02_fornecedores_recorrentes.sql` | Identifica fornecedores com maior recorrência |
| `03_compras_por_categoria.sql` | Analisa compras por categoria de contratação |
| `04_evolucao_mensal.sql` | Mostra a evolução mensal das licitações |
| `05_contratos_acima_media.sql` | Localiza contratos acima da média da categoria |
| `06_indicadores_risco.sql` | Resume indicadores por nível de risco |
| `07_ranking_geral_risco.sql` | Ordena as licitações por score de risco |
| `08_concentracao_fornecedor_orgao.sql` | Mede a concentração entre fornecedor e órgão |
| `09_view_licitacoes_analytics.sql` | Cria a view analítica consumida pelo dashboard |

## Fluxo de uso

1. Execute a carga do banco para popular o modelo dimensional.
2. Rode `09_view_licitacoes_analytics.sql` para criar ou atualizar a view analítica.
3. Execute as demais consultas para investigar recortes específicos.
4. Use a view como base para o dashboard e para análises ad hoc.

## View analítica

`vw_licitacoes_analytics` centraliza os campos mais usados na camada analítica, reduzindo a necessidade de joins repetidos nas consultas de consumo.

Ela foi desenhada para suportar:

- filtros por ano, órgão, categoria e nível de risco
- KPIs de valor, volume e recorrência
- análise de anomalias e risco final
- exploração por fornecedor e concentração de compras

## Indicadores cobertos

- valor total contratado
- quantidade de licitações
- valor médio por contrato
- fornecedores recorrentes
- contratos acima da média
- score médio de risco
- distribuição por nível de risco
- concentração de fornecedores por órgão

## Observação prática

As consultas assumem que o banco já está carregado e que a view analítica foi criada. Se a view não existir, o dashboard e parte das análises vão falhar na leitura dos dados.
