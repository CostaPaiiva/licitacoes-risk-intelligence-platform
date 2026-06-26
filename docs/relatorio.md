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

## 17. Camada Analítica com SQL

Após a carga dos dados no PostgreSQL, foi criada uma camada analítica utilizando SQL. Essa camada permite explorar os dados de licitações a partir de diferentes perspectivas, como órgão público, fornecedor, categoria, tempo e risco.

## 18. Consultas Criadas

Foram criadas consultas para responder perguntas analíticas relevantes, como:

- quais órgãos concentram maior valor contratado;
- quais fornecedores aparecem com maior recorrência;
- quais categorias possuem maior volume financeiro;
- como os contratos evoluem ao longo do tempo;
- quais contratos possuem valores muito acima da média da categoria;
- qual a distribuição dos contratos por nível de risco;
- quais licitações aparecem no topo do ranking de risco;
- onde existe maior concentração entre fornecedor e órgão.

## 19. View Analítica

Também foi criada a view `vw_licitacoes_analytics`, consolidando informações da tabela fato e das dimensões.

Essa view facilita o consumo dos dados em ferramentas de BI, dashboards e scripts de ciência de dados, evitando a repetição de joins complexos em diferentes análises.

## 20. Resultado da Etapa

Ao final desta etapa, o projeto passou a contar com uma camada SQL estruturada, permitindo análises de auditoria, compliance e inteligência em compras públicas.

Essa etapa reforça a proposta do projeto como uma solução completa de dados, integrando modelagem dimensional, banco relacional e consultas analíticas.

## 21. Dashboard Analítico

Após a criação da camada analítica SQL, foi desenvolvido um dashboard interativo utilizando Streamlit e Plotly.

O objetivo do dashboard é permitir a análise visual dos principais indicadores relacionados às licitações públicas, facilitando a identificação de padrões financeiros, fornecedores recorrentes, concentração de contratos e níveis de risco.

## 22. Indicadores do Dashboard

O dashboard apresenta os seguintes indicadores:

| Indicador | Descrição |
|---|---|
| Total de licitações | Quantidade total de registros analisados |
| Valor total contratado | Soma dos valores contratados |
| Valor médio contratado | Média dos valores contratados |
| Total de fornecedores | Quantidade de fornecedores distintos |
| Total de órgãos | Quantidade de órgãos públicos distintos |
| Risco alto/crítico | Percentual de licitações classificadas como alto ou crítico risco |

## 23. Visualizações Criadas

As principais visualizações desenvolvidas foram:

- top 10 órgãos por valor contratado;
- top 10 fornecedores recorrentes;
- distribuição de valores por categoria;
- distribuição por nível de risco;
- evolução mensal dos contratos;
- ranking das licitações com maior score de risco;
- análise consolidada por fornecedor.

## 24. Resultado da Etapa

Com o dashboard, o projeto passa a ter uma camada visual interativa, permitindo que os dados processados e armazenados no PostgreSQL sejam explorados de maneira simples e profissional.

Essa etapa transforma o projeto em uma solução analítica completa, integrando pipeline de dados, banco relacional, SQL analítico e visualização.

## 25. Detecção de Anomalias com Machine Learning

Após a criação do pipeline de dados, da modelagem dimensional, das consultas SQL e do dashboard, foi adicionada uma etapa de Ciência de Dados voltada para detecção de anomalias.

O objetivo dessa etapa é identificar licitações com comportamento atípico em relação ao conjunto de dados analisado.

## 26. Algoritmo Utilizado

Foi utilizado o algoritmo Isolation Forest, técnica de aprendizado não supervisionado voltada para identificação de observações incomuns em bases de dados.

No contexto do projeto, o modelo foi aplicado para detectar licitações que apresentam padrões financeiros ou comportamentais fora do esperado.

## 27. Variáveis Utilizadas

As principais variáveis utilizadas pelo modelo foram:

| Variável | Descrição |
|---|---|
| valor_estimado | Valor previsto inicialmente para a licitação |
| valor_contratado | Valor efetivamente contratado |
| diferenca_valor | Diferença entre valor contratado e estimado |
| percentual_diferenca | Diferença percentual entre os valores |
| score_risco | Pontuação inicial de risco |
| frequencia_fornecedor | Quantidade de contratos associados ao fornecedor |
| frequencia_orgao | Quantidade de contratos associados ao órgão |
| media_valor_categoria | Média de valor contratado da categoria |
| percentual_acima_media_categoria | Percentual acima ou abaixo da média da categoria |

## 28. Resultado da Etapa

O modelo gerou novas colunas analíticas indicando se a licitação foi classificada como anomalia e qual o nível de alerta associado.

O resultado foi salvo no arquivo:

`data/processed/licitacoes_anomaly_detection.csv`

Essa etapa fortalece o projeto ao adicionar uma camada de Ciência de Dados aplicada à análise de risco em licitações públicas.

