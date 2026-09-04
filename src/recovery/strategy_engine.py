"""
Module 4: Recovery Strategy Engine.

Chooses ONE recommended action for a payment based on root cause,
recovery probability, retry history, and expected value.
"""

from src.recovery.expected_value import best_action_by_value

# Which actions are even plausible given the root cause
ACTIONS_BY_REASON = {
    "BANK_TECHNICAL_FAILURE": ["WAIT", "RETRY", "STOP_RECOVERY"],
    "NETWORK_FAILURE": ["RETRY", "WAIT", "STOP_RECOVERY"],
    "INSUFFICIENT_FUNDS": ["SEND_REMINDER", "WAIT", "STOP_RECOVERY"],
    "EXPIRED_PAYMENT_METHOD": ["GENERATE_PAYMENT_LINK", "SEND_REMINDER", "STOP_RECOVERY"],
    "REPEATED_DECLINE": ["ESCALATE", "STOP_RECOVERY"],
    "CUSTOMER_ABANDONMENT": ["SEND_REMINDER", "GENERATE_PAYMENT_LINK", "STOP_RECOVERY"],
    "UNKNOWN": ["SEND_REMINDER", "STOP_RECOVERY"],
}


def recommend_strategy(row) -> dict:
    reason = row["failure_reason"]
    probability = row["recovery_probability"]
    amount = row["amount"]
    retry_attempts = row["retry_attempts"]

    candidates = list(ACTIONS_BY_REASON.get(reason, ["SEND_REMINDER", "STOP_RECOVERY"]))

    # If the customer has already been retried a lot, drop RETRY as an option
    if retry_attempts >= 3 and "RETRY" in candidates:
        candidates.remove("RETRY")
        if "ESCALATE" not in candidates:
            candidates.append("ESCALATE")

    best, all_scored = best_action_by_value(amount, probability, candidates)

    return {
        "recommended_action": best["action"],
        "expected_value": best["expected_value"],
        "all_candidate_actions": all_scored,
    }
