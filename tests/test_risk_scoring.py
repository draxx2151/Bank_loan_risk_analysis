"""
Unit Tests for Credit Risk Scoring Engine
"""

import pytest
import pandas as pd
import numpy as np
from src.ml.risk_scoring import CreditRiskScoringEngine, LOW_RISK_THRESHOLD, HIGH_RISK_THRESHOLD

@pytest.fixture(scope="module")
def scoring_engine():
    engine = CreditRiskScoringEngine()
    return engine

@pytest.fixture
def sample_valid_record():
    return {
        "loan_amount": 10000,
        "annual_income": 60000,
        "dti": 0.12,
        "int_rate": 0.105,
        "emp_length_years": 5.0,
        "total_acc": 15,
        "term": "36 months",
        "grade": "B",
        "home_ownership": "MORTGAGE",
        "verification_status": "Verified",
        "purpose": "debt_consolidation",
        "address_state": "CA"
    }

def test_score_record_success(scoring_engine, sample_valid_record):
    res = scoring_engine.score_record(sample_valid_record)
    assert res["status"] == "SUCCESS"
    assert 0.0 <= res["risk_probability"] <= 1.0
    assert 0.0 <= res["risk_score_pct"] <= 100.0
    assert res["predicted_class"] in [0, 1]
    assert res["risk_category"] in ["Low Risk", "Medium Risk", "High Risk"]
    assert res["model_version"] == "v1.0.0"

@pytest.mark.parametrize(
    "probability, expected_category",
    [
        (0.00, "Low Risk"),
        (0.10, "Low Risk"),
        (0.149999, "Low Risk"),
        (LOW_RISK_THRESHOLD - 1e-9, "Low Risk"),
        (LOW_RISK_THRESHOLD, "Medium Risk"),
        (0.15, "Medium Risk"),
        (0.20, "Medium Risk"),
        (0.349999, "Medium Risk"),
        (HIGH_RISK_THRESHOLD - 1e-9, "Medium Risk"),
        (HIGH_RISK_THRESHOLD, "High Risk"),
        (0.35, "High Risk"),
        (0.50, "High Risk"),
        (1.00, "High Risk"),
        (np.nan, "UNKNOWN"),
        (float("nan"), "UNKNOWN"),
    ]
)
def test_risk_categorization_thresholds(probability, expected_category):
    assert CreditRiskScoringEngine.categorize_risk(probability) == expected_category

def test_score_record_missing_required_field(scoring_engine, sample_valid_record):
    incomplete_record = sample_valid_record.copy()
    del incomplete_record["loan_amount"]
    
    res = scoring_engine.score_record(incomplete_record)
    assert res["status"] == "MISSING_REQUIRED_FIELDS"
    assert res["risk_probability"] is None
    assert res["risk_category"] == "UNKNOWN"

def test_score_record_invalid_input(scoring_engine):
    res = scoring_engine.score_record({})
    assert res["status"] == "INVALID_INPUT"
    
    res2 = scoring_engine.score_record(None)
    assert res2["status"] == "INVALID_INPUT"

def test_score_record_ignores_post_outcome_leakage_fields(scoring_engine, sample_valid_record):
    leakage_record = sample_valid_record.copy()
    leakage_record["total_payment"] = 5000.0  # Leakage field
    leakage_record["loan_status"] = "Charged Off"  # Target field

    res = scoring_engine.score_record(leakage_record)
    assert res["status"] == "SUCCESS"
    assert len(res["warnings"]) > 0
    assert "total_payment" in res["warnings"][0]

def test_score_batch_success(scoring_engine, sample_valid_record):
    df_batch = pd.DataFrame([sample_valid_record, sample_valid_record])
    scored_df = scoring_engine.score_batch(df_batch)

    assert len(scored_df) == 2
    assert "predicted_default_prob" in scored_df.columns
    assert "predicted_risk_score_pct" in scored_df.columns
    assert "predicted_default_class" in scored_df.columns
    assert "risk_category" in scored_df.columns

def test_score_batch_empty_dataframe(scoring_engine):
    with pytest.raises(ValueError):
        scoring_engine.score_batch(pd.DataFrame())
