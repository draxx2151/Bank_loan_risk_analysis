"""
Model Training Script
Trains candidate credit risk classification pipelines (Logistic Regression vs Random Forest),
evaluates metrics on held-out test set, selects the best model, and persists versioned artifacts.
"""

import json
from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from src.config import CLEANED_DATA_PATH, BASE_DIR
from src.ml.feature_engineering import (
    prepare_ml_dataset,
    build_preprocessor_pipeline,
    FEATURE_ALLOWLIST,
    LEAKAGE_EXCLUSIONS
)
from src.ml.evaluate_model import evaluate_classifier, compare_models

ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODELS_DIR = ARTIFACTS_DIR / "models"
METRICS_DIR = ARTIFACTS_DIR / "metrics"
REPORTS_DIR = ARTIFACTS_DIR / "reports"

def train_and_evaluate_models(data_path: Path = CLEANED_DATA_PATH) -> Tuple[Any, Dict[str, Any], pd.DataFrame]:
    """
    Executes the full training, cross-model evaluation, selection, and artifact persistence pipeline.
    """
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading cleaned dataset from {data_path}...")
    df = pd.read_csv(data_path, low_memory=False)

    print("Preparing ML dataset and checking target leakage safeguards...")
    X, y, prep_metadata = prepare_ml_dataset(df)
    print(f"Completed loans dataset shape: X={X.shape}, y={y.shape}")
    print(f"Target distribution (Class 1 = Charged Off): {int(y.sum())} / {len(y)} ({prep_metadata['default_rate_pct']}%)")

    # Stratified 80/20 Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Train set: {len(X_train)} records, Test set: {len(X_test)} records.")

    # 1. Build Baseline: Logistic Regression Pipeline
    lr_preprocessor = build_preprocessor_pipeline()
    lr_model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    lr_pipeline = Pipeline([
        ("preprocessor", lr_preprocessor),
        ("classifier", lr_model)
    ])

    print("Fitting Baseline Logistic Regression Pipeline on train set...")
    lr_pipeline.fit(X_train, y_train)
    lr_metrics = evaluate_classifier(lr_pipeline, X_test, y_test)

    # 2. Build Challenger: Random Forest Pipeline
    rf_preprocessor = build_preprocessor_pipeline()
    rf_model = RandomForestClassifier(
        n_estimators=100, max_depth=12, class_weight="balanced", random_state=42, n_jobs=-1
    )
    rf_pipeline = Pipeline([
        ("preprocessor", rf_preprocessor),
        ("classifier", rf_model)
    ])

    print("Fitting Challenger Random Forest Pipeline on train set...")
    rf_pipeline.fit(X_train, y_train)
    rf_metrics = evaluate_classifier(rf_pipeline, X_test, y_test)

    # Model Comparison
    metrics_map = {
        "Logistic Regression (Baseline)": lr_metrics,
        "Random Forest Classifier (Challenger)": rf_metrics
    }
    comparison_df = compare_models(metrics_map)

    # Select Best Model based on ROC-AUC & F1-Score
    best_model_name = "Random Forest Classifier (Challenger)" if rf_metrics["roc_auc"] >= lr_metrics["roc_auc"] else "Logistic Regression (Baseline)"
    selected_pipeline = rf_pipeline if best_model_name == "Random Forest Classifier (Challenger)" else lr_pipeline
    selected_metrics = rf_metrics if best_model_name == "Random Forest Classifier (Challenger)" else lr_metrics

    print(f"\n=== MODEL EVALUATION COMPARISON ===")
    print(comparison_df.to_string(index=False))
    print(f"\nSelected Model: {best_model_name}")

    # Artifact Persistence
    model_version = "v1.0.0"
    model_filename = MODELS_DIR / f"credit_risk_pipeline_{model_version}.joblib"
    latest_model_filename = MODELS_DIR / "credit_risk_pipeline_latest.joblib"
    
    print(f"Saving model artifacts to {model_filename}...")
    joblib.dump(selected_pipeline, model_filename)
    joblib.dump(selected_pipeline, latest_model_filename)

    # Save Metadata JSON
    metadata = {
        "model_version": model_version,
        "selected_model_name": best_model_name,
        "random_seed": 42,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "positive_class": 1,
        "positive_class_label": "Charged Off (Default)",
        "negative_class_label": "Fully Paid (Non-Default)",
        "features_used": FEATURE_ALLOWLIST,
        "leakage_exclusions_count": len(LEAKAGE_EXCLUSIONS),
        "dataset_metadata": prep_metadata,
        "metrics": selected_metrics
    }
    
    with open(MODELS_DIR / "model_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    with open(METRICS_DIR / "evaluation_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_map, f, indent=2)

    # Save Markdown Evaluation Report
    report_md = f"""# ML Credit Risk Intelligence Evaluation Report

- **Model Version**: {model_version}
- **Selected Model**: {best_model_name}
- **Random Seed**: 42
- **Training Universe**: {prep_metadata['completed_sample_count']} completed historical loans (Excluded {prep_metadata['excluded_current_records']} active `Current` loans).
- **Split**: 80/20 Stratified Split ({len(X_train)} Train / {len(X_test)} Test).

## Performance Metrics (Held-Out Test Set)

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| **Logistic Regression (Baseline)** | {lr_metrics['accuracy']} | {lr_metrics['precision']} | {lr_metrics['recall']} | {lr_metrics['f1_score']} | {lr_metrics['roc_auc']} | {lr_metrics['pr_auc']} |
| **Random Forest Classifier** | {rf_metrics['accuracy']} | {rf_metrics['precision']} | {rf_metrics['recall']} | {rf_metrics['f1_score']} | {rf_metrics['roc_auc']} | {rf_metrics['pr_auc']} |

## Selected Model Confusion Matrix ({best_model_name})
- **True Negatives (TN)**: {selected_metrics['confusion_matrix']['tn']}
- **False Positives (FP)**: {selected_metrics['confusion_matrix']['fp']}
- **False Negatives (FN)**: {selected_metrics['confusion_matrix']['fn']}
- **True Positives (TP)**: {selected_metrics['confusion_matrix']['tp']}

## Underwriting Disclaimers & Limitations
- **Academic Decision Support**: Model outputs represent learned historical associations from consumer loan performance and are not intended for live automated underwriting.
- **Class Imbalance**: Default outcome accounts for ~14.2% of historical completed loans. Balanced class weights were applied during training.
"""
    with open(REPORTS_DIR / "model_evaluation_report.md", "w", encoding="utf-8") as f:
        f.write(report_md)

    return selected_pipeline, selected_metrics, comparison_df

if __name__ == "__main__":
    train_and_evaluate_models()
