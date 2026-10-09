"""
Data Cleaning Module
Provides functional, reproducible cleaning routines for the Bank Loan dataset.
"""

import re
import pandas as pd
import numpy as np
from src.config import US_STATE_MAP, DATE_COLUMNS

def parse_emp_length_years(emp_len_str) -> float:
    """Converts employment length strings (e.g. '< 1 year', '10+ years') into numeric years."""
    if pd.isna(emp_len_str) or not isinstance(emp_len_str, str):
        return np.nan
    s = emp_len_str.strip().lower()
    if '< 1' in s or 'less' in s:
        return 0.0
    if '10+' in s:
        return 10.0
    match = re.search(r'\d+', s)
    if match:
        return float(match.group())
    return np.nan

def parse_term_months(term_str) -> int:
    """Converts term string (e.g. ' 36 months', '60 months') into integer months."""
    if pd.isna(term_str) or not isinstance(term_str, str):
        return np.nan
    match = re.search(r'\d+', term_str.strip())
    if match:
        return int(match.group())
    return np.nan

def clean_bank_loan_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw bank loan dataset:
    - Parses dates from dd-mm-yyyy to ISO format YYYY-MM-DD.
    - Imputes missing state names from 2-letter address_state codes using US_STATE_MAP.
    - Fills missing emp_title with 'Unspecified'.
    - Extracts numeric term_months and emp_length_years.
    - Strips whitespace from string columns.
    - Adds derived helper fields: is_good_loan, loan_standing.
    - Preserves 100% of input rows (no arbitrary drops).
    """
    cleaned = df.copy()

    # 1. Clean String Whitespace
    str_cols = cleaned.select_dtypes(include=['object', 'string']).columns
    for col in str_cols:
        cleaned[col] = cleaned[col].astype(str).str.strip()

    # 2. State Name Imputation
    if 'address_state' in cleaned.columns:
        cleaned['address_state'] = cleaned['address_state'].str.upper()
        # Derive full state name from lookup map where States is missing/nan/'nan'
        derived_states = cleaned['address_state'].map(US_STATE_MAP)
        cleaned['States'] = cleaned['States'].replace({'nan': np.nan, 'None': np.nan, '': np.nan})
        cleaned['States'] = cleaned['States'].fillna(derived_states)

    # 3. Handle missing emp_title
    if 'emp_title' in cleaned.columns:
        cleaned['emp_title'] = cleaned['emp_title'].replace({'nan': 'Unspecified', 'None': 'Unspecified', '': 'Unspecified'})
        cleaned['emp_title'] = cleaned['emp_title'].fillna('Unspecified')

    # 4. Parse Dates to YYYY-MM-DD ISO strings & datetime
    for date_col in DATE_COLUMNS:
        if date_col in cleaned.columns:
            # Handle potential nan strings
            cleaned[date_col] = cleaned[date_col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})
            dt_series = pd.to_datetime(cleaned[date_col], format='%d-%m-%Y', errors='coerce')
            cleaned[f'{date_col}_dt'] = dt_series
            cleaned[date_col] = dt_series.dt.strftime('%Y-%m-%d')

    # 5. Extract Numeric Representations
    if 'term' in cleaned.columns:
        cleaned['term_months'] = cleaned['term'].apply(parse_term_months)

    if 'emp_length' in cleaned.columns:
        cleaned['emp_length_years'] = cleaned['emp_length'].apply(parse_emp_length_years)

    # 6. Derived Standing Categories
    if 'loan_status' in cleaned.columns:
        good_statuses = ['Fully Paid', 'Current']
        cleaned['is_good_loan'] = cleaned['loan_status'].isin(good_statuses)
        cleaned['loan_standing'] = np.where(cleaned['is_good_loan'], 'Good Standing', 'Bad Standing')

    return cleaned
