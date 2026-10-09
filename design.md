# Product Design & User Experience Specification

**Project Name:** AI-Assisted Bank Loan Analysis and Risk Intelligence Dashboard  
**Application File:** [app.py](file:///c:/Bank_loan_risk_analysis/app.py)  
**UI Modules:** [src/ui/components.py](file:///c:/Bank_loan_risk_analysis/src/ui/components.py), [src/ui/views/](file:///c:/Bank_loan_risk_analysis/src/ui/views/)  

---

## 1. Product Vision & Target Audience

### Product Vision
The **AI-Assisted Bank Loan Analysis & Risk Intelligence Dashboard** provides an executive-grade, interactive analytics portal for financial bank management. It unifies high-level financial KPI monitoring, portfolio health tracking (Good Standing vs Bad Standing), multi-dimensional demographic analytics, and machine-learning credit risk scoring into a single, intuitive web interface.

### Target Users & Primary Job Roles
1. **Bank Managers & Executives**: Require top-level visibility into total loan applications, funded amounts, collection recoveries, and Month-over-Month (MoM) growth metrics to guide strategic financial planning.
2. **Financial & Risk Analysts**: Require multi-dimensional portfolio breakdowns across US State geography, risk grades, loan terms, and borrower purposes to evaluate credit risk exposure.
3. **Loan Underwriters & Credit Officers**: Require interactive credit risk simulation tools to evaluate applicant default probabilities, inspect model feature drivers, and make informed underwriting decisions.

---

## 2. Primary Use Cases

| Use Case ID | Job Role | Action / Workflow | Intended Outcome |
|---|---|---|---|
| **UC-01** | Bank Manager | Review Executive Summary KPI Cards & Standing Ratios | Assess overall portfolio volume, MTD funding, collection rate, and Good vs Bad standing ratios. |
| **UC-02** | Risk Analyst | Explore Loan Overview Tabs (Time, Map, Demographics) | Identify regional risk concentrations, high-default borrower categories, and term distributions. |
| **UC-03** | Credit Officer | Search & Export Detailed Records | Filter loan records by state/status/grade, search by borrower ID/job title, and download CSV report. |
| **UC-04** | Underwriter | Simulate Applicant Default Risk in Risk Intelligence | Input applicant terms (loan amount, income, DTI, rate, state), calculate default probability, and review risk tier. |
| **UC-05** | Risk Manager | Perform Portfolio Batch Risk Scoring | Run batch model inference across filtered loan records to evaluate portfolio probability distribution. |

---

## 3. Dashboard Navigation & Page Structure

The application adopts a clean, multi-page layout navigated via the global Streamlit sidebar radio selector:

```
[Main Entrypoint: app.py]
  │
  ├── Sidebar Navigation & Global Filter Controls
  │
  ├── Page 1: 📌 Executive Summary (src/ui/views/summary.py)
  ├── Page 2: 📈 Loan Overview (src/ui/views/overview.py)
  ├── Page 3: 📄 Detailed Loan Records (src/ui/views/details.py)
  └── Page 4: 🤖 Risk Intelligence (src/ui/views/risk_intelligence.py)
```

### Global Sidebar Filter Controls
Located persistently on the left sidebar:
- **Navigation Page Selector**: Radio buttons for switching views.
- **US State Filter**: Multiselect list of 50 US state codes (`CA`, `NY`, `TX`, `FL`, etc.).
- **Loan Status Filter**: Multiselect list of loan statuses (`Fully Paid`, `Charged Off`, `Current`).
- **Risk Grade Filter**: Multiselect list of bank risk grades (`A` to `G`).
- **Loan Purpose Filter**: Multiselect list of borrower purposes (`debt_consolidation`, `credit_card`, `car`, etc.).
- **Filtered Record Counter**: Displays live sample count (e.g. `Filtered Universe: 38,576 of 38,576 loans`).

---

## 4. Visual Design & Theme System

### Corporate Dark Banking Theme (`BANKING_CSS`)
Implemented in [src/ui/components.py](file:///c:/Bank_loan_risk_analysis/src/ui/components.py) using custom injected CSS:
- **Background Color**: Deep dark slate (`#0e1117`).
- **Card Gradient Containers**: High-contrast glassmorphism linear gradients (`linear-gradient(135deg, #1e2530 0%, #161b22 100%)`) with subtle hover elevation (`translateY(-2px)`).
- **Typography**: Clean sans-serif system fonts with uppercase section titles (`#a0aec0`) and bold white numerical callouts (`#ffffff`).
- **Color Palette**:
  - **Primary Corporate Accent**: Steel Blue (`#3182ce`).
  - **Positive Trend / Good Standing**: Emerald Green (`#48bb78` / `#38a169`).
  - **Negative Trend / Bad Standing**: Crimson Red (`#f56565` / `#e53e3e`).
  - **Medium Risk / Secondary Accent**: Warm Amber (`#ecc94b`) / Purple (`#805ad5`).

---

## 5. Detailed Page Specifications

### Page 1: Executive Summary ([src/ui/views/summary.py](file:///c:/Bank_loan_risk_analysis/src/ui/views/summary.py))
- **Top 5 KPI Metric Cards**:
  1. *Total Loan Applications*: Count (`38,576`), Dec 2021 MTD (`4,314`), MoM Growth (`+6.91%`).
  2. *Total Funded Amount*: Currency (`$435.76M`), Dec 2021 MTD (`$53.98M`), MoM Growth (`+13.04%`).
  3. *Total Amount Received*: Currency (`$473.07M`), Dec 2021 MTD (`$58.07M`), MoM Growth (`+15.84%`).
  4. *Average Interest Rate*: Percentage (`12.05%`), Dec 2021 MTD (`12.36%`), MoM Growth (`+3.51%`).
  5. *Average DTI Ratio*: Percentage (`13.33%`), Dec 2021 MTD (`13.67%`), MoM Growth (`+2.77%`).
- **Good Standing vs Bad Standing Cards**:
  - *Good Standing Card* (Green border): `33,243` loans (`86.2%` of total), `$370.22M` funded, `$435.79M` received.
  - *Bad Standing Card* (Red border): `5,333` loans (`13.8%` of total), `$65.53M` funded, `$37.28M` received.
- **Status Breakdown Table Grid**: Aggregated table showing Total Applications, Total Funded, Total Received, MTD Funded, MTD Received, Avg Int Rate, and Avg DTI grouped by `loan_status`.

### Page 2: Loan Overview ([src/ui/views/overview.py](file:///c:/Bank_loan_risk_analysis/src/ui/views/overview.py))
Organized into 4 interactive breakdown tabs:
- **Tab 1: Monthly Trends**: Dual-axis Plotly chart displaying Total Funded Amount ($M bars) and Loan Applications (gold line) across all 12 months of 2021.
- **Tab 2: Regional Geography**: Interactive Plotly US State Choropleth Map shading states by application volume (California, New York, Texas, Florida lead).
- **Tab 3: Purpose & Demographics**: Horizontal bar chart of loan applications by stated purpose (`Debt consolidation`: 18,214, `Credit card`: 4,998) and employment length distribution.
- **Tab 4: Grade & Term Ratios**: Donut chart of loan terms (`36 months`: 73.2% vs `60 months`: 26.8%) and risk grade bar chart (`A` to `G`).

### Page 3: Detailed Loan Records ([src/ui/views/details.py](file:///c:/Bank_loan_risk_analysis/src/ui/views/details.py))
- **Interactive Quick Search Bar**: `st.text_input` allowing real-time filtering by borrower ID, state code, purpose, or employer title.
- **Filtered Metrics Header**: Displays filtered record count, total funded sum, and total received sum.
- **Data Table Grid**: Interactive `st.dataframe` showing 13 core attributes (`id`, `issue_date`, `address_state`, `emp_length`, `grade`, `home_ownership`, `loan_status`, `purpose`, `loan_amount`, `int_rate`, `dti`, `annual_income`, `total_payment`).
- **CSV Download Button**: `st.download_button` allowing users to export filtered records as `bank_loan_records_filtered.csv`.

### Page 4: Risk Intelligence ([src/ui/views/risk_intelligence.py](file:///c:/Bank_loan_risk_analysis/src/ui/views/risk_intelligence.py))
- **Model Information Header**: Displays active model status: Logistic Regression Pipeline (v1.0.0), Test ROC-AUC = `0.6953`, Test Recall = `65.23%`.
- **Tab 1: Single Application Simulator**:
  - Applicant Form: 12 underwriting input fields (Loan Amount, Income, DTI %, Int Rate %, Term, Grade, Home Ownership, Employment Years, Purpose, State, Verification Status, Credit Lines).
  - Risk Probability Gauge: Interactive Plotly gauge chart (0% to 100%) with green/amber/red threshold zones.
  - Risk Category Banner:
    - `Low Risk` (< 15% default probability): Green banner, Standard Underwriting Approval.
    - `Medium Risk` (15% - 35% default probability): Amber banner, Manual Underwriting Review Required.
    - `High Risk` (>= 35% default probability): Red banner, High Adverse Risk Flag.
  - **Model Feature Drivers Table**: Displays top global Logistic Regression coefficients (`int_rate` +0.4814, `purpose_small_business` +0.6865, etc.) for explainability.
- **Tab 2: Portfolio Batch Risk Distribution**: Scores all currently filtered records in batch mode and displays risk category counts and a default probability histogram.

---

## 6. Error States, Input Validation & Underwriting Disclaimers

### Input Validation & Edge-Case Handling
- **Missing Required Fields**: `CreditRiskScoringEngine.score_record()` validates all 12 allowlist features; returns `status: "MISSING_REQUIRED_FIELDS"` if an attribute is omitted.
- **Target Leakage Safeguard**: If post-outcome fields (`total_payment`, `last_payment_date`, etc.) are passed, the scoring engine ignores them and logs a non-fatal warning.
- **Unseen Categorical Values**: The preprocessor uses `OneHotEncoder(handle_unknown='ignore')`, ensuring unseen states or purposes score safely without runtime exceptions.
- **Empty Dataset Protection**: All KPI engine functions and chart generators check `df.empty` and return zeroed default structures.

### Underwriting & Academic Disclaimers
Displayed prominently in the UI:
> 🔒 **Underwriting Disclaimer**: Model default risk estimates represent statistical associations learned from historical consumer loan performance data. They are designed for academic decision support and experimental risk analysis, not for live automated credit rejection or binding lending decisions.

---

## 7. Usability Recommendations & Proposed Enhancements

### Existing Design Strengths (Verified)
- Clean, uncluttered dark theme layout with distinct visual hierarchy.
- Consistent number formatting across all views (e.g. `$435.76M`, `12.05%`, `+6.91% MoM`).
- Universal sidebar filters synchronized across all 4 pages.

### Proposed Future Enhancements (Unimplemented)
1. **Interactive What-If Sensitivity Sliders**: Allow underwriters to dynamically slide interest rate or DTI in real-time and observe probability gauge movement.
2. **Local Feature Contribution Waterfall Chart**: Implement SHAP or local coefficient contribution charts for individual single-record predictions.
3. **Dark/Light Theme Toggle**: Allow users to toggle between corporate dark mode and classic light banking theme.
