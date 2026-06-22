# Relatório Técnico — Licitações Risk Intelligence Platform

## 1. Introdução

Este projeto tem como objetivo desenvolver uma plataforma de inteligência analítica aplicada ao contexto de licitações públicas. A proposta é construir uma solução completa de dados capaz de coletar, tratar, armazenar, analisar e visualizar informações relacionadas a contratos públicos, com foco na identificação de padrões de risco.

O projeto foi desenvolvido com foco em Engenharia de Dados, Ciência de Dados e Análise de Dados, utilizando tecnologias como Python, Pandas, PostgreSQL, Docker, SQL, Scikit-learn e Streamlit.

## 2. Objetivo do Projeto

O principal objetivo do sistema é demonstrar como dados de licitações podem ser utilizados para apoiar processos de auditoria, controle interno, compliance e análise de gastos públicos.

A plataforma busca identificar:

- fornecedores recorrentes;
- valores contratados acima da média;
- concentração de contratos por órgão;
- categorias com maior volume financeiro;
- evolução mensal das contratações;
- contratos com maior score de risco;
- possíveis anomalias nos dados.

## 3. Arquitetura Inicial

A arquitetura do projeto foi organizada em camadas:

- extração de dados;
- transformação e tratamento;
- carga em banco PostgreSQL;
- consultas analíticas SQL;
- modelos de ciência de dados;
- dashboard interativo.

A estrutura foi planejada para simular um fluxo real de dados, desde a origem até a camada de visualização.

## 4. Geração da Base de Dados

Nesta etapa, foi criada uma base simulada de licitações públicas utilizando Python, Pandas e Faker.

A base gerada contém registros com aparência realista, incluindo órgãos públicos, fornecedores, CNPJs, categorias de contratação, valores, datas, modalidades e status das licitações.

## 5. Campos Gerados

A base contém os seguintes campos principais:

| Campo | Descrição |
|---|---|
| id_licitacao | Identificador único da licitação |
| numero_processo | Número fictício do processo |
| orgao | Nome do órgão público |
| cidade | Cidade vinculada à licitação |
| estado | Unidade federativa |
| regiao | Região do Brasil |
| categoria | Categoria da contratação |
| grupo_categoria | Grupo geral da categoria |
| descricao | Descrição da contratação |
| fornecedor | Empresa vencedora ou participante |
| cnpj_fornecedor | CNPJ fictício do fornecedor |
| porte_empresa | Porte da empresa |
| valor_estimado | Valor estimado da contratação |
| valor_contratado | Valor contratado |
| diferenca_valor | Diferença entre valor contratado e estimado |
| percentual_diferenca | Diferença percentual entre valores |
| data_publicacao | Data de publicação da licitação |
| data_homologacao | Data de homologação |
| ano | Ano da publicação |
| mes | Mês da publicação |
| trimestre | Trimestre da publicação |
| modalidade | Modalidade da licitação |
| status | Status da licitação |
| fornecedor_recorrente | Indica se o fornecedor aparece de forma recorrente |
| possivel_outlier | Indica se o registro foi gerado como possível anomalia |
| score_risco | Pontuação inicial de risco |
| nivel_risco | Classificação do risco |

## 6. Regras Iniciais de Risco

A pontuação inicial de risco foi construída com base em regras simples e interpretáveis.

Foram considerados fatores como:

- percentual de diferença entre valor estimado e valor contratado;
- fornecedor recorrente;
- modalidade de contratação;
- status da licitação;
- presença de outlier intencional.

A partir da pontuação final, cada licitação foi classificada em um dos seguintes níveis:

- Baixo;
- Médio;
- Alto;
- Crítico.

## 7. Resultado da Etapa

Ao final desta etapa, foram gerados dois arquivos:

```txt
data/raw/licitacoes_raw.csv
data/sample/licitacoes_sample.csv