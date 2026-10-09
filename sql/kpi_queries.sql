-- ====================================================================
-- SQL KPI Queries for Bank Loan Analysis & Risk Intelligence Dashboard
-- Target Database: SQLite / MySQL Compatible
-- ====================================================================

-- 1. OVERALL SUMMARY KPIS
SELECT 
    COUNT(id) AS total_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS total_funded_amount,
    COALESCE(SUM(total_payment), 0) AS total_amount_received,
    COALESCE(AVG(int_rate), 0) AS avg_int_rate,
    COALESCE(AVG(dti), 0) AS avg_dti
FROM bank_loans;

-- 2. MONTH-TO-DATE (MTD) KPIS (Latest Month: Dec 2021)
SELECT 
    COUNT(id) AS mtd_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS mtd_funded_amount,
    COALESCE(SUM(total_payment), 0) AS mtd_amount_received,
    COALESCE(AVG(int_rate), 0) AS mtd_avg_int_rate,
    COALESCE(AVG(dti), 0) AS mtd_avg_dti
FROM bank_loans
WHERE strftime('%Y-%m', issue_date) = '2021-12';

-- 3. PREVIOUS MONTH-TO-DATE (PMTD) KPIS (Previous Month: Nov 2021)
SELECT 
    COUNT(id) AS pmtd_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS pmtd_funded_amount,
    COALESCE(SUM(total_payment), 0) AS pmtd_amount_received,
    COALESCE(AVG(int_rate), 0) AS pmtd_avg_int_rate,
    COALESCE(AVG(dti), 0) AS pmtd_avg_dti
FROM bank_loans
WHERE strftime('%Y-%m', issue_date) = '2021-11';

-- 4. GOOD LOANS SUMMARY (Fully Paid & Current)
SELECT 
    COUNT(id) AS good_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS good_loan_funded_amount,
    COALESCE(SUM(total_payment), 0) AS good_loan_received_amount,
    ROUND(COUNT(id) * 100.0 / NULLIF((SELECT COUNT(*) FROM bank_loans), 0), 2) AS good_loan_pct
FROM bank_loans
WHERE loan_status IN ('Fully Paid', 'Current');

-- 5. BAD LOANS SUMMARY (Charged Off)
SELECT 
    COUNT(id) AS bad_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS bad_loan_funded_amount,
    COALESCE(SUM(total_payment), 0) AS bad_loan_received_amount,
    ROUND(COUNT(id) * 100.0 / NULLIF((SELECT COUNT(*) FROM bank_loans), 0), 2) AS bad_loan_pct
FROM bank_loans
WHERE loan_status = 'Charged Off';

-- 6. LOAN STATUS OVERVIEW GRID
SELECT 
    loan_status,
    COUNT(id) AS total_loan_applications,
    COALESCE(SUM(loan_amount), 0) AS total_funded_amount,
    COALESCE(SUM(total_payment), 0) AS total_amount_received,
    COALESCE(SUM(CASE WHEN strftime('%Y-%m', issue_date) = '2021-12' THEN loan_amount ELSE 0 END), 0) AS mtd_funded_amount,
    COALESCE(SUM(CASE WHEN strftime('%Y-%m', issue_date) = '2021-12' THEN total_payment ELSE 0 END), 0) AS mtd_amount_received,
    COALESCE(AVG(int_rate), 0) AS avg_int_rate,
    COALESCE(AVG(dti), 0) AS avg_dti
FROM bank_loans
GROUP BY loan_status
ORDER BY total_loan_applications DESC;
