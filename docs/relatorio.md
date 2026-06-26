# Relatório Técnico - Licitacoes Risk Intelligence Platform

## 1. Resumo executivo

O projeto Licitacoes Risk Intelligence Platform foi desenvolvido como uma solução end-to-end para análise de risco em licitações públicas. A proposta central é transformar dados brutos em informação analítica de alto valor, permitindo investigar padrões de contratação, identificar comportamentos atípicos e apoiar priorização de auditoria e compliance.

A solução integra geração de dados, tratamento, modelagem dimensional, carga em PostgreSQL, camada SQL analítica, modelos de machine learning e dashboard interativo. O resultado é uma plataforma completa para exploração técnica e apresentação executiva.

## 2. Contexto e problema de negócio

Em ambientes de compras públicas, equipes de auditoria e controle interno lidam com volume elevado de processos, múltiplos fornecedores e restrições de tempo para análise manual. Nesse cenário, o desafio não é apenas armazenar os dados, mas organizar sinais relevantes para apoiar decisão.

Este projeto foi estruturado para responder perguntas como:

- quais órgãos concentram maior volume financeiro;
- quais fornecedores se repetem com maior frequência;
- quais contratos apresentam valores acima do estimado;
- quais categorias concentram maior exposição financeira;
- quais licitações merecem maior prioridade de auditoria;
- onde há indícios de anomalia ou comportamento atípico.

## 3. Objetivo do projeto

O objetivo principal é construir uma base analítica confiável e interpretável para apoiar a análise de risco em licitações públicas.

Os objetivos específicos são:

- estruturar um pipeline de dados reproduzível;
- modelar os dados em formato dimensional para consumo analítico;
- criar consultas SQL voltadas à exploração executiva;
- aplicar machine learning para detecção de anomalias e segmentação de fornecedores;
- disponibilizar os resultados em um dashboard interativo.

## 4. Escopo implementado

Até o momento, o projeto cobre a maior parte da cadeia analítica:

- geração de base simulada de licitações;
- limpeza, padronização e feature engineering;
- carga em PostgreSQL com arquitetura dimensional;
- consultas SQL analíticas para exploração dos dados;
- detecção de anomalias com machine learning;
- classificação final de risco com regras de negócio e sinal estatístico;
- clusterização de fornecedores;
- dashboard em Streamlit para visualização dos resultados.

## 5. Arquitetura da solução

A arquitetura foi organizada em camadas para reduzir acoplamento e facilitar evolução:

1. extração e geração dos dados;
2. transformação e enriquecimento;
3. carga em banco relacional;
4. camada analítica SQL;
5. modelagem e classificação de risco;
6. dashboard interativo.

Essa separação torna o projeto mais fácil de manter, testar e explicar em contexto técnico.

## 6. Extração e geração de dados

A base utilizada no projeto foi gerada de forma simulada para permitir a validação completa do fluxo. A composição dos dados contempla entidades comuns ao domínio de licitações públicas, como órgão, fornecedor, categoria, valores, datas, modalidade, status e score de risco.

Os registros foram desenhados para refletir diferentes perfis de comportamento, incluindo fornecedores recorrentes, contratos de maior valor e casos com potencial de anomalia.

## 7. Transformação e enriquecimento

A etapa de transformação foi implementada em Python com foco em consistência, padronização e criação de atributos analíticos.

Os principais tratamentos realizados foram:

- normalização de campos textuais;
- limpeza e formatação de CNPJ;
- conversão e padronização de datas;
- criação de colunas temporais;
- cálculo de dias entre publicação e homologação;
- conversão de valores numéricos;
- validação de colunas obrigatórias;
- criação de faixas de valor e variação percentual;
- geração de indicadores auxiliares para análise de risco.

Essa etapa melhora a qualidade da base e prepara os dados para consumo em SQL, dashboard e modelos de machine learning.

## 8. Carga e modelagem em PostgreSQL

A carga foi estruturada em um modelo dimensional com tabelas de dimensão e tabela fato, favorecendo consultas analíticas e relatórios executivos.

### 8.1 Dimensões

- `dim_orgao`
- `dim_fornecedor`
- `dim_categoria`
- `dim_localidade`
- `dim_tempo`

### 8.2 Fato

- `fato_licitacoes`

A modelagem em estrela reduz complexidade de consulta, melhora legibilidade do modelo e facilita o consumo por camadas superiores, como SQL analítico e dashboard.

## 9. Camada analítica SQL

Após a carga dos dados, foi criada uma camada de consultas SQL para apoiar a análise exploratória e a geração de indicadores.

As consultas contemplam temas como:

