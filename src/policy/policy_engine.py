"""
Module 5: Safety and Policy Engine.

This is the ONLY module allowed to turn an AI recommendation into an
approved, executable action. It enforces hard financial and customer-
protection boundaries defined in config/policy_config.py.
"""

from config import policy_config as pc


def evaluate_policy(row: dict, recommended_action: str, expected_value: float,
                     contact_count_so_far: int = 0) -> dict:
    """
    Returns a decision dict:
        {approved: bool, final_action: str, reasons: [str, ...]}
    """
    reasons = []
    approved = True
    final_action = recommended_action

    probability = row["recovery_probability"]
    amount = row["amount"]
    retry_attempts = row["retry_attempts"]

    if probability < pc.MIN_RECOVERY_PROBABILITY:
        approved = False
        final_action = "STOP_RECOVERY"
        reasons.append(
            f"Recovery probability {probability:.2f} is below minimum threshold "
            f"{pc.MIN_RECOVERY_PROBABILITY}."
        )

    if expected_value < pc.MIN_EXPECTED_VALUE:
        approved = False
        final_action = "STOP_RECOVERY"
        reasons.append(f"Expected recovery value {expected_value} is not positive.")

    if retry_attempts >= pc.MAX_AUTOMATIC_RECOVERY_ATTEMPTS and recommended_action == "RETRY":
        approved = False
        final_action = "ESCALATE"
        reasons.append(
            f"Maximum automatic recovery attempts "
            f"({pc.MAX_AUTOMATIC_RECOVERY_ATTEMPTS}) reached; escalating instead of auto-retrying."
        )

    if amount >= pc.HIGH_VALUE_APPROVAL_THRESHOLD and recommended_action not in ("STOP_RECOVERY",):
        approved = False
        final_action = "ESCALATE"
        reasons.append(
            f"Transaction amount ₹{amount:,.0f} exceeds high-value auto-approval "
            f"threshold ₹{pc.HIGH_VALUE_APPROVAL_THRESHOLD:,.0f}; requires human approval."
        )

    if contact_count_so_far >= pc.MAX_CONTACTS_PER_CUSTOMER and recommended_action in (
        "SEND_REMINDER", "GENERATE_PAYMENT_LINK"
    ):
        approved = False
        final_action = "STOP_RECOVERY"
        reasons.append(
            f"Customer already contacted {contact_count_so_far} times; "
            f"will not contact again (customer-protection policy)."
        )

    if not reasons:
        reasons.append("All policy checks passed.")

    return {
        "approved": approved,
        "final_action": final_action,
        "recommended_action": recommended_action,
        "reasons": reasons,
    }
