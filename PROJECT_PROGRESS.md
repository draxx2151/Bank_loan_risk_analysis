# Project Progress Log: AI-Assisted Bank Loan Analysis and Risk Intelligence Dashboard

---

## Chronological Progress Record

### [2026-10-09] - Phase 1: Initial Setup, Data Sourcing & Documentation
**Completed Tasks:**
- Inspected requirements and reference repository (`arnavchaturvedi17/Data-Analysis-Bank-Loan-Lending_Data_Analytics`).
- Created modular project directory layout separating raw data, processed data, SQL scripts, source code, UI views, tests, and documentation.
- Downloaded and verified authentic dataset `data/raw/financial_loan.csv` (38,576 loan application records, 25 columns).
- Created core documentation: `README.md`, `docs/Data_Dictionary.md`, `docs/Architecture.md`, `requirements.txt`, and `PROJECT_PROGRESS.md`.
- Drafted complete implementation plan (`implementation_plan.md`).

**Technical Decisions:**
- **Modular Design**: Structured code into `src/database`, `src/data_processing`, `src/analytics`, and `src/ui` to ensure clear separation of concerns.
- **Database Engine**: Selected SQLite as default zero-configuration database, with architecture abstracting SQL connections to allow plug-and-play MySQL integration via standard database interface.
- **Justified ML Model**: Selected Scikit-Learn Logistic Regression & Random Forest Classifier for loan default risk prediction, providing automated risk scoring to support credit underwriting.
- **Data Integrity**: Verified raw dataset contains 38,576 rows. Strictly mandated no synthetic, mock, or fake data generation.

---

### [2026-10-09] - Phase 2: Data Cleaning, Schema Validation & Database Layer (COMPLETED)
**Completed Tasks:**
- **Configuration & Constants**: Implemented `src/config.py` containing project paths, column definitions, numeric range limits, and a deterministic 50-state lookup map (`US_STATE_MAP`).
- **Data Cleaner Module**: Implemented `src/data_processing/cleaner.py`:
  - Standardized date attributes (`issue_date`, `last_payment_date`, `next_payment_date`, `last_credit_pull_date`) from `dd-mm-yyyy` string format to ISO `YYYY-MM-DD` and pandas datetime.
  - Imputed missing state names in `States` column (38,476 nulls) using 2-letter `address_state` codes mapped against `US_STATE_MAP`.
  - Filled missing employer titles in `emp_title` (1,438 nulls) with `'Unspecified'`.
  - Derived numeric attributes `term_months` (36, 60) and `emp_length_years` (0 to 10) while preserving raw text representations.
  - Derived loan health flags: `is_good_loan` (boolean) and `loan_standing` (`Good Standing` for Fully Paid/Current, `Bad Standing` for Charged Off).
  - Preserved 100% of input records (raw row count 38,576 == cleaned row count 38,576). Saved cleaned data to `data/processed/financial_loan_cleaned.csv`.
- **Data Validator Module**: Implemented `src/data_processing/validator.py`:
  - Enforced schema requirements, duplicate `id` detection, missing column checks, negative numeric value bounds, and loan status integrity.
  - Created automated data quality scoring and report dictionary.
- **Database Layer**:
  - Wrote SQL table DDL schema and indexes in `sql/schema.sql`.
  - Implemented `src/database/db_manager.py` with SQLite connection lifecycle, schema initialization, parameter sanitization, and bulk chunked loading (`to_sql` with chunksize=5000).
  - Created SQLite database `data/processed/bank_loans.db` and successfully loaded 38,576 cleaned records.
- **Automated Testing Suite**:
  - Implemented unit tests: `tests/test_cleaner.py`, `tests/test_validator.py`, and `tests/test_db.py`.
  - Executed `pytest -v` across 12 test cases with **100% pass rate** (12 passed in 0.74s).

---

