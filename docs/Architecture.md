# Technical Architecture: AI-Assisted Bank Loan Analysis and Risk Intelligence Dashboard

---

## 1. System Overview

The system is engineered as a decoupled, multi-tiered data analytics and machine learning application. It ingests raw bank lending records, cleans and validates data formats, loads structured data into SQL databases (SQLite/MySQL), computes core financial KPIs and dynamic aggregations, trains an ML risk model, and presents an interactive Streamlit executive portal.

```
[Raw CSV File] 
     │
     ▼
[ETL & Validation Layer (src/data_processing/)]
     │
     ▼
[SQL Database Layer (SQLite / MySQL DB via src/database/)]
     │
     ├──────────────────────────┐
     ▼                          ▼
[KPI Engine]            [ML Risk Intelligence Engine]
(src/analytics/)        (Scikit-Learn Classifier)
     │                          │
     └──────────────────────────┤
                                ▼
                 [Streamlit UI Portal Layer]
                 (src/ui/ & app.py)
```

---

## 2. Module Specifications

### Data Processing (`src/data_processing/`)
- `cleaner.py`: Parses dates (`dd-mm-yyyy`), strips whitespace from string fields, handles missing values, converts interest rates & DTIs to standardized percentages/floats.
- `validator.py`: Enforces column presence, data types, value ranges (e.g. non-negative income/amounts), and generates data quality reports.

### Database Layer (`src/database/`)
- `db_manager.py`: Manages SQLite connection lifecycle, table creation, bulk insertion, query execution, and parameter sanitization. Supports optional MySQL connection via `mysql-connector-python`.

### Analytics & ML Layer (`src/analytics/`)
- `kpi_engine.py`: Computes core financial KPIs (Total Loan Applications, Total Funded Amount, Total Amount Received, Avg Int Rate, Avg DTI, Good vs Bad loan ratios, MTD, PMTD, MoM metrics).
- `ml_risk_model.py`: Trains Logistic Regression / Random Forest classification models on historical loan attributes (`dti`, `int_rate`, `annual_income`, `loan_amount`, `emp_length`, `grade`) to predict probability of default and output automated risk recommendations (Grades A to F).

### Visualization & User Interface Layer (`src/ui/`)
- `components.py`: Standardized metric cards, Plotly charts (bar, line, map, pie), styled containers, and filter controls.
- `views/summary.py`: Executive Summary view.
- `views/overview.py`: Detailed breakdown view (Trends, Geography, Purpose, Term, Grade).
- `views/details.py`: Filterable data table grid with CSV export options.
- `views/risk_intelligence.py`: Interactive AI Risk Calculator & Underwriting Simulator.

---

## 3. Technology Stack

- **Python 3.10+**: Core programming language.
- **Pandas & NumPy**: High-performance data manipulation and numerical analysis.
- **SQLite / MySQL**: Relational SQL engine for data persistence and analytical queries.
- **Plotly Express & Graph Objects**: Interactive, responsive charts and maps.
- **Streamlit**: Modern Web application framework for dynamic data dashboards.
- **Scikit-Learn**: Machine learning framework for credit risk classification.
- **PyTest**: Automated unit test runner.
