"""
Global configuration for RecoverAI.
Central place for paths, dataset size, and random seed so every module
(and every run) stays reproducible and consistent.
"""

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "synthetic_payment_events.csv")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "processed_payments.csv")
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "recoverability_model.pkl")
MODEL_METRICS_PATH = os.path.join(BASE_DIR, "data", "models", "model_metrics.json")

DB_PATH = os.path.join(BASE_DIR, "database", "recoverai.db")

AUDIT_LOG_DIR = os.path.join(BASE_DIR, "outputs", "audit_logs")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")
CHARTS_DIR = os.path.join(BASE_DIR, "outputs", "charts")

# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------
NUM_SYNTHETIC_RECORDS = 1000
RANDOM_SEED = 42

FAILURE_REASONS = [
    "BANK_TECHNICAL_FAILURE",
    "INSUFFICIENT_FUNDS",
    "CUSTOMER_ABANDONMENT",
    "NETWORK_FAILURE",
    "REPEATED_DECLINE",
    "EXPIRED_PAYMENT_METHOD",
    "UNKNOWN",
]

PAYMENT_METHODS = ["CARD", "UPI", "NETBANKING", "WALLET", "EMI"]

# ---------------------------------------------------------------------------
# Business economics (used by the Expected Recovery Value engine)
# ---------------------------------------------------------------------------
INTERVENTION_COST = {
    "RETRY": 5,
    "WAIT": 0,
    "SEND_REMINDER": 20,
    "GENERATE_PAYMENT_LINK": 50,
    "ESCALATE": 200,
    "STOP_RECOVERY": 0,
}

RISK_COST_FACTOR = 0.02  # % of amount treated as ongoing risk/carry cost if untouched
