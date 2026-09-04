import streamlit as st
from src.utils.helpers import get_scored_payments, format_inr
from src.recovery.recovery_executor import process_payment


def render():
    st.title("Recovery Execution")
    st.caption("Run the full pipeline for one payment and watch the workflow unfold")

    df = get_scored_payments()
    payment_id = st.selectbox("Select a payment to execute", df["payment_id"].tolist(), key="exec_select")
    row = df[df["payment_id"] == payment_id].iloc[0].to_dict()

    if st.button("▶ Run Recovery Workflow", type="primary"):
        steps = st.container()
        with steps:
            st.write("**① Action Initiated** — payment queued for recovery evaluation")
            record = process_payment(row)

            st.write("**② Safety Check** — Policy Engine evaluated the recommendation")
            if record["policy_approved"]:
                st.success(f"Passed → action approved as `{record['final_action']}`")
            else:
                st.warning(f"Blocked/redirected → final action `{record['final_action']}`")
                for r in record["policy_reasons"]:
                    st.caption(f"• {r}")

            st.write(f"**③ Recovery Attempt** — executing `{record['final_action']}` (simulated)")

            st.write("**④ Outcome**")
            if record["outcome"] == "RECOVERED":
                st.success(f" RECOVERED — {format_inr(record['amount'])} recovered")
            elif record["outcome"] == "FAILED":
                st.error(" FAILED — recovery attempt did not succeed")
            else:
                st.info("⏹ NOT ATTEMPTED — policy determined recovery was not worthwhile")

            st.write("**⑤ Next Decision**")
            if record["outcome"] == "FAILED" and row["retry_attempts"] < 2:
                st.write("→ Eligible for another recovery cycle on next pipeline run.")
            elif record["final_action"] == "ESCALATE":
                st.write("→ Routed to a human agent for manual follow-up.")
            else:
                st.write("→ Case closed. Logged permanently to the audit trail.")

        st.markdown("---")
        st.json(record, expanded=False)
    else:
        st.info("Select a payment and click **Run Recovery Workflow** to see the live pipeline.")
