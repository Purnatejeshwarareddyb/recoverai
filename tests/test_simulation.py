import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simulation.outcome_simulator import simulate_outcome


def test_stop_recovery_is_never_attempted():
    outcome = simulate_outcome(probability=0.9, action="STOP_RECOVERY", seed=1)
    assert outcome == "NOT_ATTEMPTED"


def test_high_probability_recovers_more_often_than_low():
    seeds = range(50)
    high_recovered = sum(
        1 for s in seeds if simulate_outcome(0.95, "SEND_REMINDER", seed=s) == "RECOVERED"
    )
    low_recovered = sum(
        1 for s in seeds if simulate_outcome(0.05, "SEND_REMINDER", seed=s) == "RECOVERED"
    )
    assert high_recovered > low_recovered


def test_outcome_is_one_of_expected_values():
    outcome = simulate_outcome(0.5, "RETRY", seed=7)
    assert outcome in ("RECOVERED", "FAILED", "NOT_ATTEMPTED")
