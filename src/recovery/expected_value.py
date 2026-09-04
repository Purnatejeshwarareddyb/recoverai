"""
The intellectual core of RecoverAI: Expected Recovery Value.

    Expected Recovery Value = (Amount * P(recover)) - Intervention Cost - Risk Cost
"""

from config import settings


def expected_value(amount: float, probability: float, action: str) -> float:
    intervention_cost = settings.INTERVENTION_COST.get(action, 0)
    risk_cost = amount * settings.RISK_COST_FACTOR * (1 - probability)
    return round(amount * probability - intervention_cost - risk_cost, 2)


def best_action_by_value(amount: float, probability: float, candidate_actions: list) -> dict:
    """Given a shortlist of feasible actions, pick the one with the highest EV."""
    scored = [
        {"action": a, "expected_value": expected_value(amount, probability, a)}
        for a in candidate_actions
    ]
    scored.sort(key=lambda x: x["expected_value"], reverse=True)
    return scored[0], scored
