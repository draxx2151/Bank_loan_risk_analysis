"""
Data Validation Module
Provides comprehensive schema validation, data quality checks, and reporting.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from src.config import EXPECTED_COLUMNS, NUMERIC_COLUMNS

class DataValidationError(Exception):
    """Custom exception raised when critical data validation checks fail."""
    pass

def validate_bank_loan_data(df: pd.DataFrame, strict: bool = False) -> Dict[str, Any]:
    """
    Validates the bank loan DataFrame against expected schema, integrity rules, and bounds.
    Returns a data quality report dictionary.
    """
    errors: List[str] = []
    warnings: List[str] = []
    
    total_records = len(df)
    if total_records == 0:
        errors.append("Dataset is empty (0 records).")
    
    # 1. Column Presence Check
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")

    # 2. Duplicate ID Check
    duplicate_ids = 0
    if 'id' in df.columns:
        duplicate_ids = df['id'].duplicated().sum()
        if duplicate_ids > 0:
            errors.append(f"Found {duplicate_ids} duplicate loan IDs.")

    # 3. Numeric Bounds & Negative Values Check
    negative_counts = {}
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            neg_count = (df[col] < 0).sum()
            if neg_count > 0:
                negative_counts[col] = int(neg_count)
                warnings.append(f"Column '{col}' has {neg_count} negative values.")

    # 4. Valid Loan Status Check
    expected_statuses = {'Fully Paid', 'Charged Off', 'Current'}
    invalid_statuses = []
    if 'loan_status' in df.columns:
        actual_statuses = set(df['loan_status'].dropna().unique())
        invalid_statuses = list(actual_statuses - expected_statuses)
        if invalid_statuses:
            warnings.append(f"Unexpected loan statuses found: {invalid_statuses}")

    # 5. Null Value Checks for Mandatory Identifiers
    null_ids = 0
    if 'id' in df.columns:
        null_ids = df['id'].isnull().sum()
        if null_ids > 0:
            errors.append(f"Column 'id' has {null_ids} NULL values.")

    # Calculate Data Quality Score (0 to 100)
    penalty = (len(errors) * 25) + (len(warnings) * 5)
    quality_score = max(0.0, float(100 - penalty))

    is_valid = len(errors) == 0

    report = {
        "is_valid": is_valid,
        "total_records": total_records,
        "missing_columns": missing_cols,
        "duplicate_ids": int(duplicate_ids),
        "negative_numeric_counts": negative_counts,
        "invalid_statuses": invalid_statuses,
        "data_quality_score": quality_score,
        "errors": errors,
        "warnings": warnings
    }

    if strict and not is_valid:
        raise DataValidationError(f"Data validation failed with errors: {'; '.join(errors)}")

    return report
