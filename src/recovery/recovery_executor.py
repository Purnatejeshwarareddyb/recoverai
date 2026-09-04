"""
Orchestrates the complete per-payment recovery pipeline described in the
architecture:

Risk Detection -> Recoverability Prediction -> Root Cause -> Strategy ->
Expected Value -> Policy Validation -> Execution (simulated) -> Audit
"""

from src.diagnosis.root_cause_analyzer import diagnose
from src.recovery.strategy_engine import recommend_strategy
from src.policy.policy_engine import evaluate_policy
from src.simulation.outcome_simulator import simulate_outcome
from src.audit.audit_logger import log_decision


def process_payment(row: dict, contact_count_so_far: int = 0, seed: int = None) -> dict:
    """row must already contain risk_score/risk_level and recovery_probability."""
    diagnosis = diagnose(row)
    strategy = recommend_strategy(row)
    policy = evaluate_policy(
        row,
        recommended_action=strategy["recommended_action"],
        expected_value=strategy["expected_value"],
        contact_count_so_far=contact_count_so_far,
    )
    outcome = simulate_outcome(row["recovery_probability"], policy["final_action"], seed=seed)

    record = {
        "payment_id": row["payment_id"],
        "customer_id": row["customer_id"],
        "amount": row["amount"],
        "risk_score": row["risk_score"],
        "risk_level": row["risk_level"],
        "root_cause": diagnosis["root_cause"],
        "recovery_probability": row["recovery_probability"],
        "model_used": row.get("model_used", "N/A"),
        "recommended_action": strategy["recommended_action"],
        "expected_value": strategy["expected_value"],
        "policy_approved": policy["approved"],
        "final_action": policy["final_action"],
        "policy_reasons": policy["reasons"],
        "outcome": outcome,
    }

    log_decision(record)
    record["explanation"] = diagnosis["explanation"]
    record["all_candidate_actions"] = strategy["all_candidate_actions"]
    return record
