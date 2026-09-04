"""
Turns raw payment events into the numeric feature matrix used by the
recoverability ML model.
"""

import pandas as pd

CATEGORICAL_COLS = ["payment_method", "failure_reason"]
NUMERIC_COLS = [
    "amount",
    "retry_attempts",
    "prior_failures",
    "hours_since_failure",
    "customer_txn_frequency_90d",
]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """One-hot encodes categoricals and keeps numeric columns. Returns X only."""
    encoded = pd.get_dummies(df[CATEGORICAL_COLS], prefix=CATEGORICAL_COLS)
    features = pd.concat([df[NUMERIC_COLS].reset_index(drop=True),
                           encoded.reset_index(drop=True)], axis=1)
    return features


def align_features(features: pd.DataFrame, training_columns: list) -> pd.DataFrame:
    """Ensures inference-time features have exactly the columns the model was trained on."""
    for col in training_columns:
        if col not in features.columns:
            features[col] = 0
    return features[training_columns]
