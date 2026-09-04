"""
Runs the full RecoverAI pipeline over the entire synthetic batch:

    Ingest -> Risk Detection -> Recoverability Prediction ->
    (per payment) Root Cause -> Strategy -> Expected Value ->
    Policy -> Simulated Execution -> Audit Trail

Run:
    python scripts/run_pipeline.py
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import defaultdict

from database.database import init_db, get_connection
from src.ingestion.payment_loader import load_raw_payments
from src.risk.risk_detector import detect_risk
from src.ml.predict_recoverability import predict_recovery_probability
from src.recovery.recovery_executor import process_payment
from config import settings


def run():
    init_db()
    # Clear previous audit trail so re-running the pipeline gives a clean demo
    conn = get_connection()
    conn.execute("DELETE FROM audit_trail")
    conn.commit()
    conn.close()

    df = load_raw_payments()
    df = detect_risk(df)
    df = predict_recovery_probability(df)

    contact_counts = defaultdict(int)
    results = []
    for i, row in df.iterrows():
        row_dict = row.to_dict()
        record = process_payment(
            row_dict,
            contact_count_so_far=contact_counts[row_dict["customer_id"]],
            seed=settings.RANDOM_SEED + i,
        )
        if record["final_action"] in ("SEND_REMINDER", "GENERATE_PAYMENT_LINK"):
            contact_counts[row_dict["customer_id"]] += 1
        results.append(record)

    recovered = sum(1 for r in results if r["outcome"] == "RECOVERED")
    revenue_recovered = sum(r["amount"] for r in results if r["outcome"] == "RECOVERED")
    print(f"Processed {len(results)} payments.")
    print(f"Recovered: {recovered} payments, ₹{revenue_recovered:,.2f}")
    return results


if __name__ == "__main__":
    run()
