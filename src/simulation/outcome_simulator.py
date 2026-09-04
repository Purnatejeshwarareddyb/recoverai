"""
Since no real merchant money or gateway is involved, outcomes are simulated
using the recovery_probability as the chance of success -- with a small
action-quality multiplier so the choice of strategy actually matters.
"""

import numpy as np

ACTION_EFFECTIVENESS_MULTIPLIER = {
    "RETRY": 1.00,
    "WAIT": 0.95,
    "SEND_REMINDER": 1.05,
    "GENERATE_PAYMENT_LINK": 1.10,
    "ESCALATE": 1.15,
    "STOP_RECOVERY": 0.0,
}


def simulate_outcome(probability: float, action: str, seed: int = None) -> str:
    if action == "STOP_RECOVERY":
        return "NOT_ATTEMPTED"

    rng = np.random.default_rng(seed)
    effective_p = min(probability * ACTION_EFFECTIVENESS_MULTIPLIER.get(action, 1.0), 0.99)
    return "RECOVERED" if rng.random() < effective_p else "FAILED"
