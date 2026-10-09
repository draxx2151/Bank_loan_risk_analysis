"""
Unit Tests for Database Manager Module
"""

import sqlite3
import tempfile
from pathlib import Path
import pandas as pd
import pytest
from src.database.db_manager import DatabaseManager, DatabaseError
from src.data_processing.cleaner import clean_bank_loan_data

@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = Path(tmp.name)
    db_mgr = DatabaseManager(db_path)
    db_mgr.initialize_schema()
    yield db_mgr
    # Teardown
    if db_path.exists():
        try:
            db_path.unlink()
        except OSError:
            pass

def test_db_initialization(temp_db):
    assert temp_db.db_path.exists()
    df = temp_db.execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name='bank_loans';")
    assert not df.empty
    assert df.iloc[0]["name"] == "bank_loans"

def test_db_bulk_load(temp_db):
    sample_data = {
        "id": [1, 2],
        "member_id": [101, 102],
        "address_state": ["GA", "CA"],
        "States": ["Georgia", "California"],
        "application_type": ["INDIVIDUAL", "INDIVIDUAL"],
        "emp_length": ["< 1 year", "10+ years"],
        "emp_length_years": [0.0, 10.0],
        "emp_title": ["Ryder", "Engineer"],
        "grade": ["C", "E"],
        "sub_grade": ["C4", "E1"],
        "home_ownership": ["RENT", "RENT"],
        "issue_date": ["2021-02-11", "2021-01-01"],
        "last_credit_pull_date": ["2021-09-13", "2021-12-14"],
        "last_payment_date": ["2021-04-13", "2021-01-15"],
        "next_payment_date": ["2021-05-13", "2021-02-15"],
        "loan_status": ["Charged Off", "Fully Paid"],
        "loan_standing": ["Bad Standing", "Good Standing"],
        "is_good_loan": [False, True],
        "purpose": ["car", "car"],
        "term": ["36 months", "60 months"],
        "term_months": [36, 60],
        "verification_status": ["Source Verified", "Source Verified"],
        "annual_income": [30000.0, 48000.0],
        "dti": [0.01, 0.0535],
        "installment": [59.83, 109.43],
        "int_rate": [0.1527, 0.1864],
        "loan_amount": [2500.0, 3000.0],
        "total_acc": [4, 4],
        "total_payment": [1009.0, 3939.0]
    }
    df = pd.DataFrame(sample_data)
    loaded_count = temp_db.load_cleaned_data(df)
    assert loaded_count == 2

    # Verify data contents
    res_df = temp_db.execute_query("SELECT loan_amount, loan_status FROM bank_loans ORDER BY id")
    assert len(res_df) == 2
    assert res_df.iloc[0]["loan_amount"] == 2500.0
    assert res_df.iloc[0]["loan_status"] == "Charged Off"

def test_db_execute_invalid_query(temp_db):
    with pytest.raises(DatabaseError):
        temp_db.execute_query("SELECT * FROM non_existent_table")

def test_db_load_empty_dataframe(temp_db):
    with pytest.raises(DatabaseError):
        temp_db.load_cleaned_data(pd.DataFrame())
