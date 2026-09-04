import streamlit as st
import pandas as pd
from src.utils.helpers import get_audit_trail, format_inr
from src.analytics.metrics import compute_summary


def render():
    st.title(" Executive Overview")
    st.caption("System-wide revenue recovery performance")

    audit_df = get_audit_trail()

    if audit_df.empty:
        st.warning(
            "No audit data yet. Run `python scripts/run_pipeline.py` "
            "from the project root to process the synthetic batch, then reload this page."
        )
        return

    summary = compute_summary(audit_df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Transactions", f"{summary['total_transactions']:,}")
    c2.metric("Revenue At Risk", format_inr(summary["revenue_at_risk"]))
    c3.metric("Revenue Recovered", format_inr(summary["revenue_recovered"]))
    c4.metric("Recovery Rate", f"{summary['recovery_rate']:.1%}")

    c5, c6, c7 = st.columns(3)
    c5.metric("Avg Recovery Value", format_inr(summary["avg_recovery_value"]))
    c6.metric("Cases Escalated", f"{summary['cases_escalated']:,}")
    c7.metric("Cases Stopped", f"{summary['cases_stopped']:,}")

    st.markdown("---")
    st.subheader("Outcomes by Final Action")
    action_counts = audit_df["final_action"].value_counts()
    st.bar_chart(action_counts)

    st.subheader("Revenue Recovered vs Revenue At Risk (by Risk Level)")
    grouped = audit_df.groupby("risk_level").apply(
        lambda g: pd.Series({
            "revenue_at_risk": g["amount"].sum(),
            "revenue_recovered": g.loc[g["outcome"] == "RECOVERED", "amount"].sum(),
        })
    )
    st.bar_chart(grouped)
