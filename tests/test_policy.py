import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.policy.policy_engine import evaluate_policy
from config import policy_config as pc


def make_row(**overrides):
    row = {
        "payment_id": "P1", "amount": 5000, "recovery_probability": 0.6,
        "retry_attempts": 0,
    }
    row.update(overrides)
    return row


def test_low_probability_blocks_recovery():
    row = make_row(recovery_probability=0.05)
    result = evaluate_policy(row, "RETRY", expected_value=100)
    assert result["approved"] is False
    assert result["final_action"] == "STOP_RECOVERY"


def test_high_value_requires_escalation():
    row = make_row(amount=pc.HIGH_VALUE_APPROVAL_THRESHOLD + 1)
    result = evaluate_policy(row, "GENERATE_PAYMENT_LINK", expected_value=500)
    assert result["approved"] is False
    assert result["final_action"] == "ESCALATE"


def test_max_retries_forces_escalation():
    row = make_row(retry_attempts=pc.MAX_AUTOMATIC_RECOVERY_ATTEMPTS)
    result = evaluate_policy(row, "RETRY", expected_value=500)
    assert result["final_action"] == "ESCALATE"


def test_healthy_case_is_approved():
    row = make_row()
    result = evaluate_policy(row, "SEND_REMINDER", expected_value=500)
    assert result["approved"] is True
    assert result["final_action"] == "SEND_REMINDER"
