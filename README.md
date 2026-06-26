# Licitacoes Risk Intelligence Platform

Plataforma end-to-end para analise de risco em licitacoes publicas, desenvolvida como projeto de portfolio para demonstrar capacidade pratica em engenharia de dados, analytics engineering, machine learning aplicado e data apps.

O projeto simula um fluxo real de dados: gera uma base de licitacoes, aplica tratamento e modelagem analitica, persiste tudo em PostgreSQL, executa regras e modelos de risco e entrega os resultados em um dashboard interativo com foco em auditoria, compliance e controle interno.

## Visao executiva

Este projeto foi pensado para responder a uma pergunta objetiva de negocio: como priorizar licitacoes com maior potencial de risco usando dados, SQL e machine learning?

Principais entregas:

- pipeline completo de dados, da geracao da base ao consumo analitico
- modelo dimensional em PostgreSQL para consultas e dashboards
- camada SQL com indicadores e view analitica dedicada
- deteccao de anomalias com `IsolationForest`
- score final de risco com regras de negocio + sinal do modelo
- segmentacao de fornecedores com `KMeans`
- dashboard em `Streamlit` para exploracao executiva e analitica

## Problema de negocio

Em cenarios de compras publicas, equipes de auditoria e compliance lidam com grande volume de processos e poucos recursos para analise manual. A proposta desta plataforma e reduzir esse atrito ao organizar sinais de risco como:

- contratos muito acima do valor estimado
- fornecedores recorrentes em excesso
- concentracao por orgao ou categoria
- modalidades e status com maior sensibilidade analitica
- comportamentos atipicos identificados automaticamente

## O que foi construido

### 1. Engenharia de dados

- geracao de base simulada com dados brasileiros usando `Faker`
- padronizacao de textos, datas, CNPJ e atributos temporais
- criacao de colunas analiticas para risco, faixas de valor e variacao percentual
- carga de dados em PostgreSQL com separacao entre dimensoes e fato

### 2. Modelagem analitica

O banco segue uma estrutura em estrela para facilitar consumo em BI, SQL e aplicacoes analiticas:

- `dim_orgao`
- `dim_fornecedor`
- `dim_categoria`
- `dim_localidade`
- `dim_tempo`
- `fato_licitacoes`

Sobre essa base, o projeto disponibiliza consultas SQL e uma view consolidada:

- `09_view_licitacoes_analytics.sql`
- indicadores de valor por orgao
- fornecedores recorrentes
- compras por categoria
- evolucao mensal
- contratos acima da media
- indicadores e ranking de risco
- concentracao fornecedor-orgao

### 3. Machine learning aplicado

#### Deteccao de anomalias

O script `src/ml/anomaly_detection.py` usa `IsolationForest` com features financeiras e comportamentais para identificar licitacoes fora do padrao esperado.

Exemplos de sinais usados:

- valor estimado e valor contratado
- diferenca absoluta e percentual
- score de risco original
- frequencia de fornecedor e orgao
- media de valor por categoria
- percentual acima da media da categoria

#### Classificacao final de risco

O script `src/ml/risk_classification.py` combina regras de negocio com o resultado do modelo para produzir:

- `ml_score_risco_final`
- `ml_nivel_risco_final`
- `prioridade_auditoria`
- `motivos_risco`

Essa etapa aumenta interpretabilidade, o que e importante para contexto de auditoria.

#### Clusterizacao de fornecedores

O script `src/ml/supplier_clustering.py` usa `KMeans` para agrupar fornecedores por comportamento e exposicao a risco, gerando perfis como:

- fornecedor recorrente
- fornecedor de alto valor
- fornecedor de baixo risco
- fornecedor com atencao especial

## Dashboard

O dashboard em `Streamlit` consolida a analise em quatro frentes principais:

- visao geral com KPIs e filtros
- anomalias
- classificacao de risco
- fornecedores e clusters comportamentais

Arquivo principal:

- `dashboard/app.py`

## Escopo atual do dataset

Os arquivos gerados no repositorio hoje demonstram o pipeline funcionando ponta a ponta com:

- `1.500` registros de licitacoes simuladas
- `110` fornecedores clusterizados
- artefatos intermediarios e finais em `data/processed`

## Stack tecnica

| Camada | Tecnologias |
| --- | --- |
| Linguagem | Python |
| Dados | Pandas, SQLAlchemy |
| Banco | PostgreSQL |
| Containerizacao | Docker, Docker Compose |
| Machine Learning | scikit-learn |
| Dashboard | Streamlit, Plotly |
| Dados simulados | Faker |
| Configuracao | python-dotenv |

## Estrutura do repositorio

```text
.
+-- dashboard/           # app Streamlit
+-- data/
|   +-- raw/             # dados brutos
|   +-- processed/       # artefatos tratados e saidas de ML
|   `-- sample/          # amostras
+-- database/            # inicializacao do banco
+-- docker/              # volume/local de persistencia
+-- docs/                # documentacao complementar
+-- sql/analytics/       # consultas e view analitica
`-- src/
    +-- extraction/      # geracao/entrada de dados
    +-- transformation/  # limpeza e feature engineering
    +-- loading/         # carga no PostgreSQL
    +-- ml/              # modelos e regras de risco
    `-- utils/           # utilitarios compartilhados
```

## Como executar localmente

### Pre-requisitos

- Python 3.10+
- Docker Desktop

### 1. Clonar o repositorio

```bash
git clone https://github.com/CostaPaiiva/licitacoes-risk-intelligence-platform.git
cd licitacoes-risk-intelligence-platform
```

### 2. Configurar ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5433/licitacoes_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=licitacoes_db
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Subir infraestrutura

```bash
docker compose up -d
```

Servicos disponiveis:

- PostgreSQL em `localhost:5433`
- pgAdmin em `http://localhost:8081`

### 5. Executar o pipeline

```bash
python src/extraction/extract_sample_data.py
python src/transformation/transform_licitacoes.py
python src/loading/load_to_postgres.py
python src/ml/anomaly_detection.py
python src/ml/risk_classification.py
python src/ml/supplier_clustering.py
```

### 6. Iniciar o dashboard

```bash
streamlit run dashboard/app.py
```

Aplicacao disponivel em `http://localhost:8501`.

## Diferenciais tecnicos

- projeto organizado por camadas, com separacao clara entre extracao, transformacao, carga, SQL e ML
- uso combinado de regras de negocio e modelo estatistico, evitando uma abordagem de caixa-preta
- modelagem pensada para consumo analitico e nao apenas para armazenamento operacional
- saida interpretavel para auditoria, com prioridade e motivos de risco
- demonstracao pratica de stack recorrente em times de dados

## Evolucoes possiveis

- testes automatizados para pipeline e regras de risco
- orchestracao com Airflow, Prefect ou Mage
- validacao de dados com Great Expectations ou Pandera
- versionamento de modelos e experimentos
- deploy em cloud com banco gerenciado e app publica

## Sobre o projeto

Este repositorio foi construido como ativo de portfolio com foco em demonstrar:

- estruturacao de pipelines de dados
- modelagem analitica em SQL/PostgreSQL
- traducao de problema de negocio em regras e features
- aplicacao de machine learning em um caso plausivel de risco
- entrega final orientada a consumo por usuario de negocio