## 29. Classificação Final de Risco

Após a detecção de anomalias, foi criada uma etapa de classificação final de risco. Essa etapa combina o score inicial da base, o resultado do modelo de anomalias e regras adicionais de negócio.

O objetivo é transformar os indicadores técnicos em uma classificação mais interpretável para auditoria, compliance e tomada de decisão.

## 30. Critérios Utilizados

A classificação final considera:

| Critério | Justificativa |
|---|---|
| Score de risco inicial | Representa a primeira avaliação baseada em regras |
| Anomalia detectada pelo modelo | Indica comportamento estatisticamente atípico |
| Diferença percentual | Mede quanto o valor contratado se distancia do estimado |
| Valor contratado | Contratos de maior valor exigem maior atenção |
| Frequência do fornecedor | Fornecedores recorrentes podem indicar concentração |
| Modalidade | Dispensa e inexigibilidade exigem maior atenção analítica |
| Status | Licitações canceladas, suspensas ou revogadas podem indicar sensibilidade |

## 31. Saídas Geradas

A etapa gera as seguintes colunas:

| Coluna | Descrição |
|---|---|
| ml_score_risco_final | Pontuação final de risco |
| ml_nivel_risco_final | Classificação final em Baixo, Médio, Alto ou Crítico |
| prioridade_auditoria | Nível de prioridade para análise |
| motivos_risco | Explicação textual dos principais fatores de risco |

## 32. Resultado da Etapa

O resultado da classificação final de risco foi salvo no arquivo:

`data/processed/licitacoes_risk_classification.csv`

Essa etapa torna o projeto mais interpretável, pois não apenas identifica riscos, mas também explica os principais motivos associados a cada licitação.

## 33. Clusterização de Fornecedores

Além da detecção de anomalias e da classificação de risco, foi criada uma etapa de clusterização de fornecedores utilizando KMeans.

O objetivo dessa etapa é identificar grupos de fornecedores com comportamentos semelhantes, permitindo análises sobre recorrência, concentração, valor financeiro e exposição a riscos.

## 34. Variáveis Utilizadas na Clusterização

A clusterização foi construída a partir de uma base agregada por fornecedor.

As principais variáveis utilizadas foram:

| Variável | Descrição |
|---|---|
| total_contratos | Quantidade de contratos associados ao fornecedor |
| total_orgaos | Quantidade de órgãos públicos atendidos |
| total_categorias | Quantidade de categorias atendidas |
| valor_total_contratado | Soma total dos contratos do fornecedor |
| valor_medio_contrato | Valor médio dos contratos |
| maior_contrato | Maior contrato identificado |
| score_medio_original | Média do score inicial de risco |
| score_medio_final | Média do score final de risco |
| total_anomalias | Quantidade de contratos classificados como anomalia |
| contratos_alto_critico | Quantidade de contratos com risco alto ou crítico |
| contratos_criticos | Quantidade de contratos críticos |
| percentual_anomalias | Percentual de contratos classificados como anomalia |
| percentual_alto_critico | Percentual de contratos com risco alto ou crítico |

## 35. Perfis Gerados

Os fornecedores foram agrupados em perfis interpretáveis:

| Perfil | Interpretação |
|---|---|
| Fornecedor recorrente | Fornecedor com presença frequente na base |
| Fornecedor de alto valor | Fornecedor associado a contratos de maior valor financeiro |
| Fornecedor de baixo risco | Fornecedor com comportamento mais estável |
| Fornecedor com atenção especial | Fornecedor com maior presença de anomalias, contratos críticos ou indicadores de risco |

## 36. Resultado da Etapa

O resultado da clusterização foi salvo em:

`data/processed/fornecedores_clusterizados.csv`

Essa etapa fortalece a análise de fornecedores, permitindo identificar padrões de concentração, recorrência e exposição a risco em compras públicas.

## 37. Integração dos Modelos ao Dashboard

Após a criação dos modelos de detecção de anomalias, classificação de risco e clusterização de fornecedores, os resultados foram integrados ao dashboard em Streamlit.

A interface foi organizada em abas para facilitar a navegação entre os diferentes tipos de análise.

## 38. Abas do Dashboard

| Aba | Objetivo |
|---|---|
| Visão Geral | Apresenta os principais indicadores das licitações |
| Anomalias | Mostra os registros classificados como anômalos pelo modelo |
| Classificação de Risco | Apresenta o risco final, prioridade de auditoria e motivos de risco |
| Fornecedores | Exibe os perfis criados pela clusterização de fornecedores |

## 39. Resultado da Integração

Com essa integração, o projeto passa a funcionar como uma plataforma analítica completa, reunindo engenharia de dados, banco relacional, SQL analítico, machine learning e dashboard interativo.

Essa etapa fortalece a apresentação do projeto como uma solução aplicada a auditoria, compliance e inteligência em compras públicas.