# Licitacoes Risk Intelligence Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/ML-IsolationForest%20%7C%20KMeans-111827?style=flat-square" alt="ML" />
  <img src="https://img.shields.io/badge/Analytics-SQL%20%7C%20Star%20Schema-111827?style=flat-square" alt="Analytics" />
  <img src="https://img.shields.io/badge/Focus-Risk%20Intelligence-111827?style=flat-square" alt="Focus" />
  <img src="https://img.shields.io/badge/Portfolio-Data%20Engineering-111827?style=flat-square" alt="Portfolio" />
</p>

<p align="center">
  Plataforma end-to-end para analise de risco em licitacoes publicas, desenhada para demonstrar engenharia de dados, analytics engineering, machine learning aplicado e entrega de produto em dashboard.
</p>

## Why this project stands out

<table>
  <tr>
    <td>
      <strong>End-to-end delivery</strong><br/>
      Da geracao da base ao dashboard final, com pipeline executavel localmente.
    </td>
    <td>
      <strong>Business-oriented</strong><br/>
      Foco em auditoria, compliance e priorizacao de investigacoes.
    </td>
    <td>
      <strong>Interpretabilidade</strong><br/>
      Regras de negocio + ML + motivos de risco para apoiar decisao.
    </td>
  </tr>
</table>

## Tech stack

<table>
  <tr>
    <td><strong>Language</strong><br/>Python 3.10+</td>
    <td><strong>Data</strong><br/>Pandas, SQLAlchemy</td>
    <td><strong>Database</strong><br/>PostgreSQL</td>
    <td><strong>Containers</strong><br/>Docker, Docker Compose</td>
  </tr>
  <tr>
    <td><strong>ML</strong><br/>scikit-learn, IsolationForest, KMeans</td>
    <td><strong>Dashboard</strong><br/>Streamlit, Plotly</td>
    <td><strong>Dataset</strong><br/>Faker, CSV pipelines</td>
    <td><strong>Config</strong><br/>python-dotenv</td>
  </tr>
</table>

## Executive summary

This project answers a practical question: how do you prioritize public procurement processes with the highest risk potential using data, SQL and machine learning?

The solution simulates a realistic data flow, stores it in a dimensional model, generates analytical views, scores risk with combined rules and ML signals, and exposes the result in a dashboard for fast investigation.

## Key outcomes

- complete data pipeline from raw data generation to analytical consumption
- star schema in PostgreSQL for reporting and dashboard queries
- SQL analytics layer with dedicated views and investigation queries
- anomaly detection with `IsolationForest`
- final risk classification combining business rules and model output
- supplier clustering with `KMeans`
- interactive dashboard built with `Streamlit`

## Core capabilities

### Data engineering

- simulated Brazilian procurement data with `Faker`
- text, date and CNPJ normalization
- feature engineering for risk analysis
- dimensional load into PostgreSQL

### Analytics engineering

- star schema with `dim_orgao`, `dim_fornecedor`, `dim_categoria`, `dim_localidade`, `dim_tempo` and `fato_licitacoes`
- analytical SQL for spend concentration, recurrence, risk ranking and monthly evolution
- consolidated view `vw_licitacoes_analytics` for downstream consumption

### Machine learning

- anomaly detection over financial and behavioral features
- final risk score combining original score, anomaly flag and business thresholds
- supplier profiling into operationally useful clusters

### Product layer

- Streamlit dashboard focused on executive exploration
- filters by year, agency, category and risk
- views for general overview, anomalies, risk classification and suppliers

## Business value

This platform helps teams working with public procurement identify:

- contracts far above expected values
- recurring suppliers with concentration patterns
- agencies with higher spend concentration
- high-risk procurement processes requiring audit priority
- atypical behavior that deserves review

## Project metrics

<table>
  <tr>
    <td align="center"><strong>1,500</strong><br/>simulated procurement records</td>
    <td align="center"><strong>110</strong><br/>clustered suppliers</td>
    <td align="center"><strong>9</strong><br/>SQL analytics queries</td>
    <td align="center"><strong>1</strong><br/>analytical dashboard</td>
  </tr>
</table>

## Repository structure

```text
.
+-- dashboard/           # Streamlit app
+-- data/
|   +-- raw/             # raw data
|   +-- processed/       # processed data and ML outputs
|   `-- sample/          # sample files
+-- database/            # database bootstrap
+-- docker/              # local persistence volume
+-- docs/                # supporting documentation
+-- sql/analytics/       # analytical SQL and view
`-- src/
    +-- extraction/      # data generation and ingestion
    +-- transformation/  # cleansing and feature engineering
    +-- loading/         # PostgreSQL load
    +-- ml/              # risk models and clustering
    `-- utils/           # shared utilities
```

## How to run locally

### Prerequisites

- Python 3.10+
- Docker Desktop

### 1. Clone the repository

```bash
git clone https://github.com/CostaPaiiva/licitacoes-risk-intelligence-platform.git
cd licitacoes-risk-intelligence-platform
```

### 2. Configure environment

Create a `.env` file at the project root:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5433/licitacoes_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=licitacoes_db
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start infrastructure

```bash
docker compose up -d
```

Services available:

- PostgreSQL on `localhost:5433`
- pgAdmin on `http://localhost:8081`

### 5. Run the pipeline

```bash
python src/extraction/extract_sample_data.py
python src/transformation/transform_licitacoes.py
python src/loading/load_to_postgres.py
python src/ml/anomaly_detection.py
python src/ml/risk_classification.py
python src/ml/supplier_clustering.py
```

### 6. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

Open `http://localhost:8501` in your browser.

## Differentiators

- clear separation between extraction, transformation, loading, analytics and ML
- business logic translated into transparent risk signals
- analytical design oriented to decision support, not just storage
- portfolio-level implementation that shows technical breadth and execution quality

## Next steps

- automated tests for the pipeline and risk rules
- orchestration with Airflow, Prefect or Mage
- data validation with Great Expectations or Pandera
- model versioning and experiment tracking
- cloud deployment with managed database and public app

## Portfolio note

This repository is designed to show how a data project can be turned into a product narrative: a real business problem, a structured data stack, explainable risk logic and a final interface that a recruiter or hiring manager can review quickly.
