"""
Unit Tests for Data Validator Module
"""

import pandas as pd
import pytest
from src.data_processing.validator import validate_bank_loan_data, DataValidationError
from src.config import EXPECTED_COLUMNS

def test_validate_bank_loan_data_valid():
    valid_data = {col: [1] for col in EXPECTED_COLUMNS}
    valid_data["loan_status"] = ["Fully Paid"]
    valid_data["dti"] = [0.15]
    valid_data["loan_amount"] = [10000]
    df = pd.DataFrame(valid_data)

    report = validate_bank_loan_data(df)
    assert report["is_valid"] == True
    assert report["data_quality_score"] == 100.0
    assert len(report["errors"]) == 0

def test_validate_missing_columns():
    df = pd.DataFrame({"id": [1, 2], "loan_amount": [1000, 2000]})
    report = validate_bank_loan_data(df)
    assert report["is_valid"] == False
    assert len(report["missing_columns"]) > 0

def test_validate_duplicate_ids():
    valid_data = {col: [1, 1] for col in EXPECTED_COLUMNS}
    df = pd.DataFrame(valid_data)
    report = validate_bank_loan_data(df)
    assert report["duplicate_ids"] == 1
    assert "Found 1 duplicate loan IDs." in report["errors"]

def test_validate_negative_numeric_bounds():
    valid_data = {col: [1] for col in EXPECTED_COLUMNS}
    valid_data["loan_amount"] = [-500]  # Invalid negative amount
    df = pd.DataFrame(valid_data)
    report = validate_bank_loan_data(df)
    assert "loan_amount" in report["negative_numeric_counts"]

def test_validate_strict_mode_raises():
    df = pd.DataFrame({"invalid_col": [1]})
    with pytest.raises(DataValidationError):
        validate_bank_loan_data(df, strict=True)
