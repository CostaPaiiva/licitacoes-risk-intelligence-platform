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
## 9. Transformação e Tratamento dos Dados

Após a geração da base bruta, foi criada uma etapa de transformação utilizando Python e Pandas. Essa etapa tem como objetivo preparar os dados para uso analítico e posterior carga no banco PostgreSQL.

Durante o processo de transformação, foram aplicadas regras de limpeza, padronização e enriquecimento dos dados.

## 10. Tratamentos Realizados

Os principais tratamentos aplicados foram:

| Tratamento | Descrição |
|---|---|
| Padronização textual | Remoção de espaços extras e normalização dos campos textuais |
| Limpeza de CNPJ | Remoção de caracteres especiais, mantendo apenas números |
| Formatação de CNPJ | Criação de campo formatado para visualização |
| Conversão de datas | Conversão das datas para formato adequado |
| Enriquecimento temporal | Criação de ano, mês, dia, trimestre, nome do mês e ano/mês |
| Cálculo de prazo | Cálculo dos dias entre publicação e homologação |
| Validação numérica | Conversão e validação dos valores financeiros |
| Recalculo de diferença | Recalculo da diferença entre valor contratado e estimado |
| Faixa de valor | Classificação dos contratos por faixa financeira |
| Faixa de variação | Classificação da diferença percentual entre valores |
| Indicadores de risco | Criação de flags para facilitar análises futuras |

## 11. Novas Colunas Criadas

A etapa de transformação adicionou colunas analíticas importantes para o projeto:

| Nova coluna | Descrição |
|---|---|
| cnpj_limpo | CNPJ contendo apenas números |
| cnpj_formatado | CNPJ formatado para visualização |
| ano_publicacao | Ano extraído da data de publicação |
| mes_publicacao | Mês extraído da data de publicação |
| dia_publicacao | Dia extraído da data de publicação |
| nome_mes | Nome do mês da publicação |
| ano_mes | Ano e mês no formato YYYY-MM |
| dias_ate_homologacao | Quantidade de dias entre publicação e homologação |
| faixa_valor | Classificação do contrato por valor contratado |
| faixa_variacao | Classificação da variação entre valor contratado e estimado |
| valor_milhoes | Valor contratado convertido para milhões |
| is_valor_acima_estimado | Indica se o valor contratado ficou acima do estimado |
| is_risco_alto_ou_critico | Indica se a licitação possui risco alto ou crítico |
| is_dispensa_ou_inexigibilidade | Indica modalidades com maior atenção analítica |

## 12. Resultado da Etapa

Ao final da transformação, foi gerado o arquivo processado:

```txt
data/processed/licitacoes_processed.csv