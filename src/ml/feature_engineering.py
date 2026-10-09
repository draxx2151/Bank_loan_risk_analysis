"""
Feature Engineering & Target Definition Module
Handles prediction target mapping, target leakage prevention, feature allowlisting,
and scikit-learn preprocessing pipeline construction.
"""

from typing import Tuple, Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# -------------------------------------------------------------------------
# Feature Allowlist (Pre-Origination Underwriting Features Only)
# -------------------------------------------------------------------------
NUMERICAL_FEATURES: List[str] = [
    "loan_amount",
    "annual_income",
    "dti",
    "int_rate",
    "emp_length_years",
    "total_acc"
]

CATEGORICAL_FEATURES: List[str] = [
    "term",
    "grade",
    "home_ownership",
    "verification_status",
    "purpose",
    "address_state"
]

FEATURE_ALLOWLIST: List[str] = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

# -------------------------------------------------------------------------
# Leakage Exclusions & Rationale Documentation
# -------------------------------------------------------------------------
LEAKAGE_EXCLUSIONS: Dict[str, str] = {
    "total_payment": "Post-origination cumulative repayment amount; directly reflects repayment progress and outcome.",
    "installment": "Calculated after loan terms/rates are finalized and payment schedule is active.",
    "last_payment_date": "Post-origination servicing date; available only after loan is active.",
    "next_payment_date": "Post-origination servicing schedule date; available only after loan is active.",
    "last_credit_pull_date": "Post-origination credit monitoring date; updated throughout loan lifetime.",
    "loan_status": "Target variable itself (Fully Paid, Charged Off, Current).",
    "is_good_loan": "Direct derived target flag.",
    "loan_standing": "Direct derived target standing label.",
    "member_id": "Arbitrary borrower identifier; risk shortcut without underwriting substance.",
    "id": "Primary key identifier; arbitrary sequential ID.",
    "States": "Redundant state full name; replaced by address_state.",
    "sub_grade": "High-granularity sub-division of grade determined after full underwriting scoring."
}

def prepare_ml_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, Dict[str, Any]]:
    """
    Prepares the feature matrix X and binary target vector y.
    
    Target Mapping:
    - Adverse Outcome (Default / Positive Class 1): 'Charged Off'
    - Favorable Outcome (Non-Default / Negative Class 0): 'Fully Paid'
    - Unresolved Outcome Handling: 'Current' loans (ongoing repayments) are excluded
      from supervised training to prevent target noise.
    
    Returns:
    - X (pd.DataFrame): Feature matrix containing ONLY allowed prediction-time features.
    - y (pd.Series): Binary target vector (0 or 1).
    - metadata (dict): Dataset preparation statistics and sample counts.
    """
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty or None.")

    raw_total_records = len(df)
    
    # 1. Filter for completed loans with known outcomes
    completed_df = df[df["loan_status"].isin(["Fully Paid", "Charged Off"])].copy()
    current_excluded_count = raw_total_records - len(completed_df)

    if len(completed_df) == 0:
        raise ValueError("No completed loans ('Fully Paid' or 'Charged Off') found in dataset.")

    # 2. Binary Target Mapping (Adverse Risk = Positive Class 1)
    y = (completed_df["loan_status"] == "Charged Off").astype(int)
    y.name = "target_default"

    # 3. Extract Allowed Features Only
    missing_allowed = [f for f in FEATURE_ALLOWLIST if f not in completed_df.columns]
    if missing_allowed:
        raise ValueError(f"Missing required prediction features in dataset: {missing_allowed}")

    X = completed_df[FEATURE_ALLOWLIST].copy()

    # 4. Strict Target Leakage Assertion
    leakage_detected = [col for col in LEAKAGE_EXCLUSIONS if col in X.columns]
    if leakage_detected:
        raise ValueError(f"TARGET LEAKAGE DETECTED! Allowed features contained prohibited post-outcome columns: {leakage_detected}")

    # Metadata audit
    total_samples = len(X)
    default_count = int(y.sum())
    non_default_count = int(total_samples - default_count)
    default_rate_pct = float((default_count / total_samples) * 100.0)

    metadata = {
        "raw_total_records": raw_total_records,
        "excluded_current_records": current_excluded_count,
        "completed_sample_count": total_samples,
        "class_0_fully_paid_count": non_default_count,
        "class_1_charged_off_count": default_count,
        "default_rate_pct": round(default_rate_pct, 2),
        "numerical_features": NUMERICAL_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "total_feature_count": len(FEATURE_ALLOWLIST)
    }

    return X, y, metadata

def build_preprocessor_pipeline() -> ColumnTransformer:
    """
    Constructs a ColumnTransformer preprocessing pipeline:
    - Numerical: SimpleImputer(median) -> StandardScaler()
    - Categorical: SimpleImputer(most_frequent) -> OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    """
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, NUMERICAL_FEATURES),
            ("cat", cat_pipeline, CATEGORICAL_FEATURES)
        ],
        remainder="drop"
    )

    return preprocessor
