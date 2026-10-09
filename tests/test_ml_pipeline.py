"""
Unit Tests for Machine Learning Pipeline & Leakage Safeguards
"""

import pytest
from pathlib import Path
import pandas as pd
import numpy as np
from src.config import CLEANED_DATA_PATH
from src.ml.feature_engineering import (
    prepare_ml_dataset,
    build_preprocessor_pipeline,
    FEATURE_ALLOWLIST,
    LEAKAGE_EXCLUSIONS
)
from src.ml.evaluate_model import evaluate_classifier, compare_models
from src.ml.train_model import train_and_evaluate_models

@pytest.fixture(scope="module")
def cleaned_df():
    if not CLEANED_DATA_PATH.exists():
        pytest.skip("Cleaned dataset CSV does not exist.")
    return pd.read_csv(CLEANED_DATA_PATH, low_memory=False)

def test_prepare_ml_dataset_target_mapping(cleaned_df):
    X, y, meta = prepare_ml_dataset(cleaned_df)

    # 1. Total records check
    assert meta["raw_total_records"] == 38576
    assert meta["excluded_current_records"] == 1098
    assert len(X) == 37478
    assert len(y) == 37478

    # 2. Binary target check
    assert set(y.unique()) == {0, 1}
    assert int(y.sum()) == 5333  # Charged Off count

    # 3. Target Leakage Assertion
    for prohibited_col in LEAKAGE_EXCLUSIONS:
        assert prohibited_col not in X.columns

def test_feature_allowlist_integrity(cleaned_df):
    X, y, meta = prepare_ml_dataset(cleaned_df)
    assert set(X.columns) == set(FEATURE_ALLOWLIST)
    assert X.shape[1] == 12

def test_preprocessor_pipeline_fitting(cleaned_df):
    X, y, meta = prepare_ml_dataset(cleaned_df)
    preprocessor = build_preprocessor_pipeline()
    
    # Fit preprocessor on training data
    X_trans = preprocessor.fit_transform(X.iloc[:100])
    assert isinstance(X_trans, np.ndarray)
    assert X_trans.shape[0] == 100
    assert X_trans.shape[1] > 12  # Due to OneHotEncoding

def test_unseen_categories_handling(cleaned_df):
    X, y, meta = prepare_ml_dataset(cleaned_df)
    preprocessor = build_preprocessor_pipeline()
    preprocessor.fit(X.iloc[:500])

    # Unseen state code and purpose
    unseen_sample = X.iloc[:2].copy()
    unseen_sample.loc[0, "address_state"] = "ZZ"  # Non-existent US state
    unseen_sample.loc[0, "purpose"] = "unseen_purpose_category"

    # Should transform without raising KeyError or ValueError
    X_unseen_trans = preprocessor.transform(unseen_sample)
    assert X_unseen_trans.shape[0] == 2

def test_train_and_evaluate_pipeline_execution():
    pipeline, metrics, cmp_df = train_and_evaluate_models(CLEANED_DATA_PATH)
    assert pipeline is not None
    assert metrics["roc_auc"] > 0.60
    assert metrics["recall"] > 0.50
    assert len(cmp_df) == 2
