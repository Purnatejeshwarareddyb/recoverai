"""Aggregates the audit trail into executive-level recovery metrics."""

import pandas as pd


def compute_summary(audit_df: pd.DataFrame) -> dict:
    if audit_df.empty:
        return {
            "total_transactions": 0, "revenue_at_risk": 0, "revenue_recovered": 0,
            "recovery_rate": 0, "avg_recovery_value": 0, "cases_escalated": 0,
            "cases_stopped": 0,
        }

    total_transactions = len(audit_df)
    revenue_at_risk = audit_df["amount"].sum()
    recovered_mask = audit_df["outcome"] == "RECOVERED"
    revenue_recovered = audit_df.loc[recovered_mask, "amount"].sum()
    attempted_mask = audit_df["final_action"] != "STOP_RECOVERY"
    recovery_rate = (recovered_mask.sum() / attempted_mask.sum()) if attempted_mask.sum() else 0
    avg_recovery_value = audit_df.loc[recovered_mask, "amount"].mean() if recovered_mask.any() else 0
    cases_escalated = (audit_df["final_action"] == "ESCALATE").sum()
    cases_stopped = (audit_df["final_action"] == "STOP_RECOVERY").sum()

    return {
        "total_transactions": int(total_transactions),
        "revenue_at_risk": round(float(revenue_at_risk), 2),
        "revenue_recovered": round(float(revenue_recovered), 2),
        "recovery_rate": round(float(recovery_rate), 4),
        "avg_recovery_value": round(float(avg_recovery_value), 2),
        "cases_escalated": int(cases_escalated),
        "cases_stopped": int(cases_stopped),
    }