- valor total por órgão;
- fornecedores recorrentes;
- compras por categoria;
- evolução mensal;
- contratos acima da média;
- indicadores de risco;
- ranking de licitações com maior risco;
- concentração fornecedor-órgão.

Também foi criada a view `vw_licitacoes_analytics`, que consolida os principais campos necessários para consumo por ferramentas analíticas e pela aplicação Streamlit.

Essa camada reduz a repetição de joins complexos e centraliza a lógica de leitura usada pelo dashboard.

## 10. Machine learning aplicado

O projeto incorpora uma etapa de ciência de dados voltada à geração de sinais analíticos mais sofisticados.

### 10.1 Detecção de anomalias

Foi utilizado o algoritmo `IsolationForest` para identificar licitações com comportamento atípico em relação ao conjunto analisado. A modelagem considera variáveis financeiras e comportamentais, como:

- valor estimado;
- valor contratado;
- diferença de valor;
- percentual de diferença;
- score de risco original;
- frequência de fornecedor;
- frequência de órgão;
- média de valor por categoria;
- percentual acima da média da categoria.

O resultado gera uma marcação de anomalia e um score associado ao comportamento observado.

### 10.2 Classificação final de risco

Após a detecção de anomalias, foi criada uma classificação final de risco combinando:

- score de risco original;
- resultado do modelo de anomalia;
- diferença percentual entre valor estimado e contratado;
- valor contratado;
- recorrência de fornecedor;
- modalidade de licitação;
- status do processo.

Essa abordagem aumenta a interpretabilidade do resultado final e aproxima a solução do uso real em auditoria e compliance.

### 10.3 Clusterização de fornecedores

Também foi aplicada a técnica `KMeans` para agrupar fornecedores com perfis semelhantes. A clusterização usa variáveis agregadas por fornecedor, como:

- total de contratos;
- total de órgãos atendidos;
- total de categorias atendidas;
- valor total contratado;
- valor médio do contrato;
- score médio de risco;
- total de anomalias;
- percentual de contratos de alto ou crítico risco.

Os grupos formados ajudam a identificar perfis como fornecedor recorrente, fornecedor de alto valor, fornecedor de baixo risco e fornecedor com atenção especial.

## 11. Dashboard analítico

Os resultados do pipeline, da modelagem e dos modelos foram disponibilizados em um dashboard construído com Streamlit e Plotly.

O dashboard foi organizado em abas para apoiar navegação rápida entre os principais pontos de análise:

- visão geral;
- anomalias;
- classificação de risco;
- fornecedores.

Os indicadores exibidos incluem:

- total de licitações;
- valor total contratado;
- valor médio contratado;
- total de fornecedores;
- total de órgãos;
- percentual de risco alto/crítico.

## 12. Resultados alcançados

O projeto já demonstra uma cadeia analítica completa, com entrega funcional em múltiplas camadas.

Resultados atuais:

- base com 1.500 registros simulados de licitações;
- 110 fornecedores clusterizados;
- 9 consultas SQL analíticas;
- view consolidada para consumo do dashboard;
- classificação final de risco com motivos explicáveis;
- dashboard interativo pronto para exploração.

## 13. Qualidade e interpretabilidade

Um ponto importante do projeto é a preocupação com interpretabilidade. Em vez de limitar a solução a um modelo preditivo isolado, o fluxo combina regras de negócio, indicadores objetivos e sinal estatístico.

Isso torna os resultados mais úteis para contexto de negócio, principalmente em auditoria, compliance e priorização de análise.

## 14. Limitações atuais

Como toda solução em evolução, o projeto ainda possui pontos a serem aprimorados:

- validação automatizada de dados;
- testes unitários e de integração;
- orquestração formal do pipeline;
- versionamento de modelos;
- monitoramento de qualidade e drift;
- publicação em ambiente cloud.

Essas melhorias estão alinhadas com a evolução natural de uma solução analítica mais madura.

## 15. Próximos passos

As próximas entregas planejadas incluem:

- expansão da camada de testes;
- validação de dados com Great Expectations ou Pandera;
- orquestração com Airflow, Prefect ou Mage;
- refinamento de features e métricas dos modelos;
- melhoria da experiência visual do dashboard;
- publicação em infraestrutura gerenciada.

## 16. Conclusão

O Licitacoes Risk Intelligence Platform já se apresenta como uma solução analítica completa, integrando engenharia de dados, modelagem dimensional, SQL, machine learning e visualização.

O principal valor do projeto está na capacidade de transformar dados públicos em sinais acionáveis para análise de risco, apoiando decisões mais rápidas, consistentes e interpretáveis.

Este relatório documenta o estado atual da solução e serve como base para a continuidade do desenvolvimento.
