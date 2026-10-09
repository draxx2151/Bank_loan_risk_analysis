# ML Credit Risk Intelligence Evaluation Report

- **Model Version**: v1.0.0
- **Selected Model**: Logistic Regression (Baseline)
- **Random Seed**: 42
- **Training Universe**: 37478 completed historical loans (Excluded 1098 active `Current` loans).
- **Split**: 80/20 Stratified Split (29982 Train / 7496 Test).

## Performance Metrics (Held-Out Test Set)

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| **Logistic Regression (Baseline)** | 0.6443 | 0.2327 | 0.6523 | 0.343 | 0.6953 | 0.2709 |
| **Random Forest Classifier** | 0.6761 | 0.2412 | 0.5942 | 0.3431 | 0.6945 | 0.2695 |

## Selected Model Confusion Matrix (Logistic Regression (Baseline))
- **True Negatives (TN)**: 4134
- **False Positives (FP)**: 2295
- **False Negatives (FN)**: 371
- **True Positives (TP)**: 696

## Underwriting Disclaimers & Limitations
- **Academic Decision Support**: Model outputs represent learned historical associations from consumer loan performance and are not intended for live automated underwriting.
- **Class Imbalance**: Default outcome accounts for ~14.2% of historical completed loans. Balanced class weights were applied during training.
