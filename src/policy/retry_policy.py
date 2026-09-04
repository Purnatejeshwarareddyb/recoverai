"""
Focused, single-purpose policy checks for retry behavior. Split out from
the main policy_engine.py so retry rules can be unit-tested and reasoned
about in isolation.
"""

from config import policy_config as pc


def retry_allowed(retry_attempts: int) -> bool:
    return retry_attempts < pc.MAX_AUTOMATIC_RECOVERY_ATTEMPTS


def retry_denial_reason(retry_attempts: int) -> str:
    return (
        f"Retry denied: {retry_attempts} attempts already made, "
        f"maximum is {pc.MAX_AUTOMATIC_RECOVERY_ATTEMPTS}."
    )
