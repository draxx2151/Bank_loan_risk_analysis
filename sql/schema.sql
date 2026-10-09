-- Bank Loans Table DDL (SQLite / MySQL Compatible)

CREATE TABLE IF NOT EXISTS bank_loans (
    id INTEGER PRIMARY KEY,
    member_id INTEGER NOT NULL,
    address_state VARCHAR(2),
    States VARCHAR(50),
    application_type VARCHAR(20),
    emp_length VARCHAR(20),
    emp_length_years REAL,
    emp_title VARCHAR(150),
    grade VARCHAR(5),
    sub_grade VARCHAR(5),
    home_ownership VARCHAR(20),
    issue_date DATE,
    last_credit_pull_date DATE,
    last_payment_date DATE,
    next_payment_date DATE,
    loan_status VARCHAR(20),
    loan_standing VARCHAR(20),
    is_good_loan BOOLEAN,
    purpose VARCHAR(50),
    term VARCHAR(20),
    term_months INTEGER,
    verification_status VARCHAR(30),
    annual_income REAL,
    dti REAL,
    installment REAL,
    int_rate REAL,
    loan_amount REAL,
    total_acc INTEGER,
    total_payment REAL
);

-- Indexes for fast KPI aggregations
CREATE INDEX IF NOT EXISTS idx_loan_status ON bank_loans(loan_status);
CREATE INDEX IF NOT EXISTS idx_issue_date ON bank_loans(issue_date);
CREATE INDEX IF NOT EXISTS idx_address_state ON bank_loans(address_state);
CREATE INDEX IF NOT EXISTS idx_grade ON bank_loans(grade);
