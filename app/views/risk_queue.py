import streamlit as st
from src.utils.helpers import get_scored_payments
from src.recovery.expected_value import expected_value
from src.recovery.strategy_engine import recommend_strategy


def render():
    st.title(" Revenue Risk Queue")
    st.caption("All at-risk payments, ranked by highest expected recovery value")

    df = get_scored_payments()

    strategies = df.apply(lambda r: recommend_strategy(r), axis=1)
    df["recommended_action"] = strategies.apply(lambda s: s["recommended_action"])
    df["expected_value"] = strategies.apply(lambda s: s["expected_value"])

    col1, col2, col3 = st.columns(3)
    with col1:
        risk_filter = st.multiselect(
            "Risk level", options=sorted(df["risk_level"].unique()),
            default=sorted(df["risk_level"].unique())
        )
    with col2:
        reason_filter = st.multiselect(
            "Root cause", options=sorted(df["failure_reason"].unique()),
            default=sorted(df["failure_reason"].unique())
        )
    with col3:
        min_ev = st.number_input("Minimum expected value (₹)", value=-100000, step=1000)

    filtered = df[
        df["risk_level"].isin(risk_filter)
        & df["failure_reason"].isin(reason_filter)
        & (df["expected_value"] >= min_ev)
    ].sort_values("expected_value", ascending=False)

    st.write(f"**{len(filtered)}** payments match your filters")

    display_cols = [
        "payment_id", "amount", "risk_score", "risk_level",
        "recovery_probability", "failure_reason", "recommended_action", "expected_value",
    ]
    st.dataframe(
        filtered[display_cols].rename(columns={
            "payment_id": "Payment ID", "amount": "Amount (₹)", "risk_score": "Risk Score",
            "risk_level": "Risk Level", "recovery_probability": "Recovery Prob.",
            "failure_reason": "Root Cause", "recommended_action": "Recommended Action",
            "expected_value": "Expected Value (₹)",
        }),
        use_container_width=True, height=520,
    )
