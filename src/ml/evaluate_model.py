"""
Re-evaluates the currently saved model against a fresh holdout split and
prints a readable report. Useful for sanity-checking a model after
retraining without re-running the whole training script.

Run:
    python -m src.ml.evaluate_model
"""

import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

from config import settings
from src.ingestion.payment_loader import load_raw_payments
from src.preprocessing.feature_engineering import build_features, align_features


def evaluate():
    bundle = joblib.load(settings.MODEL_PATH)
    model = bundle["model"]
    columns = bundle["feature_columns"]

    df = load_raw_payments()
    X = align_features(build_features(df), columns)
    y = df["recovered"]

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.25, random_state=settings.RANDOM_SEED, stratify=y
    )

    proba = model.predict_proba(X_test)[:, 1]
    preds = model.predict(X_test)

    print(f"Model: {bundle['model_name']}")
    print(f"ROC-AUC: {roc_auc_score(y_test, proba):.4f}")
    print(classification_report(y_test, preds, target_names=["Not Recovered", "Recovered"]))


if __name__ == "__main__":
    evaluate()
