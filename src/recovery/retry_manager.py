"""
Tracks retry counts per payment across a pipeline run so the strategy and
policy engines never exceed configured limits, and provides a single place
to compute backoff timing for WAIT actions.
"""

from config import policy_config as pc

_BACKOFF_MINUTES = [15, 60, 240]  # grows with each successive retry


class RetryManager:
    def __init__(self):
        self._counts = {}

    def count(self, payment_id: str) -> int:
        return self._counts.get(payment_id, 0)

    def can_retry(self, payment_id: str) -> bool:
        return self.count(payment_id) < pc.MAX_AUTOMATIC_RECOVERY_ATTEMPTS

    def record_attempt(self, payment_id: str):
        self._counts[payment_id] = self.count(payment_id) + 1

    def next_backoff_minutes(self, payment_id: str) -> int:
        idx = min(self.count(payment_id), len(_BACKOFF_MINUTES) - 1)
        return _BACKOFF_MINUTES[idx]