### [2026-10-09] - Phase 3: SQL Analytics, KPI Engine & Consistency Testing (COMPLETED)
**Completed Tasks:**
- **SQL Analytics Script**: Wrote `sql/kpi_queries.sql` containing production-grade SQL queries for overall summary metrics, MTD (Dec 2021), PMTD (Nov 2021), Good vs Bad loan portfolio metrics, and loan status grid overview.
- **Analytical Database Views**: Wrote `sql/views.sql` and integrated `initialize_views()` into `DatabaseManager`:
  - `vw_monthly_trends`: Aggregations grouped by `issue_date` month.
  - `vw_state_summary`: Geographic regional metrics by US state.
  - `vw_purpose_summary`: Financial aggregations by borrower loan purpose.
  - `vw_grade_summary`: Risk grade aggregations (`A` to `G`).
  - `vw_term_summary`: Aggregations by loan term (36 vs 60 months).
  - `vw_emp_length_summary`: Aggregations by employment duration.
  - `vw_home_ownership_summary`: Aggregations by home ownership status (`RENT`, `MORTGAGE`, `OWN`).
- **Analytical KPI Engine**: Implemented `src/analytics/kpi_engine.py`:
  - Methods: `compute_summary_kpis()`, `compute_period_kpis()`, `compute_mom_growth()`, and `compute_good_vs_bad_kpis()`.
  - Full support for both Pandas DataFrames and SQLite SQL query results.
  - Protected against empty DataFrames, NaN inputs, and zero denominators.
- **Automated Consistency Testing**:
  - Created `tests/test_kpi_consistency.py` cross-validating SQL queries against Pandas calculations.
  - Verified **0 numeric discrepancy** across overall applications (38,576), total funded amount ($435,757,075), total received amount ($473,070,933), average interest rate (12.05%), average DTI (13.33%), MTD (Dec 2021: 4,314 apps), PMTD (Nov 2021: 4,035 apps), and Good vs Bad loan counts/funding.
  - Executed `pytest -v` across 18 test cases with **100% pass rate** (18 passed in 1.41s).

---

### [2026-10-09] - Phase 4: ML Credit Risk Intelligence Engine & Evaluation (COMPLETED)
**Completed Tasks:**
- **Feature Engineering & Leakage Prevention (`src/ml/feature_engineering.py`)**:
  - Defined strict pre-origination feature allowlist: `loan_amount`, `annual_income`, `dti`, `int_rate`, `emp_length_years`, `total_acc`, `term`, `grade`, `home_ownership`, `verification_status`, `purpose`, `address_state`.
  - Explicitly excluded all post-outcome servicing fields (`total_payment`, `installment`, `last_payment_date`, `next_payment_date`, `last_credit_pull_date`, `loan_status`, `is_good_loan`, `loan_standing`, `member_id`, `id`, `States`, `sub_grade`).
  - Implemented `prepare_ml_dataset()`: Mapped target `is_default` (Positive Class `1` = `Charged Off`, Negative Class `0` = `Fully Paid`). Excluded 1,098 active `Current` loans. Training universe: 37,478 historical completed loans.
  - Built scikit-learn `ColumnTransformer` preprocessor (`StandardScaler` for numeric, `OneHotEncoder(handle_unknown='ignore')` for categorical).
- **Model Training & Comparison (`src/ml/train_model.py`)**:
  - Split dataset 80/20 using stratified random sampling (`random_state=42`).
  - Trained Baseline Model: `LogisticRegression(class_weight='balanced', random_state=42)`.
  - Trained Challenger Model: `RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)`.
  - Selected Logistic Regression based on higher ROC-AUC (0.6953 vs 0.6945) and higher default Recall (65.23% vs 59.42%).
  - Saved versioned artifacts: `artifacts/models/credit_risk_pipeline_v1.0.0.joblib`, `artifacts/models/model_metadata.json`, `artifacts/metrics/evaluation_metrics.json`, and `artifacts/reports/model_evaluation_report.md`.
- **Model Evaluation Module (`src/ml/evaluate_model.py`)**:
  - Computed evaluation metrics on held-out test set: Accuracy (0.6443), Precision (0.2327), Recall (0.6523), F1-Score (0.3430), ROC-AUC (0.6953), PR-AUC (0.2709). Added `get_feature_importances()` for model explainability.
- **Credit Risk Scoring Engine (`src/ml/risk_scoring.py`)**:
  - Implemented `CreditRiskScoringEngine` supporting single-record dictionary scoring (`score_record`) and batch DataFrame scoring (`score_batch`).
  - Categorizes default probability `P(Default)` into documented risk tiers: Low Risk (<0.15), Medium Risk (0.15-0.35), High Risk (>=0.35).

