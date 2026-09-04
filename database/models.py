"""
Lightweight dataclass representations of database rows.

The project uses raw SQLite (see database.py) rather than a full ORM to
keep the dependency footprint minimal, but these dataclasses document the
schema in one place and give callers a typed object to work with when
they don't want to deal with raw tuples/dicts.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AuditRecord:
    event_time: str
    payment_id: str
    customer_id: str
    amount: float
    risk_score: float
    risk_level: str
    root_cause: str
    recovery_probability: float
    model_used: str
    recommended_action: str
    expected_value: float
    policy_approved: bool
    final_action: str
    policy_reasons: str  # JSON-encoded list
    outcome: str
    id: Optional[int] = None
