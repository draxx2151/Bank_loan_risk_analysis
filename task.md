# Project Task Roadmap & Implementation Status

**Project Name:** AI-Assisted Bank Loan Analysis and Risk Intelligence Dashboard  
**Project Location:** `C:\Bank_loan_risk_analysis`  
**Technology Stack:** Python 3.14+, Pandas, NumPy, SQL (SQLite default), Streamlit, Plotly, Scikit-learn, PyTest, Joblib  

---

## 1. Executive Summary & Audit Baseline

Based on an empirical audit of the repository, all core data processing, database management, KPI analytics, machine learning modeling, and Streamlit user interface components have been built, integrated, and verified against 37 automated PyTest unit tests with a 100% pass rate.

### Verified Project Assets
- **Authentic Raw Dataset**: [data/raw/financial_loan.csv](file:///c:/Bank_loan_risk_analysis/data/raw/financial_loan.csv) (38,576 records, 25 columns, 7.8 MB).
- **Cleaned Dataset**: [data/processed/financial_loan_cleaned.csv](file:///c:/Bank_loan_risk_analysis/data/processed/financial_loan_cleaned.csv) (38,576 records, 33 columns).
- **SQLite Database**: [data/processed/bank_loans.db](file:///c:/Bank_loan_risk_analysis/data/processed/bank_loans.db) (38,576 records, 7 analytical database views).
- **Trained Model Pipeline**: [artifacts/models/credit_risk_pipeline_v1.0.0.joblib](file:///c:/Bank_loan_risk_analysis/artifacts/models/credit_risk_pipeline_v1.0.0.joblib) (Logistic Regression Pipeline, Test ROC-AUC = 0.6953, Recall = 65.23%).
- **Streamlit Entrypoint**: [app.py](file:///c:/Bank_loan_risk_analysis/app.py) (Multi-page dashboard with global sidebar filters).
- **Automated Test Suite**: 37 unit and integration tests passing cleanly in `5.42s`.

---

## 2. Actionable Implementation Roadmap

### Phase 1: Existing Project Audit & Infrastructure Setup
- [x] **Task 1.1: Environment & Repository Structure Audit**
  - **Priority**: High
  - **Relevant Files**: [requirements.txt](file:///c:/Bank_loan_risk_analysis/requirements.txt), `src/`
  - **Acceptance Criteria**: Verify directory layout (`data/`, `sql/`, `src/`, `tests/`, `artifacts/`, `docs/`) and install dependencies.
  - **Status**: Completed (38,576 record dataset verified).

- [x] **Task 1.2: Core Project Documentation Creation**
  - **Priority**: High
  - **Relevant Files**: [README.md](file:///c:/Bank_loan_risk_analysis/README.md), [docs/Data_Dictionary.md](file:///c:/Bank_loan_risk_analysis/docs/Data_Dictionary.md), [docs/Architecture.md](file:///c:/Bank_loan_risk_analysis/docs/Architecture.md)
  - **Acceptance Criteria**: Comprehensive documentation detailing schema, architecture, setup guide, and progress log.
  - **Status**: Completed.

---

### Phase 2: Data Processing, Schema Validation & Database Layer
- [x] **Task 2.1: Data Cleaning Pipeline Implementation**
  - **Priority**: High
  - **Relevant Files**: [src/config.py](file:///c:/Bank_loan_risk_analysis/src/config.py), [src/data_processing/cleaner.py](file:///c:/Bank_loan_risk_analysis/src/data_processing/cleaner.py)
  - **Acceptance Criteria**: Standardize dates (`dd-mm-yyyy` -> `YYYY-MM-DD`), map missing `States` via 2-letter `address_state` codes using `US_STATE_MAP`, convert `term_months` and `emp_length_years`, preserve 100% of raw records (38,576 rows).
  - **Status**: Completed.

- [x] **Task 2.2: Data Quality & Schema Validation**
  - **Priority**: High
  - **Relevant Files**: [src/data_processing/validator.py](file:///c:/Bank_loan_risk_analysis/src/data_processing/validator.py)
  - **Acceptance Criteria**: Validate column presence, duplicate primary keys (`id`), numeric bounds, loan status enum values, and generate data quality reports.
  - **Status**: Completed.

- [x] **Task 2.3: SQLite Database & Analytical View Setup**
  - **Priority**: High
  - **Relevant Files**: [sql/schema.sql](file:///c:/Bank_loan_risk_analysis/sql/schema.sql), [sql/views.sql](file:///c:/Bank_loan_risk_analysis/sql/views.sql), [src/database/db_manager.py](file:///c:/Bank_loan_risk_analysis/src/database/db_manager.py)
  - **Acceptance Criteria**: Initialize `bank_loans` SQLite table schema with indexes and 7 analytical database views (`vw_monthly_trends`, `vw_state_summary`, `vw_purpose_summary`, `vw_grade_summary`, `vw_term_summary`, `vw_emp_length_summary`, `vw_home_ownership_summary`). Load 38,576 records into `data/processed/bank_loans.db`.
  - **Status**: Completed.

---

### Phase 3: SQL Analytics, KPI Engine & Consistency Testing
- [x] **Task 3.1: SQL KPI Script Development**
  - **Priority**: High
  - **Relevant Files**: [sql/kpi_queries.sql](file:///c:/Bank_loan_risk_analysis/sql/kpi_queries.sql)
  - **Acceptance Criteria**: SQL queries for Total Applications (38,576), Total Funded Amount ($435.76M), Total Amount Received ($473.07M), Avg Interest Rate (12.05%), Avg DTI (13.33%), Good Loans (86.18%), Bad Loans (13.82%), MTD (Dec 2021), PMTD (Nov 2021), and MoM growth.
  - **Status**: Completed.

- [x] **Task 3.2: Analytical KPI Engine Implementation**
  - **Priority**: High
  - **Relevant Files**: [src/analytics/kpi_engine.py](file:///c:/Bank_loan_risk_analysis/src/analytics/kpi_engine.py)
  - **Acceptance Criteria**: Methods for summary KPIs, period KPIs, MoM growth calculations, and Good vs Bad loan portfolio metrics supporting both Pandas DataFrames and SQL query inputs.
  - **Status**: Completed.

- [x] **Task 3.3: SQL vs Pandas Cross-Validation Unit Testing**
  - **Priority**: High
  - **Relevant Files**: [tests/test_kpi_consistency.py](file:///c:/Bank_loan_risk_analysis/tests/test_kpi_consistency.py)
  - **Acceptance Criteria**: PyTest assertions demonstrating zero numerical discrepancy between SQLite query aggregations and Pandas calculations.
  - **Status**: Completed (All 6 KPI consistency tests passed).

---

### Phase 4: Machine Learning Credit Risk Intelligence Engine & Evaluation
- [x] **Task 4.1: Target Mapping & Target Leakage Prevention**
  - **Priority**: High
  - **Relevant Files**: [src/ml/feature_engineering.py](file:///c:/Bank_loan_risk_analysis/src/ml/feature_engineering.py)
  - **Acceptance Criteria**: Define binary target `target_default` (Positive Class `1` = `Charged Off`, Negative Class `0` = `Fully Paid`). Exclude 1,098 active `Current` loans from training universe (37,478 completed historical loans). Enforce pre-origination feature allowlist (12 features) and prohibit post-outcome servicing fields (`total_payment`, `installment`, `last_payment_date`, etc.).
  - **Status**: Completed.

- [x] **Task 4.2: Candidate Model Training & Comparison**
  - **Priority**: High
  - **Relevant Files**: [src/ml/train_model.py](file:///c:/Bank_loan_risk_analysis/src/ml/train_model.py), [src/ml/evaluate_model.py](file:///c:/Bank_loan_risk_analysis/src/ml/evaluate_model.py)
  - **Acceptance Criteria**: Train Baseline Logistic Regression (`class_weight='balanced'`, `random_state=42`) and Challenger Random Forest (`n_estimators=100`) using 80/20 stratified split. Selected Logistic Regression (Test ROC-AUC = 0.6953, Recall = 65.23%). Serialize versioned joblib pipeline and metadata.
  - **Status**: Completed.

- [x] **Task 4.3: Real-Time & Batch Risk Scoring Engine**
  - **Priority**: High
  - **Relevant Files**: [src/ml/risk_scoring.py](file:///c:/Bank_loan_risk_analysis/src/ml/risk_scoring.py)
  - **Acceptance Criteria**: Implement `CreditRiskScoringEngine` supporting single-record dict scoring (`score_record`) and batch DataFrame scoring (`score_batch`). Categorize default probability into documented risk tiers: `Low Risk` (<0.15), `Medium Risk` (0.15–0.35), `High Risk` (>=0.35).
  - **Status**: Completed.

---

### Phase 5: Streamlit Interactive UI Pages & Visualizations
- [x] **Task 5.1: Custom Banking CSS & UI Components**
  - **Priority**: High
  - **Relevant Files**: [src/ui/components.py](file:///c:/Bank_loan_risk_analysis/src/ui/components.py)
  - **Acceptance Criteria**: Banking dark theme CSS (`BANKING_CSS`), reusable KPI metric cards (`render_kpi_card`) with MTD and MoM trend badges, Good/Bad standing health cards (`render_standing_card`), and Plotly chart generators.
  - **Status**: Completed.

- [x] **Task 5.2: Multi-Page Views Implementation**
  - **Priority**: High
  - **Relevant Files**: [src/ui/views/summary.py](file:///c:/Bank_loan_risk_analysis/src/ui/views/summary.py), [src/ui/views/overview.py](file:///c:/Bank_loan_risk_analysis/src/ui/views/overview.py), [src/ui/views/details.py](file:///c:/Bank_loan_risk_analysis/src/ui/views/details.py), [src/ui/views/risk_intelligence.py](file:///c:/Bank_loan_risk_analysis/src/ui/views/risk_intelligence.py)
  - **Acceptance Criteria**: 4 pages (Executive Summary, Loan Overview with 4 breakdown tabs, Detailed Records with search & CSV export, Risk Intelligence with applicant simulator, model feature drivers, and batch scoring).
  - **Status**: Completed.

- [x] **Task 5.3: Main Application Entrypoint & Sidebar Router**
  - **Priority**: High
  - **Relevant Files**: [app.py](file:///c:/Bank_loan_risk_analysis/app.py)
  - **Acceptance Criteria**: Page navigation radio selector, global filter controls (State, Status, Grade, Purpose), and cached dataset loader `@st.cache_data`.
  - **Status**: Completed.

---

### Phase 6: Production Readiness & System Integration Verification
- [x] **Task 6.1: Model Explainability & Feature Drivers Extraction**
  - **Priority**: Medium
  - **Relevant Files**: [src/ml/evaluate_model.py](file:///c:/Bank_loan_risk_analysis/src/ml/evaluate_model.py), [src/ml/risk_scoring.py](file:///c:/Bank_loan_risk_analysis/src/ml/risk_scoring.py), [src/ui/views/risk_intelligence.py](file:///c:/Bank_loan_risk_analysis/src/ui/views/risk_intelligence.py)
  - **Acceptance Criteria**: Implement `get_feature_importances()` to extract top Logistic Regression coefficients (`int_rate`, `purpose_small_business`, `address_state_WY`, etc.) and display them in the Risk Intelligence dashboard page.
  - **Status**: Completed.

- [x] **Task 6.2: System Integration Test Suite**
  - **Priority**: High
  - **Relevant Files**: [tests/test_phase6_integration.py](file:///c:/Bank_loan_risk_analysis/tests/test_phase6_integration.py)
  - **Acceptance Criteria**: Integration tests covering model explainability extraction, unseen categorical value inference, database connection lifecycle cleanup, and Streamlit view function execution.
  - **Status**: Completed (37/37 PyTest unit and integration tests passing).

---

### Phase 7: GitHub Repository Preparation & Security Hardening
- [x] **Task 7.1: `.gitignore` Audit & Security Hardening**
  - **Priority**: High
  - **Relevant Files**: [.gitignore](file:///c:/Bank_loan_risk_analysis/.gitignore)
  - **Acceptance Criteria**: Audited repository for hardcoded secrets, API keys, credentials (0 found). Created `.gitignore` excluding Python bytecode (`__pycache__/`, `*.pyc`), pytest caches (`.pytest_cache/`), virtual environments (`venv/`, `.venv/`), local environment files (`.env`), and temporary logs. Verified file sizes: model artifact is `6.8 KB` and cleaned CSV is `10.44 MB` (both well below GitHub's 100 MB file limit; Git LFS is NOT required).
  - **Status**: Completed.

- [x] **Task 7.2: Git Initialization & Initial Commit**
  - **Priority**: High
  - **Relevant Files**: `.git/`, [task.md](file:///c:/Bank_loan_risk_analysis/task.md)
  - **Acceptance Criteria**: Initialized Git repository locally (`git init`), set branch to `main`, staged 51 tracked project files, verified no secret leakage, and created initial commit (`6b1099a65fcd8f96c51075e161994b9d3913a8a3`).
  - **Status**: Completed.

- [ ] **Task 7.3: Streamlit Configuration (`.streamlit/config.toml`) Setup**
  - **Priority**: Medium
  - **Relevant Files**: `.streamlit/config.toml` [NEW]
  - **Acceptance Criteria**: Define corporate dark theme, primary accent color (`#3182ce`), background colors, and headless mode settings for cloud deployment.
  - **Dependencies**: Task 7.2.

- [x] **Task 7.4: GitHub Remote Repository Push & Deployment**
  - **Priority**: High
  - **Relevant Files**: Remote GitHub Repository URL (`https://github.com/draxx2151/Bank_loan_risk_analysis.git`)
  - **Acceptance Criteria**: Connected local repository to GitHub remote (`git remote add origin ...`), verified 0 secrets in commit `6ba085b`, and pushed `main` branch to remote.
  - **Status**: Completed.
- [ ] **Task 8.1: Streamlit Configuration (`.streamlit/config.toml`) Setup**
  - **Priority**: Medium
  - **Relevant Files**: `.streamlit/config.toml` [NEW]
  - **Acceptance Criteria**: Define corporate dark theme, primary accent color (`#3182ce`), background colors, and headless mode settings for cloud deployment.
  - **Dependencies**: Phase 7.

- [ ] **Task 8.2: Streamlit Community Cloud App Deployment & Verification**
  - **Priority**: High
  - **Relevant Files**: GitHub Repository, Streamlit Community Cloud Console
  - **Acceptance Criteria**: Connect GitHub repository to Streamlit Community Cloud, deploy `app.py`, verify dataset loading from `data/processed/financial_loan_cleaned.csv`, verify SQLite database creation, verify model joblib deserialization, and confirm web dashboard rendering.
  - **Dependencies**: Task 8.1.

---

### Phase 9: Post-Deployment Monitoring & Operational Maintenance
- [ ] **Task 9.1: Live Application Sanity Check & Health Monitoring**
  - **Priority**: High
  - **Relevant Files**: Deployed Web Application URL
  - **Acceptance Criteria**: Perform smoke tests across all 4 pages on live web URL, verify filter interactivity, test CSV export download, test Risk Intelligence applicant scoring simulator, and confirm error-free execution.
  - **Dependencies**: Phase 8.

- [ ] **Task 9.2: Model Drift & Data Quality Audit Protocol**
  - **Priority**: Low
  - **Relevant Files**: [src/data_processing/validator.py](file:///c:/Bank_loan_risk_analysis/src/data_processing/validator.py), `docs/`
  - **Acceptance Criteria**: Establish periodic dataset drift audit routines and data quality re-validation protocols when updating loan datasets.
  - **Dependencies**: Task 9.1.

---

## 3. Current Incomplete Tasks & Next Recommended Step

| Phase | Task Description | Priority | Status |
|---|---|---|---|
| **Phase 7** | `.gitignore` Audit & Security Hardening | High | `[ ] Pending` |
| **Phase 7** | Git LFS / Artifact Tracking Setup | Medium | `[ ] Pending` |
| **Phase 8** | `.streamlit/config.toml` Theme Configuration | Medium | `[ ] Pending` |
| **Phase 8** | Streamlit Community Cloud Deployment | High | `[ ] Pending` |
| **Phase 9** | Post-Deployment Verification & Smoke Testing | High | `[ ] Pending` |

### Recommended Next Action
The highest-priority next task from the roadmap is **Phase 7, Task 7.1: `.gitignore` Audit & Security Hardening** to prepare the repository for GitHub version control and eventual Streamlit Community Cloud deployment.
