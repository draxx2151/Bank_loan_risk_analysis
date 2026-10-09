"""
Unit Tests for Data Cleaner Module
"""

import pandas as pd
import numpy as np
import pytest
from src.data_processing.cleaner import (
    clean_bank_loan_data, 
    parse_term_months, 
    parse_emp_length_years
)

def test_parse_term_months():
    assert parse_term_months(" 36 months") == 36
    assert parse_term_months("60 months") == 60
    assert parse_term_months("invalid") is np.nan or np.isnan(parse_term_months("invalid"))
    assert np.isnan(parse_term_months(None))

def test_parse_emp_length_years():
    assert parse_emp_length_years("< 1 year") == 0.0
    assert parse_emp_length_years("10+ years") == 10.0
    assert parse_emp_length_years("5 years") == 5.0
    assert parse_emp_length_years("1 year") == 1.0
    assert np.isnan(parse_emp_length_years(None))

def test_clean_bank_loan_data_transformations():
    raw_data = {
        "id": [1, 2, 3],
        "member_id": [101, 102, 103],
        "address_state": ["GA", "CA", "TX"],
        "States": [np.nan, "California", None],
        "emp_title": [np.nan, "Software Engineer", ""],
        "emp_length": ["< 1 year", "10+ years", "4 years"],
        "term": [" 36 months", " 60 months", " 36 months"],
        "issue_date": ["11-02-2021", "01-01-2021", "25-02-2021"],
        "last_credit_pull_date": ["13-09-2021", "14-12-2021", "12-12-2021"],
        "last_payment_date": ["13-04-2021", "15-01-2021", "12-03-2021"],
        "next_payment_date": ["13-05-2021", "15-02-2021", "12-04-2021"],
        "loan_status": ["Charged Off", "Fully Paid", "Current"],
        "loan_amount": [2500, 3000, 4500]
    }
    df_raw = pd.DataFrame(raw_data)
    df_clean = clean_bank_loan_data(df_raw)

    # 1. Row Preservation
    assert len(df_clean) == len(df_raw)

    # 2. State Name Imputation
    assert df_clean.loc[0, "States"] == "Georgia"
    assert df_clean.loc[1, "States"] == "California"
    assert df_clean.loc[2, "States"] == "Texas"

    # 3. Missing Employer Title
    assert df_clean.loc[0, "emp_title"] == "Unspecified"
    assert df_clean.loc[1, "emp_title"] == "Software Engineer"
    assert df_clean.loc[2, "emp_title"] == "Unspecified"

    # 4. Date Parsing
    assert df_clean.loc[0, "issue_date"] == "2021-02-11"
    assert df_clean.loc[1, "issue_date"] == "2021-01-01"

    # 5. Numeric Terms and Emp Length
    assert df_clean.loc[0, "term_months"] == 36
    assert df_clean.loc[1, "term_months"] == 60
    assert df_clean.loc[0, "emp_length_years"] == 0.0
    assert df_clean.loc[1, "emp_length_years"] == 10.0

    # 6. Loan Standing Derivation
    assert df_clean.loc[0, "is_good_loan"] == False
    assert df_clean.loc[0, "loan_standing"] == "Bad Standing"
    assert df_clean.loc[1, "is_good_loan"] == True
    assert df_clean.loc[1, "loan_standing"] == "Good Standing"
    assert df_clean.loc[2, "is_good_loan"] == True
    assert df_clean.loc[2, "loan_standing"] == "Good Standing"
