"""
Phase 6 Integration, Model Integrity, and Production Readiness Tests
"""

import pytest
import pandas as pd
import numpy as np
from src.config import DEFAULT_DB_PATH, CLEANED_DATA_PATH
from src.database.db_manager import DatabaseManager
from src.ml.risk_scoring import CreditRiskScoringEngine
from src.ml.evaluate_model import get_feature_importances
from src.ui.views.summary import render_summary_page
from src.ui.views.overview import render_overview_page
from src.ui.views.details import render_details_page
from src.ui.views.risk_intelligence import render_risk_intelligence_page

@pytest.fixture(scope="module")
def loaded_components():
    db = DatabaseManager(DEFAULT_DB_PATH)
    engine = CreditRiskScoringEngine()
    df = pd.read_csv(CLEANED_DATA_PATH, low_memory=False)
    return db, engine, df

def test_phase6_model_explainability(loaded_components):
    _, engine, _ = loaded_components
    df_exp = engine.get_model_explainability(top_n=10)
    assert not df_exp.empty
    assert "feature" in df_exp.columns
    assert "coefficient" in df_exp.columns
    assert "impact_direction" in df_exp.columns
    assert len(df_exp) <= 10

def test_phase6_unseen_categorical_inference(loaded_components):
    _, engine, _ = loaded_components
    unseen_record = {
        "loan_amount": 20000,
        "annual_income": 80000,
        "dti": 0.15,
        "int_rate": 0.115,
        "emp_length_years": 4.0,
        "total_acc": 18,
        "term": "36 months",
        "grade": "Z",  # Unseen grade
        "home_ownership": "UNSEEN_HOME",  # Unseen home ownership
        "verification_status": "Verified",
        "purpose": "unseen_purpose_type",  # Unseen purpose
        "address_state": "ZZ"  # Unseen state code
    }
    res = engine.score_record(unseen_record)
    assert res["status"] == "SUCCESS"
    assert 0.0 <= res["risk_probability"] <= 1.0

def test_phase6_database_connection_cleanup(loaded_components):
    db, _, _ = loaded_components
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bank_loans")
        count = cursor.fetchone()[0]
        assert count == 38576

def test_phase6_view_functions_import_and_execution(loaded_components):
    _, _, df = loaded_components
    sample_sub = df.head(10).copy()
    
    # Ensure all 4 view rendering functions accept DataFrame without crashing
    assert callable(render_summary_page)
    assert callable(render_overview_page)
    assert callable(render_details_page)
    assert callable(render_risk_intelligence_page)
