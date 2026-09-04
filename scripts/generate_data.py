"""
Generates a realistic synthetic dataset of failed / at-risk payment events.

Run:
    python scripts/generate_data.py
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings


def _sample_amount(rng):
    # Log-normal gives a realistic long tail of transaction sizes
    return round(float(np.clip(rng.lognormal(mean=8.0, sigma=1.1), 50, 500_000)), 2)


def _reason_recovery_bias(reason):
    """Different failure reasons have structurally different recovery odds."""
    bias = {
        "BANK_TECHNICAL_FAILURE": 0.80,
        "NETWORK_FAILURE": 0.75,
        "INSUFFICIENT_FUNDS": 0.35,
        "EXPIRED_PAYMENT_METHOD": 0.40,
        "REPEATED_DECLINE": 0.20,
        "CUSTOMER_ABANDONMENT": 0.25,
        "UNKNOWN": 0.30,
    }
    return bias[reason]


def generate(n=settings.NUM_SYNTHETIC_RECORDS, seed=settings.RANDOM_SEED):
    rng = np.random.default_rng(seed)
    rows = []
    base_time = datetime(2026, 1, 1)

    for i in range(n):
        payment_id = f"P{100000 + i}"
        customer_id = f"C{rng.integers(1, int(n * 0.6))}"  # customers can repeat
        amount = _sample_amount(rng)
        method = rng.choice(settings.PAYMENT_METHODS, p=[0.45, 0.35, 0.10, 0.06, 0.04])
        reason = rng.choice(settings.FAILURE_REASONS, p=[0.18, 0.22, 0.15, 0.13, 0.14, 0.08, 0.10])
        retry_attempts = int(rng.integers(0, 4))
        prior_failures = int(rng.poisson(1.2))
        hours_since_failure = float(rng.exponential(20))
        txn_frequency = int(rng.integers(1, 30))  # customer's txns in last 90 days

        # Ground-truth recovery probability is a function of structural factors
        # plus noise -- this is what the ML model will later have to learn.
        base_p = _reason_recovery_bias(reason)
        base_p += 0.05 if method in ("CARD", "UPI") else -0.05
        base_p -= 0.03 * retry_attempts
        base_p -= 0.02 * prior_failures
        base_p += 0.10 if txn_frequency > 10 else 0
        base_p -= 0.10 if hours_since_failure > 72 else 0
        base_p = float(np.clip(base_p + rng.normal(0, 0.08), 0.02, 0.97))

        recovered = int(rng.random() < base_p)

        event_time = base_time + timedelta(hours=float(rng.integers(0, 24 * 90)))

        rows.append({
            "payment_id": payment_id,
            "customer_id": customer_id,
            "amount": amount,
            "payment_method": method,
            "failure_reason": reason,
            "retry_attempts": retry_attempts,
            "prior_failures": prior_failures,
            "hours_since_failure": round(hours_since_failure, 1),
            "customer_txn_frequency_90d": txn_frequency,
            "event_timestamp": event_time.isoformat(),
            "true_recovery_probability": round(base_p, 4),  # for evaluation only
            "recovered": recovered,  # ML training label
        })

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(settings.RAW_DATA_PATH), exist_ok=True)
    df.to_csv(settings.RAW_DATA_PATH, index=False)
    print(f"Generated {len(df)} synthetic payment records -> {settings.RAW_DATA_PATH}")
    print(f"Overall recovery rate in synthetic data: {df['recovered'].mean():.2%}")
    return df


if __name__ == "__main__":
    generate()
