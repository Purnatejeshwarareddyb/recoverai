"""
Deterministic classification rules used as a fallback/cross-check against
the raw failure_reason field. Kept separate from root_cause_analyzer.py so
the rule table can be audited, tested, and extended independently of the
explanation text.
"""

# (condition description, function(row) -> bool, resulting root cause)
# Applied in order; first match wins. Falls back to row['failure_reason'].
RULES = [
    (
        "Many rapid retries with no success",
        lambda row: row["retry_attempts"] >= 3,
        "REPEATED_DECLINE",
    ),
    (
        "Long time elapsed with a technical failure reason",
        lambda row: row["failure_reason"] in ("BANK_TECHNICAL_FAILURE", "NETWORK_FAILURE")
        and row["hours_since_failure"] > 72,
        "UNKNOWN",  # a technical issue that persists this long is probably something else
    ),
]


def apply_rules(row: dict) -> str:
    for _, condition, result in RULES:
        if condition(row):
            return result
    return row["failure_reason"]
