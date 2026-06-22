# Relatório Técnico - Licitações Risk Intelligence Platform

## 1. Introdução

Este documento registra o estado atual do projeto Licitações Risk Intelligence Platform. A solução foi pensada para apoiar análise de risco em licitações públicas por meio de uma pipeline de dados com etapas de extração, transformação, carga, consulta analítica e evolução para inteligência preditiva.

O projeto ainda está em andamento. Este relatório descreve o que já foi implementado até aqui e deixa explícito que a continuidade virá em novas etapas.

## 2. Objetivo

O objetivo principal é estruturar uma base analítica capaz de apoiar auditoria, compliance, controle interno e exploração de padrões relevantes em contratos públicos.

A plataforma busca responder perguntas como:

- quais órgãos concentram maior volume financeiro;
- quais fornecedores aparecem com mais frequência;
- quais contratações ficam acima do valor estimado;
- quais categorias concentram mais recursos;
- quais registros apresentam maior risco;
- onde há indícios de anomalia ou comportamento atípico.

## 3. Escopo Implementado Até Agora

Até este ponto, o projeto já possui:

- geração e preparação de uma base bruta de licitações;
- transformação dos dados com limpeza e enriquecimento;
- carga para PostgreSQL com modelo dimensional;
- scripts SQL para análises;
- base de apoio para indicadores e modelos de machine learning;
- documentação técnica em progresso.

## 4. Arquitetura

A arquitetura foi organizada em camadas:

1. extração;
2. transformação;
3. carga;
4. banco relacional;
5. analytics;
6. modelos de machine learning;
7. dashboard.

Essa estrutura permite evoluir o projeto sem acoplamento excessivo entre as etapas.

## 5. Extração e Geração de Dados

A base inicial do projeto é composta por dados simulados de licitações públicas, produzidos para permitir testes da pipeline e validação do fluxo analítico.

Os registros contemplam informações como:

- órgão;
- fornecedor;
- CNPJ;
- categoria;
- valores;
- datas;
- modalidade;
- status;
- score de risco;
- nível de risco.

## 6. Transformação dos Dados

A etapa de transformação foi implementada em Python com foco em padronização, consistência e criação de colunas auxiliares.

Os principais tratamentos realizados são:

- normalização de campos textuais;
- limpeza de CNPJ;
- formatação de CNPJ para exibição;
- conversão de datas;
- criação de colunas temporais;
- cálculo de dias entre publicação e homologação;
- conversão de colunas numéricas;
- remoção de registros inválidos;
- recálculo da diferença entre valor estimado e contratado;
- criação de faixas de valor;
- criação de faixas de variação percentual;
- criação de indicadores booleanos de risco.

## 7. Carga no PostgreSQL

A carga está estruturada em modelo dimensional, com tabelas de dimensão e tabela fato.

Dimensões previstas/implementadas no pipeline:

- dimensão de órgão;
- dimensão de fornecedor;
- dimensão de categoria;
- dimensão de localidade;
- dimensão de tempo.

A tabela fato consolida os registros de licitações com as chaves das dimensões e os principais atributos analíticos.

## 8. Banco de Dados

A conexão com o banco está centralizada em `src/utils/database.py`, permitindo o uso de:

- `DATABASE_URL` como conexão única;
- ou variáveis separadas `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` e `POSTGRES_DB`.

A base foi pensada para rodar com PostgreSQL via Docker, o que facilita reprodução local do ambiente.

## 9. Estrutura Analítica

Foram adicionados scripts SQL para consultas que apoiam a análise do projeto, incluindo:

- total por órgão;
- fornecedores recorrentes;
- compras por categoria;
- evolução mensal;
- contratos acima da média;
- indicadores de risco.

## 10. Base para Continuidade

O projeto já deixou pronta a fundação para continuar com as próximas entregas:

### 10.1 Consolidação dos dados

- validar cargas;
- revisar integridade das chaves;
- estabilizar a modelagem final;
- revisar nomes de colunas e regras de negócio.

### 10.2 Camada de analytics

- aprofundar os KPIs;
- revisar métricas de volume, concentração e risco;
- consolidar queries para apoio ao dashboard.

### 10.3 Machine Learning

- ajustar modelos de classificação de risco;
- evoluir a detecção de anomalias;
- testar agrupamento de fornecedores;
- revisar features e métricas de avaliação.

### 10.4 Dashboard

- integrar as consultas ao painel;
- revisar UX e organização visual;
- priorizar os indicadores principais do projeto.

## 11. Resultado Parcial

Até aqui, o projeto já cobre a cadeia principal de engenharia de dados:

- entrada dos dados;
- tratamento e enriquecimento;
- persistência em banco;
- preparação para análise.

O trabalho ainda não está concluído. A próxima fase deve focar na consolidação analítica, no refinamento dos modelos e na construção da interface final.

## 12. Conclusão Parcial

Este relatório representa o estágio atual do projeto e serve como base para a continuação do desenvolvimento. A solução já possui a espinha dorsal da pipeline, mas ainda depende de etapas de refinamento, validação e visualização para atingir a versão final.
