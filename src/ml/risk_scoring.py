"""
Risk Scoring Engine Module
Provides real-time single-record and batch risk scoring using the trained ML pipeline.
Categorizes predictions into documented risk tiers (Low, Medium, High).
"""

from pathlib import Path
from typing import Dict, Any, Union, List
import pandas as pd
import numpy as np
import joblib

from src.config import BASE_DIR
from src.ml.feature_engineering import (
    FEATURE_ALLOWLIST,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    LEAKAGE_EXCLUSIONS
)

DEFAULT_MODEL_PATH = BASE_DIR / "artifacts" / "models" / "credit_risk_pipeline_latest.joblib"

# Configured & Documented Risk Thresholds
LOW_RISK_THRESHOLD = 0.15
HIGH_RISK_THRESHOLD = 0.35

class CreditRiskScoringEngine:
    """Inference engine for scoring credit risk probability and assigning risk tiers."""

    def __init__(self, model_path: Union[str, Path] = DEFAULT_MODEL_PATH):
        self.model_path = Path(model_path)
        self.pipeline = None
        self.load_model()

    def load_model(self):
        """Loads trained joblib model pipeline."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model artifact not found at {self.model_path}. Train model first via src.ml.train_model.")
        try:
            self.pipeline = joblib.load(self.model_path)
        except Exception as e:
            raise RuntimeError(f"Error deserializing model artifact from {self.model_path}: {e}")

    def get_model_explainability(self, top_n: int = 10) -> pd.DataFrame:
        """Returns top feature coefficients/importances for model explainability."""
        from src.ml.evaluate_model import get_feature_importances
        return get_feature_importances(self.pipeline, top_n=top_n)

    @staticmethod
    def categorize_risk(probability: float) -> str:
        """
        Maps continuous default probability P(Default) to documented risk category:
        - Low Risk: P(Default) < 0.15
        - Medium Risk: 0.15 <= P(Default) < 0.35
        - High Risk: P(Default) >= 0.35
        """
        if np.isnan(probability):
            return "UNKNOWN"
        if probability < LOW_RISK_THRESHOLD:
            return "Low Risk"
        elif probability < HIGH_RISK_THRESHOLD:
            return "Medium Risk"
        else:
            return "High Risk"

    def score_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scores a single loan application record dictionary.
        Returns structured dictionary containing probability, predicted class, risk tier, and status.
        """
        warnings = []
        if not isinstance(record, dict) or not record:
            return {
                "status": "INVALID_INPUT",
                "error": "Record input must be a non-empty dictionary.",
                "risk_probability": None,
                "risk_category": "UNKNOWN"
            }

        # Check for prohibited leakage fields in input
        leakage_cols = [c for c in record.keys() if c in LEAKAGE_EXCLUSIONS]
        if leakage_cols:
            warnings.append(f"Post-outcome servicing fields provided but ignored for underwriting prediction: {leakage_cols}")

        # Missing required feature check
        missing_feats = [f for f in FEATURE_ALLOWLIST if f not in record or record[f] is None or record[f] == ""]
        if missing_feats:
            return {
                "status": "MISSING_REQUIRED_FIELDS",
                "error": f"Missing required prediction features: {missing_feats}",
                "risk_probability": None,
                "risk_category": "UNKNOWN",
                "warnings": warnings
            }

        # Build 1-row DataFrame
        try:
            df_input = pd.DataFrame([record])[FEATURE_ALLOWLIST]
        except Exception as e:
            return {
                "status": "INPUT_CONVERSION_ERROR",
                "error": f"Failed to format input record: {e}",
                "risk_probability": None,
                "risk_category": "UNKNOWN"
            }

        # Perform inference
        try:
            prob = float(self.pipeline.predict_proba(df_input)[0, 1])
            pred_class = int(self.pipeline.predict(df_input)[0])
            category = self.categorize_risk(prob)

            return {
                "status": "SUCCESS",
                "risk_probability": round(prob, 4),
                "risk_score_pct": round(prob * 100.0, 2),
                "predicted_class": pred_class,
                "predicted_label": "High Default Risk" if pred_class == 1 else "Standard/Low Risk",
                "risk_category": category,
                "model_version": "v1.0.0",
                "warnings": warnings
            }
        except Exception as e:
            return {
                "status": "INFERENCE_ERROR",
                "error": f"Error during model prediction: {e}",
                "risk_probability": None,
                "risk_category": "UNKNOWN"
            }

    def score_batch(self, df_batch: pd.DataFrame) -> pd.DataFrame:
        """
        Scores a batch DataFrame of loan applications and appends prediction columns.
        """
        if df_batch is None or df_batch.empty:
            raise ValueError("Input batch DataFrame is empty or None.")

        missing_feats = [f for f in FEATURE_ALLOWLIST if f not in df_batch.columns]
        if missing_feats:
            raise ValueError(f"Batch DataFrame missing required prediction features: {missing_feats}")

        df_out = df_batch.copy()
        X_batch = df_out[FEATURE_ALLOWLIST]

        probs = self.pipeline.predict_proba(X_batch)[:, 1]
        preds = self.pipeline.predict(X_batch)
        categories = [self.categorize_risk(p) for p in probs]

        df_out["predicted_default_prob"] = np.round(probs, 4)
        df_out["predicted_risk_score_pct"] = np.round(probs * 100.0, 2)
        df_out["predicted_default_class"] = preds
        df_out["risk_category"] = categories

        return df_out
