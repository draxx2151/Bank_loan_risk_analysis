# AI-Assisted Bank Loan Analysis and Risk Intelligence Dashboard

An academic data analytics and machine learning solution for bank loan portfolio performance, financial KPI monitoring, and credit risk intelligence.

---

## 📌 Project Overview

This application empowers Bank Managers, Financial Analysts, and Loan Officers to analyze lending dataset metrics, monitor loan performance (Good vs Bad Standing), track month-to-month growth trends, explore borrower demographics, and leverage machine-learning default risk scoring for underwriting decision support.

Reference Repository Inspiration: [arnavchaturvedi17/Data-Analysis-Bank-Loan-Lending_Data_Analytics](https://github.com/arnavchaturvedi17/Data-Analysis-Bank-Loan-Lending_Data_Analytics)

---

## 🎯 Key Features & Capabilities

1. **Executive Summary Dashboard**: Real-time KPI monitoring (Total Applications, Total Funded Amount, Total Amount Received, Avg Interest Rate, Avg DTI) with Month-to-Date (MTD), Previous Month-to-Date (PMTD), and Month-over-Month (MoM) metrics.
2. **Portfolio Risk Health Analysis**: Explicit breakdown of Good Loans (`Fully Paid`, `Current`) vs Bad Loans (`Charged Off`), including funded vs recovered amounts and approval ratios.
3. **Multi-Dimensional Overview**: Dynamic visual analytics by Issue Date Month, US State geography, Loan Purpose, Employment Duration, Home Ownership, and Loan Term.
4. **Data Grid & Export**: Fully searchable, filterable grid displaying underlying loan application records with CSV export capabilities.
5. **AI Risk Intelligence Engine**: Scikit-Learn predictive model evaluating default risk probability based on loan amount, interest rate, annual income, DTI, employment length, and grade. Includes an interactive "Loan Risk Calculator".

---

## 🛠️ Technology Stack

- **Data Processing**: Python, Pandas, NumPy
- **Database & Querying**: SQL (SQLite, MySQL compatible)
- **Machine Learning**: Scikit-Learn (Logistic Regression / Random Forest Classifier)
- **Data Visualization**: Plotly, Streamlit
- **Quality & Testing**: PyTest, Schema Validation

---

## 📁 Modular Project Structure

```
c:/Bank_loan_risk_analysis/
├── data/
│   ├── raw/                  # Authentic dataset (financial_loan.csv)
│   └── processed/            # Cleaned data & SQLite database (bank_loans.db)
├── sql/
│   ├── schema.sql            # Table DDL statements
│   ├── kpi_queries.sql       # Analytical KPI SQL queries
│   └── views.sql             # SQL views for aggregated metrics
├── src/
│   ├── database/             # SQLite & MySQL connection interface
│   ├── data_processing/      # Data cleaning & validation modules
│   ├── analytics/            # Financial KPI engine & ML risk models
│   └── ui/                   # Streamlit layout & page views
├── tests/                    # Automated unit tests
├── docs/                     # Architecture & Data Dictionary
├── app.py                    # Main Streamlit Dashboard Entrypoint
├── requirements.txt          # Dependencies
├── PROJECT_PROGRESS.md       # Chronological development tracker
└── README.md                 # Documentation
```

---

## 🚀 Quick Start Guide

### 1. Installation
```powershell
pip install -r requirements.txt
```

### 2. Run Dashboard
```powershell
streamlit run app.py
```

### 3. Run Automated Tests
```powershell
pytest tests/
```
