"""Focused policy checks for when a case must go to a human agent."""

from config import policy_config as pc


def requires_escalation(amount: float, retry_attempts: int, recovery_probability: float) -> bool:
    if amount >= pc.HIGH_VALUE_APPROVAL_THRESHOLD:
        return True
    if retry_attempts >= pc.MAX_AUTOMATIC_RECOVERY_ATTEMPTS:
        return True
    return False


def escalation_reason(amount: float, retry_attempts: int) -> str:
    reasons = []
    if amount >= pc.HIGH_VALUE_APPROVAL_THRESHOLD:
        reasons.append(f"High-value transaction (₹{amount:,.0f})")
    if retry_attempts >= pc.MAX_AUTOMATIC_RECOVERY_ATTEMPTS:
        reasons.append(f"Max automatic attempts reached ({retry_attempts})")
    return "; ".join(reasons) if reasons else "N/A"
