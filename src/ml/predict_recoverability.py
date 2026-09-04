"""Module 2: Recoverability Predictor -- inference."""

import joblib
import pandas as pd
from config import settings
from src.preprocessing.feature_engineering import build_features, align_features

_bundle_cache = None


def _load_bundle():
    global _bundle_cache
    if _bundle_cache is None:
        _bundle_cache = joblib.load(settings.MODEL_PATH)
    return _bundle_cache


def predict_recovery_probability(df: pd.DataFrame) -> pd.DataFrame:
    """Adds a 'recovery_probability' column to df using the trained model."""
    bundle = _load_bundle()
    model = bundle["model"]
    columns = bundle["feature_columns"]

    X = build_features(df)
    X = align_features(X, columns)

    proba = model.predict_proba(X)[:, 1]
    out = df.copy()
    out["recovery_probability"] = proba.round(4)
    out["model_used"] = bundle["model_name"]
    return out
