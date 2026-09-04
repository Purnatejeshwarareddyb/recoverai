"""
Safety and policy configuration.
These are the hard boundaries the AI is NOT allowed to cross on its own —
the "Responsible AI for financial systems" layer described in the design doc.
"""

# The AI may never attempt more automatic recovery actions than this
# for a single payment before it must escalate to a human / stop.
MAX_AUTOMATIC_RECOVERY_ATTEMPTS = 3

# Any single transaction above this amount cannot be auto-executed —
# it is routed to ESCALATE for human approval regardless of model confidence.
HIGH_VALUE_APPROVAL_THRESHOLD = 100_000  # INR

# Below this recovery probability, the policy engine refuses to spend
# any further money/effort recovering the payment.
MIN_RECOVERY_PROBABILITY = 0.15

# Below this expected recovery value (INR), intervening is not worth it,
# even if probability is technically nonzero.
MIN_EXPECTED_VALUE = 0

# Do not contact / retry the same customer more than this many times
# within a rolling window — protects customers from being spammed.
MAX_CONTACTS_PER_CUSTOMER = 3

# Every single decision the AI makes must be written to the audit trail.
AUDIT_EVERY_DECISION = True