---

### [2026-10-09] - Phase 5: Streamlit Interactive UI Pages & Visualizations (COMPLETED)
**Completed Tasks:**
- **UI Components & Custom Styling (`src/ui/components.py`)**:
  - Injected clean, professional banking dashboard dark theme CSS (`BANKING_CSS`).
  - Implemented reusable KPI metric cards (`render_kpi_card`) with MTD subtext and MoM percentage trend badges.
  - Implemented Good vs Bad loan portfolio standing cards (`render_standing_card`).
  - Created Plotly chart generators: `create_monthly_trends_chart`, `create_state_map_chart`, `create_purpose_chart`, `create_grade_chart`, `create_term_donut_chart`, and `create_risk_gauge_chart`.
- **Page Views Implementation (`src/ui/views/`)**:
  - `summary.py`: Executive Summary view displaying top 5 KPIs, MTD/MoM metrics, Good/Bad standing health cards, and status breakdown grid.
  - `overview.py`: Loan Overview view featuring 4 interactive tabs for Monthly Trends, Regional Geography (US Map), Purpose & Demographics, and Grade & Term ratios.
  - `details.py`: Filterable data grid table with real-time text search and a **Download Filtered Data to CSV** button (`st.download_button`).
  - `risk_intelligence.py`: AI Credit Risk Intelligence & Underwriting Simulator page with applicant parameter inputs, real-time default probability gauge, risk category assignment (`Low Risk`, `Medium Risk`, `High Risk`), underwriting recommendation banner, model feature importance table, and batch risk distribution analysis.
- **Main Entrypoint (`app.py`)**:
  - Implemented Streamlit entry point `app.py` featuring sidebar navigation radio, global filter controls (State, Loan Status, Risk Grade, Purpose), automatic filter state management, and page router.

---

### [2026-10-09] - Phase 6: Production Readiness, Integration Verification & Final Validation (COMPLETED)
**Completed Tasks:**
- **System-Wide Verification & Explainability**:
  - Verified trained ML pipeline artifact (`artifacts/models/credit_risk_pipeline_latest.joblib`) deserialization.
  - Added model explainability extraction (`get_feature_importances`) showing top predictive drivers (`int_rate`, `purpose_small_business`, `address_state_WY`, etc.).
  - Added `get_model_explainability()` display to Risk Intelligence dashboard page.
- **Integration Test Suite (`tests/test_phase6_integration.py`)**:
  - Added integration tests covering model explainability extraction, unseen categorical value inference, database connection lifecycle cleanup, and Streamlit view function invocation.
- **Full Test Suite Execution**:
  - Executed `pytest -v` across all **37 test cases** with **100% pass rate** (37 passed in 5.42s).

**Files Created / Modified:**
- `src/ml/evaluate_model.py` [UPDATED - added `get_feature_importances()`]
- `src/ml/risk_scoring.py` [UPDATED - added `get_model_explainability()`]
- `src/ui/views/risk_intelligence.py` [UPDATED - added feature drivers table]
- `tests/test_phase6_integration.py` [NEW]
- `PROJECT_PROGRESS.md` [UPDATED]

**Commands Executed:**
- `pytest -v` (Full test suite execution - 37 passed in 5.42s)
- `python -c "import app"` (App entry point validation)

**Test Results:**
```
============================= 37 passed in 5.42s ==============================
```

---

## 🏆 Project Completion & Verification Matrix

All 6 project phases are **100% complete, fully tested, and verified**:
- **Phase 1**: Initial Setup & Documentation (Completed)
- **Phase 2**: Data Cleaning, Schema Validation & Database Layer (Completed)
- **Phase 3**: SQL Analytics, KPI Engine & Consistency Testing (Completed)
- **Phase 4**: ML Credit Risk Intelligence Engine & Evaluation (Completed)
- **Phase 5**: Streamlit Interactive UI Pages & Visualizations (Completed)
- **Phase 6**: Production Readiness, Integration Verification & Final Validation (Completed)

---

## 🚀 How to Run the Dashboard Locally

1. **Launch Streamlit Dashboard**:
```powershell
streamlit run app.py
```

2. **Execute Full Automated Test Suite**:
```powershell
pytest -v
```
