import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.preprocessing.feature_engineering import build_features, align_features, NUMERIC_COLS


def make_df():
    return pd.DataFrame([
        {"amount": 1000, "payment_method": "CARD", "failure_reason": "INSUFFICIENT_FUNDS",
         "retry_attempts": 1, "prior_failures": 0, "hours_since_failure": 10,
         "customer_txn_frequency_90d": 5},
        {"amount": 5000, "payment_method": "UPI", "failure_reason": "NETWORK_FAILURE",
         "retry_attempts": 0, "prior_failures": 1, "hours_since_failure": 2,
         "customer_txn_frequency_90d": 20},
    ])


def test_build_features_includes_all_numeric_columns():
    X = build_features(make_df())
    for col in NUMERIC_COLS:
        assert col in X.columns


def test_build_features_one_hot_encodes_categoricals():
    X = build_features(make_df())
    assert any(c.startswith("payment_method_") for c in X.columns)
    assert any(c.startswith("failure_reason_") for c in X.columns)


def test_align_features_adds_missing_columns_as_zero():
    X = build_features(make_df())
    training_columns = list(X.columns) + ["payment_method_WALLET"]
    aligned = align_features(X.copy(), training_columns)
    assert "payment_method_WALLET" in aligned.columns
    assert (aligned["payment_method_WALLET"] == 0).all()
    assert list(aligned.columns) == training_columns
