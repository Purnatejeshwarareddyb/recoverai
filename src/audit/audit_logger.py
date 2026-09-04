"""
Module: Audit System.

Every single AI decision -- prediction, recommendation, policy verdict,
and outcome -- is written here. This is what makes RecoverAI explainable
and auditable rather than a black box.
"""

import json
from datetime import datetime, timezone
from database.database import get_connection


def log_decision(record: dict):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO audit_trail (
            event_time, payment_id, customer_id, amount, risk_score, risk_level,
            root_cause, recovery_probability, model_used, recommended_action,
            expected_value, policy_approved, final_action, policy_reasons, outcome
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now(timezone.utc).isoformat(),
            record["payment_id"],
            record["customer_id"],
            record["amount"],
            record["risk_score"],
            record["risk_level"],
            record["root_cause"],
            record["recovery_probability"],
            record["model_used"],
            record["recommended_action"],
            record["expected_value"],
            int(record["policy_approved"]),
            record["final_action"],
            json.dumps(record["policy_reasons"]),
            record["outcome"],
        ),
    )
    conn.commit()
    conn.close()


def read_audit_trail(limit: int = 1000):
    import pandas as pd
    conn = get_connection()
    df = pd.read_sql_query(
        f"SELECT * FROM audit_trail ORDER BY id DESC LIMIT {limit}", conn
    )
    conn.close()
    return df
