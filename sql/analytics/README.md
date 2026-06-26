# SQL Analytics

<p align="center">
  <img src="https://img.shields.io/badge/PostgreSQL-Analytics%20Layer-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL Analytics" />
  <img src="https://img.shields.io/badge/SQL-Views%20%26%20Queries-111827?style=for-the-badge" alt="SQL" />
  <img src="https://img.shields.io/badge/Dashboard-Data%20Consumption-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Dashboard" />
</p>

<p align="center">
  Camada analitica do projeto, com consultas SQL e view consolidada para auditoria, compliance e consumo pelo dashboard.
</p>

## Overview

<table>
  <tr>
    <td>
      <strong>Purpose</strong><br/>
      Transformar o modelo dimensional em consultas prontas para analise executiva.
    </td>
    <td>
      <strong>Consumption</strong><br/>
      Servir de base para o Streamlit e para analises ad hoc.
    </td>
    <td>
      <strong>Focus</strong><br/>
      Spend analysis, risk signals and supplier concentration.
    </td>
  </tr>
</table>

## What is here

| File | Purpose |
| --- | --- |
| `01_total_por_orgao.sql` | Total contracted value by public agency |
| `02_fornecedores_recorrentes.sql` | Suppliers with repeat contracts |
| `03_compras_por_categoria.sql` | Procurement analysis by category |
| `04_evolucao_mensal.sql` | Monthly evolution of procurements |
| `05_contratos_acima_media.sql` | Contracts above category average |
| `06_indicadores_risco.sql` | Risk indicators by level |
| `07_ranking_geral_risco.sql` | Highest risk procurement ranking |
| `08_concentracao_fornecedor_orgao.sql` | Supplier-agency concentration analysis |
| `09_view_licitacoes_analytics.sql` | Main analytical view for the app |

## How it fits in the project

1. The loading step populates the dimensional model in PostgreSQL.
2. `09_view_licitacoes_analytics.sql` creates the analytical view used by the dashboard.
3. The remaining queries are used for specific investigations and reporting.
4. The dashboard reads from the consolidated layer instead of rebuilding joins on every screen.

## Analytical view

`vw_licitacoes_analytics` centralizes the fields most used by the product layer and reduces repeated joins in consumption queries.

It supports:

- filtering by year, agency, category and risk level
- KPIs for volume, value and recurrence
- anomaly and final risk analysis
- supplier-level exploration and concentration checks

## Indicators covered

- total contracted value
- procurement count
- average contract value
- recurring suppliers
- contracts above average
- average risk score
- risk level distribution
- supplier concentration by agency

## Why this matters

This SQL layer is the bridge between the modeled data and the decision-making layer. It keeps business logic reusable, keeps the dashboard lighter and makes the project easier to explain in a technical interview.

## Practical note

The queries assume the database is already loaded and the analytical view exists. If the view is missing, the dashboard and some investigations will fail when reading the data.
