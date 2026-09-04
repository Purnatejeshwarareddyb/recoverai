import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.recovery.expected_value import expected_value, best_action_by_value


def test_high_value_high_probability_is_positive():
    ev = expected_value(amount=50000, probability=0.80, action="SEND_REMINDER")
    assert ev > 0


def test_low_value_low_probability_is_negative():
    ev = expected_value(amount=500, probability=0.10, action="ESCALATE")
    assert ev < 0


def test_best_action_picks_highest_ev():
    best, all_scored = best_action_by_value(
        amount=10000, probability=0.7,
        candidate_actions=["RETRY", "SEND_REMINDER", "ESCALATE", "STOP_RECOVERY"]
    )
    assert best["action"] in ["RETRY", "SEND_REMINDER", "ESCALATE", "STOP_RECOVERY"]
    assert all_scored[0]["expected_value"] >= all_scored[-1]["expected_value"]
