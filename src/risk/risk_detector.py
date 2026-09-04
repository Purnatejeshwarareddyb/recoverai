"""
Module 1: Revenue Risk Detector.

Produces a rule-based risk score (0-1) and risk level for a payment event,
independent of the ML recoverability model -- this is the fast, cheap first
pass that decides whether a payment deserves deeper analysis at all.
"""

import pandas as pd

REASON_RISK_WEIGHT = {
    "BANK_TECHNICAL_FAILURE": 0.3,
    "NETWORK_FAILURE": 0.3,
    "INSUFFICIENT_FUNDS": 0.6,
    "EXPIRED_PAYMENT_METHOD": 0.5,
    "REPEATED_DECLINE": 0.8,
    "CUSTOMER_ABANDONMENT": 0.7,
    "UNKNOWN": 0.6,
}


def score_row(row) -> float:
    score = REASON_RISK_WEIGHT.get(row["failure_reason"], 0.5)
    score += min(row["retry_attempts"], 5) * 0.05
    score += min(row["prior_failures"], 5) * 0.04
    score += 0.15 if row["hours_since_failure"] > 48 else 0
    score += 0.10 if row["amount"] > 20000 else 0
    return float(min(score, 1.0))


def risk_level(score: float) -> str:
    if score >= 0.7:
        return "HIGH"
    if score >= 0.4:
        return "MEDIUM"
    return "LOW"


def detect_risk(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["risk_score"] = out.apply(score_row, axis=1)
    out["risk_level"] = out["risk_score"].apply(risk_level)
    out["revenue_at_risk"] = out["amount"]
    return out
