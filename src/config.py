"""
Project Configuration File
Contains paths, constants, state lookup maps, and column schemas for the Bank Loan Analysis project.
"""

from pathlib import Path

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "financial_loan.csv"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CLEANED_DATA_PATH = PROCESSED_DATA_DIR / "financial_loan_cleaned.csv"
DEFAULT_DB_PATH = PROCESSED_DATA_DIR / "bank_loans.db"
SQL_DIR = BASE_DIR / "sql"
SCHEMA_SQL_PATH = SQL_DIR / "schema.sql"

# Verified Dataset Expected Columns
EXPECTED_COLUMNS = [
    "id", "States", "application_type", "emp_length", "emp_title", 
    "grade", "home_ownership", "issue_date", "last_credit_pull_date", 
    "last_payment_date", "loan_status", "next_payment_date", "member_id", 
    "purpose", "sub_grade", "term", "verification_status", "annual_income", 
    "dti", "installment", "int_rate", "loan_amount", "total_acc", 
    "total_payment", "address_state"
]

# Date columns in raw CSV
DATE_COLUMNS = ["issue_date", "last_credit_pull_date", "last_payment_date", "next_payment_date"]

# Numeric columns expecting non-negative values
NUMERIC_COLUMNS = [
    "loan_amount", "total_payment", "annual_income", 
    "dti", "installment", "int_rate", "total_acc"
]

# US State Code to Full Name Mapping
US_STATE_MAP = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
    "DC": "District of Columbia"
}
