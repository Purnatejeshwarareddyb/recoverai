# Methodology

## Synthetic data

Real merchant/customer payment data isn't available, so `scripts/generate_data.py`
builds a structurally realistic dataset of 1,000 payment events:

- **Amount** — log-normal distribution, clipped to ₹50–₹500,000, matching the
  long-tail shape of real transaction sizes.
- **Failure reason** — sampled from 7 categories with hand-set probabilities
  reflecting typical failure-mode frequency in payment gateways.
- **Ground-truth recovery probability** — a function of failure reason,
  payment method, retry count, prior failures, transaction recency, and
  customer activity, plus Gaussian noise. This is what the ML model has to
  learn back out from the observed features — it is *not* given directly
  to the model.
- **`recovered` label** — a Bernoulli draw using that ground-truth probability,
  which becomes the ML training target.

A fixed random seed (`config/settings.RANDOM_SEED = 42`) makes every run
reproducible.

## Model selection

Two classifiers are trained on identical train/test splits (75/25, stratified
on the label):

- **Logistic Regression** — a simple, highly interpretable baseline.
- **Random Forest** — captures non-linear interactions between features.

Both are scored on Accuracy, Precision, Recall, F1, and ROC-AUC. The model
with the higher ROC-AUC is selected and persisted; both sets of metrics are
saved so the Model Performance dashboard page can show the comparison, not
just the winner.

## Expected Recovery Value

```
Expected Recovery Value = (Amount × P(recover)) − Intervention Cost − Risk Cost
```

- **Intervention Cost** — a fixed, per-action cost (`config/settings.INTERVENTION_COST`)
  representing operational cost (SMS/email cost, gateway retry fee, agent time
  for escalation, etc).
- **Risk Cost** — a small carrying cost proportional to amount and to
  `(1 − probability)`, representing the ongoing cost of revenue sitting
  unresolved.

This number, not the raw probability, is what the Strategy Engine optimizes
for. A payment with a 90% recovery probability but a tiny amount can still
lose to a payment with 40% probability and a large amount.

## Policy validation

The Policy Engine is deliberately dumb and deterministic — no ML, no LLM —
because financial safety boundaries should not depend on a model's judgment.
It checks, in order: minimum recovery probability, minimum expected value,
maximum automatic retry attempts, high-value approval threshold, and
maximum customer contacts. Any failed check downgrades the action to
`ESCALATE` or `STOP_RECOVERY` and records why.

## Simulation

Since no real gateway is used, `outcome_simulator.py` draws a Bernoulli
outcome using the model's recovery probability, adjusted by a small
per-action effectiveness multiplier (e.g. a payment link is slightly more
effective than a bare retry for an abandoned checkout). This keeps the
choice of action meaningfully connected to the simulated result rather than
being purely cosmetic.
