import streamlit as st
from src.utils.helpers import get_scored_payments, format_inr
from src.diagnosis.root_cause_analyzer import diagnose
from src.recovery.strategy_engine import recommend_strategy
from src.policy.policy_engine import evaluate_policy


def render():
    st.title(" Recovery Decision")
    st.caption("Full AI reasoning trail for a single transaction")

    df = get_scored_payments()
    payment_id = st.selectbox("Select a payment", df["payment_id"].tolist())
    row = df[df["payment_id"] == payment_id].iloc[0].to_dict()

    st.markdown("### 1️⃣ Payment Information")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Amount", format_inr(row["amount"]))
    c2.metric("Method", row["payment_method"])
    c3.metric("Retry Attempts", int(row["retry_attempts"]))
    c4.metric("Prior Failures", int(row["prior_failures"]))

    st.markdown("### 2️⃣ AI Risk Analysis")
    st.write(f"**Risk Score:** {row['risk_score']:.2f}  |  **Risk Level:** {row['risk_level']}")

    st.markdown("### 3️⃣ Recovery Probability")
    st.progress(min(row["recovery_probability"], 1.0))
    st.write(f"**{row['recovery_probability']:.1%}** chance of recovery (model: {row['model_used']})")

    st.markdown("### 4️⃣ Root Cause")
    diagnosis = diagnose(row)
    st.info(f"**{diagnosis['root_cause']}** — {diagnosis['explanation']}")

    st.markdown("### 5️⃣ Recommended Strategy")
    strategy = recommend_strategy(row)
    st.write(f"**Recommended action:** `{strategy['recommended_action']}`")
    with st.expander("See all candidate actions ranked by expected value"):
        for c in strategy["all_candidate_actions"]:
            st.write(f"- `{c['action']}` → {format_inr(c['expected_value'])}")

    st.markdown("### 6️⃣ Expected Recovery Value")
    st.metric("Expected Value", format_inr(strategy["expected_value"]))

    st.markdown("### 7️⃣ Policy Validation")
    policy = evaluate_policy(row, strategy["recommended_action"], strategy["expected_value"])
    if policy["approved"]:
        st.success(f"✅ Approved — final action: `{policy['final_action']}`")
    else:
        st.error(f"⛔ Not auto-approved — final action: `{policy['final_action']}`")
    for reason in policy["reasons"]:
        st.write(f"- {reason}")

    st.markdown("### 8️⃣ Final Decision")
    st.success(f"**{policy['final_action']}**")
