"""
Module 2: Recoverability Predictor -- training.

Trains and compares Logistic Regression vs Random Forest, selects the
better model by ROC-AUC, and persists it along with its metrics.
"""

import json
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, roc_curve
)

from config import settings
from src.ingestion.payment_loader import load_raw_payments
from src.preprocessing.feature_engineering import build_features


def _evaluate(name, model, X_test, y_test):
    proba = model.predict_proba(X_test)[:, 1]
    preds = model.predict(X_test)
    fpr, tpr, _ = roc_curve(y_test, proba)
    return {
        "model": name,
        "accuracy": round(accuracy_score(y_test, preds), 4),
        "precision": round(precision_score(y_test, preds, zero_division=0), 4),
        "recall": round(recall_score(y_test, preds, zero_division=0), 4),
        "f1_score": round(f1_score(y_test, preds, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
        "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
        "roc_curve": {"fpr": fpr.tolist(), "tpr": tpr.tolist()},
    }


def train():
    df = load_raw_payments()
    X = build_features(df)
    y = df["recovered"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=settings.RANDOM_SEED, stratify=y
    )

    candidates = {
        "LogisticRegression": LogisticRegression(max_iter=5000),
        "RandomForest": RandomForestClassifier(
            n_estimators=200, max_depth=8, random_state=settings.RANDOM_SEED
        ),
    }

    results = {}
    fitted = {}
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        fitted[name] = model
        results[name] = _evaluate(name, model, X_test, y_test)

    best_name = max(results, key=lambda k: results[k]["roc_auc"])
    best_model = fitted[best_name]

    joblib.dump({
        "model": best_model,
        "feature_columns": list(X.columns),
        "model_name": best_name,
    }, settings.MODEL_PATH)

    metrics_out = {"selected_model": best_name, "candidates": results}
    with open(settings.MODEL_METRICS_PATH, "w") as f:
        json.dump(metrics_out, f, indent=2)

    print(f"Best model: {best_name} (ROC-AUC={results[best_name]['roc_auc']})")
    print(f"Saved -> {settings.MODEL_PATH}")
    return metrics_out


if __name__ == "__main__":
    train()
