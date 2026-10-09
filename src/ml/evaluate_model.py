"""
Model Evaluation Module
Computes classification metrics, confusion matrices, ROC-AUC, PR-AUC,
feature coefficients/importances, and comparative metric summary tables.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

def extract_feature_names(pipeline) -> List[str]:
    """Extracts feature names from fitted ColumnTransformer inside pipeline."""
    if not hasattr(pipeline, "named_steps") or "preprocessor" not in pipeline.named_steps:
        return []

    preprocessor = pipeline.named_steps["preprocessor"]
    feature_names = []
    
    for name, transformer, cols in preprocessor.transformers_:
        if name == "num":
            feature_names.extend(cols)
        elif name == "cat":
            if hasattr(transformer, "named_steps") and "onehot" in transformer.named_steps:
                onehot = transformer.named_steps["onehot"]
                cat_names = onehot.get_feature_names_out(cols)
                feature_names.extend(cat_names)
            else:
                feature_names.extend(cols)
    return feature_names

def get_feature_importances(pipeline, top_n: int = 15) -> pd.DataFrame:
    """
    Extracts top feature coefficients for Logistic Regression or feature importances for Random Forest.
    """
    if not hasattr(pipeline, "named_steps") or "classifier" not in pipeline.named_steps:
        return pd.DataFrame()

    classifier = pipeline.named_steps["classifier"]
    feature_names = extract_feature_names(pipeline)

    if hasattr(classifier, "coef_"):
        coefs = classifier.coef_[0]
        if len(coefs) != len(feature_names):
            return pd.DataFrame()
        df_imp = pd.DataFrame({
            "feature": feature_names,
            "coefficient": coefs,
            "impact_direction": np.where(coefs > 0, "Increases Default Risk", "Decreases Default Risk"),
            "abs_impact": np.abs(coefs)
        }).sort_values("abs_impact", ascending=False).head(top_n)
        return df_imp
    elif hasattr(classifier, "feature_importances_"):
        imps = classifier.feature_importances_
        if len(imps) != len(feature_names):
            return pd.DataFrame()
        df_imp = pd.DataFrame({
            "feature": feature_names,
            "importance": imps,
            "impact_direction": "Feature Importance",
            "abs_impact": imps
        }).sort_values("abs_impact", ascending=False).head(top_n)
        return df_imp

    return pd.DataFrame()

def evaluate_classifier(model, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Any]:
    """
    Evaluates a trained classifier pipeline on the held-out test set.
    Positive Class 1 = Charged Off (Adverse Risk).
    """
    if model is None or X_test is None or y_test is None:
        raise ValueError("Model, X_test, and y_test cannot be None.")

    y_pred = model.predict(X_test)
    
    # Extract positive class predicted probabilities
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, "decision_function"):
        y_prob = model.decision_function(X_test)
    else:
        y_prob = y_pred

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, pos_label=1, zero_division=0))
    rec = float(recall_score(y_test, y_pred, pos_label=1, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, pos_label=1, zero_division=0))

    try:
        roc_auc = float(roc_auc_score(y_test, y_prob))
    except Exception:
        roc_auc = 0.0

    try:
        pr_auc = float(average_precision_score(y_test, y_prob))
    except Exception:
        pr_auc = 0.0

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)

    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "pr_auc": round(pr_auc, 4),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
            "matrix_array": cm.tolist()
        },
        "test_sample_count": len(y_test),
        "test_positive_count": int(y_test.sum()),
        "test_negative_count": int(len(y_test) - y_test.sum()),
        "classification_report": report_dict
    }

def compare_models(metrics_map: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """
    Builds a summary comparison table DataFrame across trained candidate models.
    """
    rows = []
    for model_name, metrics in metrics_map.items():
        cm = metrics.get("confusion_matrix", {})
        rows.append({
            "Model": model_name,
            "Accuracy": metrics.get("accuracy", 0.0),
            "Precision": metrics.get("precision", 0.0),
            "Recall": metrics.get("recall", 0.0),
            "F1-Score": metrics.get("f1_score", 0.0),
            "ROC-AUC": metrics.get("roc_auc", 0.0),
            "PR-AUC": metrics.get("pr_auc", 0.0),
            "True Positives (TP)": cm.get("tp", 0),
            "False Positives (FP)": cm.get("fp", 0),
            "False Negatives (FN)": cm.get("fn", 0),
            "True Negatives (TN)": cm.get("tn", 0)
        })
    df_cmp = pd.DataFrame(rows)
    return df_cmp
