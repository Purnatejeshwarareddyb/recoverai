# Safety Design

RecoverAI is a financial-decision system, so it is built around one rule:

> **No model — ML or LLM — is ever allowed to directly authorize an action
> that spends money or contacts a customer.**

## The approval chain

```
AI Recommendation (ML + rules + explanation)
            │
            ▼
      Policy Engine   ← deterministic, config-driven, no learning
            │
     ┌──────┴──────┐
  APPROVED       BLOCKED
     │               │
   Execute      Escalate / Stop
```

Only `src/policy/policy_engine.py` can turn a recommendation into an
executed action, and it does so using fixed rules from
`config/policy_config.py` — not model confidence, not an LLM's judgment.

## Hard boundaries enforced

| Boundary | Config value | Effect |
|---|---|---|
| Max automatic recovery attempts | `MAX_AUTOMATIC_RECOVERY_ATTEMPTS = 3` | Beyond this, cases are escalated to a human, never auto-retried indefinitely |
| High-value approval threshold | `HIGH_VALUE_APPROVAL_THRESHOLD = ₹100,000` | Any transaction at or above this always requires human approval |
| Minimum recovery probability | `MIN_RECOVERY_PROBABILITY = 0.15` | Below this, no further recovery effort is spent |
| Minimum expected value | `MIN_EXPECTED_VALUE = 0` | Negative-EV actions are never auto-approved |
| Max customer contacts | `MAX_CONTACTS_PER_CUSTOMER = 3` | Customers can't be repeatedly messaged by an over-eager system |

## Auditability

Every decision — approved or blocked — is written to the `audit_trail` table
via `src/audit/audit_logger.py`, including the policy reasons as free text.
Nothing the system does is silent; every action can be traced back to the
exact rule that allowed or blocked it.

## Why this matters for a payments company

A system that can decide *not* to act is safer than one that always acts.
RecoverAI's default posture is conservative: intervention has to clear a
positive expected-value bar and pass every safety check before anything
happens. When in doubt, the system escalates to a human rather than guessing.
