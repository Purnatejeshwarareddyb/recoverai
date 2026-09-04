import streamlit as st
from src.utils.helpers import get_audit_trail


def render():
    st.title(" Audit Trail")
    st.caption("Every AI decision, fully logged and explainable")

    df = get_audit_trail()
    if df.empty:
        st.warning(
            "No audit records yet. Run `python scripts/run_pipeline.py` "
            "from the project root, then reload this page."
        )
        return

    col1, col2 = st.columns(2)
    with col1:
        action_filter = st.multiselect(
            "Final action", options=sorted(df["final_action"].unique()),
            default=sorted(df["final_action"].unique())
        )
    with col2:
        outcome_filter = st.multiselect(
            "Outcome", options=sorted(df["outcome"].unique()),
            default=sorted(df["outcome"].unique())
        )

    filtered = df[df["final_action"].isin(action_filter) & df["outcome"].isin(outcome_filter)]

    st.write(f"**{len(filtered)}** audit records")

    display_cols = [
        "event_time", "payment_id", "recovery_probability", "model_used",
        "recommended_action", "policy_approved", "final_action", "outcome",
    ]
    st.dataframe(
        filtered[display_cols].rename(columns={
            "event_time": "Time", "payment_id": "Payment ID",
            "recovery_probability": "AI Prediction", "model_used": "Model",
            "recommended_action": "Recommended", "policy_approved": "Policy Approved",
            "final_action": "Final Action", "outcome": "Outcome",
        }),
        use_container_width=True, height=500,
    )

    with st.expander("Inspect a single record's full reasoning"):
        if len(filtered):
            pid = st.selectbox("Payment ID", filtered["payment_id"].tolist())
            rec = filtered[filtered["payment_id"] == pid].iloc[0]
            st.write(f"**Root cause:** {rec['root_cause']}")
            st.write(f"**Policy reasons:** {rec['policy_reasons']}")
