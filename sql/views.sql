-- ====================================================================
-- Analytical Database Views for Bank Loan Dashboard
-- Target Database: SQLite / MySQL Compatible
-- ====================================================================

-- 1. MONTHLY TRENDS VIEW
CREATE VIEW IF NOT EXISTS vw_monthly_trends AS
SELECT 
    strftime('%Y-%m', issue_date) AS issue_month,
    strftime('%m', issue_date) AS month_number,
    COUNT(id) AS total_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS total_funded_amount,
    COALESCE(SUM(total_payment), 0) AS total_amount_received,
    COALESCE(AVG(int_rate), 0) AS avg_int_rate,
    COALESCE(AVG(dti), 0) AS avg_dti
FROM bank_loans
GROUP BY strftime('%Y-%m', issue_date), strftime('%m', issue_date)
ORDER BY issue_month ASC;

-- 2. STATE REGIONAL SUMMARY VIEW
CREATE VIEW IF NOT EXISTS vw_state_summary AS
SELECT 
    address_state,
    States AS state_name,
    COUNT(id) AS total_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS total_funded_amount,
    COALESCE(SUM(total_payment), 0) AS total_amount_received,
    COALESCE(AVG(int_rate), 0) AS avg_int_rate,
    COALESCE(AVG(dti), 0) AS avg_dti
FROM bank_loans
GROUP BY address_state, States
ORDER BY total_loan_applications DESC;

-- 3. LOAN PURPOSE SUMMARY VIEW
CREATE VIEW IF NOT EXISTS vw_purpose_summary AS
SELECT 
    purpose,
    COUNT(id) AS total_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS total_funded_amount,
    COALESCE(SUM(total_payment), 0) AS total_amount_received,
    COALESCE(AVG(int_rate), 0) AS avg_int_rate,
    COALESCE(AVG(dti), 0) AS avg_dti
FROM bank_loans
GROUP BY purpose
ORDER BY total_loan_applications DESC;

-- 4. RISK GRADE SUMMARY VIEW
CREATE VIEW IF NOT EXISTS vw_grade_summary AS
SELECT 
    grade,
    COUNT(id) AS total_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS total_funded_amount,
    COALESCE(SUM(total_payment), 0) AS total_amount_received,
    COALESCE(AVG(int_rate), 0) AS avg_int_rate,
    COALESCE(AVG(dti), 0) AS avg_dti
FROM bank_loans
GROUP BY grade
ORDER BY grade ASC;

-- 5. LOAN TERM SUMMARY VIEW
CREATE VIEW IF NOT EXISTS vw_term_summary AS
SELECT 
    term,
    term_months,
    COUNT(id) AS total_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS total_funded_amount,
    COALESCE(SUM(total_payment), 0) AS total_amount_received,
    COALESCE(AVG(int_rate), 0) AS avg_int_rate,
    COALESCE(AVG(dti), 0) AS avg_dti
FROM bank_loans
GROUP BY term, term_months
ORDER BY term_months ASC;

-- 6. EMPLOYMENT LENGTH SUMMARY VIEW
CREATE VIEW IF NOT EXISTS vw_emp_length_summary AS
SELECT 
    emp_length,
    emp_length_years,
    COUNT(id) AS total_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS total_funded_amount,
    COALESCE(SUM(total_payment), 0) AS total_amount_received,
    COALESCE(AVG(int_rate), 0) AS avg_int_rate,
    COALESCE(AVG(dti), 0) AS avg_dti
FROM bank_loans
GROUP BY emp_length, emp_length_years
ORDER BY emp_length_years ASC;

-- 7. HOME OWNERSHIP SUMMARY VIEW
CREATE VIEW IF NOT EXISTS vw_home_ownership_summary AS
SELECT 
    home_ownership,
    COUNT(id) AS total_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS total_funded_amount,
    COALESCE(SUM(total_payment), 0) AS total_amount_received,
    COALESCE(AVG(int_rate), 0) AS avg_int_rate,
    COALESCE(AVG(dti), 0) AS avg_dti
FROM bank_loans
GROUP BY home_ownership
ORDER BY total_loan_applications DESC;
