# Licitações Risk Intelligence Platform

Uma plataforma de ponta a ponta para análise de risco em licitações públicas, demonstrando um fluxo completo de **Engenharia de Dados**, **Análise de Dados** e **Ciência de Dados**. A solução transforma dados brutos em insights acionáveis, apresentados em um dashboard interativo.

## 🎯 Objetivo

O projeto foi desenvolvido para estruturar uma base analítica robusta que apoie atividades de auditoria, compliance e controle interno em contratos públicos. A plataforma busca responder a perguntas críticas de negócio, como:

- Quais órgãos concentram os maiores volumes financeiros?
- Quais fornecedores possuem contratos recorrentes?
- Onde há indícios de sobrepreço ou comportamento atípico?
- Quais são as licitações com maior prioridade para auditoria?

## ✨ Principais Funcionalidades

- **Pipeline de Dados Completo**: Extração, transformação e carga (ETL) de dados simulados de licitações.
- **Modelagem Dimensional**: Os dados são estruturados em um modelo dimensional (Star Schema) em um banco de dados PostgreSQL, otimizado para consultas analíticas.
- **Análise de Risco com Machine Learning**:
  - **Detecção de Anomalias**: Utiliza o algoritmo `Isolation Forest` para identificar licitações com comportamento atípico.
  - **Classificação de Risco**: Combina regras de negócio e o resultado do modelo de anomalias para gerar um score de risco final e uma prioridade de auditoria.
  - **Clusterização de Fornecedores**: Agrupa fornecedores em perfis comportamentais (`KMeans`) como "Alto Valor", "Recorrente" ou "Atenção Especial".
- **Dashboard Interativo**: Uma interface em Streamlit que permite a exploração visual dos dados, indicadores e resultados dos modelos de ML.

## 📊 Dashboard (Amostra)

*Dica: Adicione aqui screenshots do seu dashboard em Streamlit. Eles são extremamente valiosos para demonstrar o resultado final do seu trabalho.*

**(Exemplo de Screenshot 1: Visão Geral)**

**(Exemplo de Screenshot 2: Análise de Risco e Anomalias)**

## 🏛️ Arquitetura da Solução

A plataforma foi projetada em camadas para garantir modularidade e escalabilidade:

1.  **Extração**: Geração de dados simulados com `Faker` e `Pandas`.
2.  **Transformação**: Limpeza, enriquecimento e feature engineering com `Python/Pandas`.
3.  **Carga**: Persistência dos dados em `PostgreSQL` com `SQLAlchemy`, seguindo um modelo dimensional.
4.  **Análise SQL**: Criação de views e queries analíticas para extrair insights e alimentar o dashboard.
5.  **Machine Learning**: Aplicação de modelos de `Scikit-learn` para detecção de anomalias, classificação e clusterização.
6.  **Visualização**: Dashboard interativo construído com `Streamlit` e `Plotly`.

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
| :--- | :--- |
| **Linguagem** | Python 3 |
| **Engenharia de Dados** | Pandas, SQLAlchemy, Docker, PostgreSQL |
| **Ciência de Dados** | Scikit-learn (IsolationForest, KMeans), Pandas |
| **Dashboard** | Streamlit, Plotly Express |
| **Utilitários** | Faker (geração de dados), Dotenv |

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar o ambiente localmente.

### Pré-requisitos

- Docker e Docker Compose
- Python 3.8+

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/licitacoes-risk-intelligence-platform.git
cd licitacoes-risk-intelligence-platform
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto, copiando o conteúdo de `.env.example` (se houver) ou usando o exemplo abaixo:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5433/licitacoes_db
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Iniciar os Serviços com Docker

Este comando irá iniciar os contêineres do PostgreSQL e do pgAdmin.

```bash
docker compose up -d
```

### 5. Executar a Pipeline de Dados

Execute os scripts na ordem correta para popular o banco de dados.

```bash
# 1. Gerar dados brutos (se necessário)
python src/extraction/extract_sample_data.py

# 2. Transformar os dados
python src/transformation/transform_licitacoes.py

# 3. Carregar os dados no PostgreSQL
python src/loading/load_to_postgres.py
```

### 6. Executar os Modelos de Machine Learning

```bash
# 1. Detecção de anomalias
python src/ml/anomaly_detection.py

# 2. Classificação de risco
python src/ml/risk_classification.py

# 3. Clusterização de fornecedores
python src/ml/supplier_clustering.py
```

### 7. Iniciar o Dashboard

Finalmente, inicie a aplicação Streamlit para visualizar os resultados.

```bash
streamlit run dashboard/app.py
```

Acesse http://localhost:8501 no seu navegador.

## 💡 Próximos Passos

O projeto está em constante evolução. As futuras implementações incluem:

- **Validação de Dados**: Implementar testes de qualidade de dados com ferramentas como `Great Expectations`.
- **Orquestração**: Adicionar um orquestrador de pipeline como `Apache Airflow` ou `Mage`.
- **Testes**: Aumentar a cobertura de testes unitários e de integração.
- **Otimização de Modelos**: Realizar tuning de hiperparâmetros e explorar outros algoritmos de ML.

---

*Este projeto foi desenvolvido como um portfólio para demonstrar habilidades em Engenharia e Ciência de Dados. Sinta-se à vontade para explorar, testar e entrar em contato!*