import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.risk.risk_detector import score_row, risk_level


def make_row(**overrides):
    row = {
        "failure_reason": "BANK_TECHNICAL_FAILURE", "retry_attempts": 0,
        "prior_failures": 0, "hours_since_failure": 5, "amount": 1000,
    }
    row.update(overrides)
    return row


def test_repeated_decline_scores_higher_than_technical_failure():
    technical = score_row(make_row(failure_reason="BANK_TECHNICAL_FAILURE"))
    declined = score_row(make_row(failure_reason="REPEATED_DECLINE"))
    assert declined > technical


def test_more_retries_increases_risk_score():
    low = score_row(make_row(retry_attempts=0))
    high = score_row(make_row(retry_attempts=5))
    assert high > low


def test_risk_level_buckets():
    assert risk_level(0.9) == "HIGH"
    assert risk_level(0.5) == "MEDIUM"
    assert risk_level(0.1) == "LOW"


def test_score_never_exceeds_one():
    row = make_row(failure_reason="REPEATED_DECLINE", retry_attempts=10,
                    prior_failures=10, hours_since_failure=200, amount=1_000_000)
    assert score_row(row) <= 1.0
