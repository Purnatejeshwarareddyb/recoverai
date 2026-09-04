# RecoverAI
### Autonomous Revenue Recovery Intelligence System

> RecoverAI does not attempt to recover every failed payment. It identifies
> where intervention creates the highest expected financial value, selects
> a safe recovery strategy, and knows when to stop.

Built for Razorpay Buildathon — Track 03 (AI Revenue Recovery).
100% Python. No HTML/CSS/JavaScript. Built and run entirely from PyCharm Community.

---

## Why this is more than "retry a failed payment"

Most systems: `Payment Failed → Send Reminder → Retry`.

RecoverAI:

```
Payment Event → Revenue Risk Detection → Recoverability Prediction (ML)
   → Root Cause Diagnosis → Intervention Selection
   → Expected Recovery Value Calculation → Safety/Policy Validation
   → Execute Recovery Workflow (simulated) → Observe Outcome
   → Update Metrics → Full Audit Trail
```

The intellectual core is the **Expected Recovery Value** engine:

```
Expected Recovery Value = (Amount × P(recover)) − Intervention Cost − Risk Cost
```

The AI only spends recovery effort where the math says it's worth it, and a
separate, deterministic **Policy Engine** — not the model or any LLM — has
final say over what's allowed to execute (max retries, high-value approval,
minimum probability thresholds, customer-contact limits).

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/generate_data.py  # 1,000 synthetic payment events
python scripts/train.py          # trains + compares LogisticRegression vs RandomForest
python scripts/run_pipeline.py   # runs the full batch through the pipeline, writes audit trail

streamlit run app/app.py         # launches the dashboard
```

Optional: drop a PNG at `app/assets/recoverai_logo.png` before launching to
show your own logo in the sidebar instead of the plain text title.

## Dashboard pages

| Page | Purpose |
|---|---|
| Executive Overview | Total transactions, revenue at risk/recovered, recovery rate |
| Revenue Risk Queue | Every at-risk payment, ranked by expected recovery value |
| Recovery Decision | Full step-by-step AI reasoning for one transaction |
| Recovery Execution | Live run of the workflow for a chosen payment |
| Audit Trail | Every decision the system has ever made, filterable |
| Model Performance | Accuracy / precision / recall / F1 / ROC-AUC / confusion matrix |

## Architecture

Five modules, each with a single responsibility:

1. **Revenue Risk Detector** (`src/risk`) — rule-based risk scoring, cheap first pass.
2. **Recoverability Predictor** (`src/ml`) — ML model (Logistic Regression vs Random Forest, best selected by ROC-AUC).
3. **Root Cause Intelligence** (`src/diagnosis`) — explains *why* a payment is at risk. Recommends, never authorizes.
4. **Recovery Strategy Engine** (`src/recovery`) — picks the action with the highest expected value.
5. **Safety & Policy Engine** (`src/policy`) — the only module allowed to approve real execution. Enforces hard limits from `config/policy_config.py`.

Every decision — approved or blocked — is written to SQLite via `src/audit/audit_logger.py`.

## Testing

```bash
pip install pytest
pytest tests/ -v
```

## Adding your own logo

Drop a PNG at `app/assets/recoverai_logo.png` and the sidebar will use it
automatically. If the file isn't there, the app falls back to a plain text
title — nothing breaks either way.

## Project structure

```
recoverai/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── config/
│   ├── settings.py            # paths, dataset size, random seed
│   ├── model_config.py        # ML hyperparameters, thresholds
│   └── policy_config.py       # hard safety boundaries (max retries, etc.)
│
├── data/
│   ├── raw/                   # synthetic_payment_events.csv (generated)
│   ├── processed/
│   └── models/                # recoverability_model.pkl, model_metrics.json (generated)
│
├── database/
│   ├── database.py            # SQLite connection + schema init
│   ├── models.py              # AuditRecord dataclass (schema documentation)
│   └── recoverai.db           # generated on first pipeline run
│
├── src/
│   │
│   ├── ingestion/
│   │   └── payment_loader.py          # loads raw payment CSV
│   │
│   ├── preprocessing/
│   │   └── feature_engineering.py     # one-hot encoding, feature alignment
│   │
│   ├── risk/
│   │   └── risk_detector.py           # Module 1: rule-based risk scoring
│   │
│   ├── ml/
│   │   ├── train_model.py             # Module 2: trains + compares LR vs RF
│   │   ├── evaluate_model.py          # standalone holdout re-evaluation
│   │   ├── predict_recoverability.py  # Module 2: inference
│   │   └── model_manager.py           # load/save/archive model bundles
│   │
│   ├── diagnosis/
│   │   ├── root_cause_analyzer.py     # Module 3: explains root cause
│   │   └── diagnosis_rules.py         # deterministic rule table
│   │
│   ├── recovery/
│   │   ├── strategy_engine.py         # Module 4: picks best action
│   │   ├── expected_value.py          # Expected Recovery Value math
│   │   ├── retry_manager.py           # per-payment retry/backoff tracking
│   │   └── recovery_executor.py       # orchestrates the full per-payment pipeline
│   │
│   ├── policy/
│   │   ├── policy_engine.py           # Module 5: approves/blocks actions
│   │   ├── retry_policy.py            # focused retry-limit checks
│   │   └── escalation_policy.py       # focused escalation checks
│   │
│   ├── simulation/
│   │   └── outcome_simulator.py       # simulates RECOVERED/FAILED/NOT_ATTEMPTED
│   │
│   ├── audit/
│   │   └── audit_logger.py            # writes/reads the SQLite audit trail
│   │
│   ├── analytics/
│   │   ├── metrics.py                 # executive summary aggregation
│   │   └── recovery_report.py         # exports audit trail + summary to CSV/JSON
│   │
│   └── utils/
│       └── helpers.py                 # shared Streamlit data-loading helpers
│
├── app/
│   ├── app.py                  # Streamlit entry point (sidebar nav + logo)
│   ├── assets/
│   │   └── recoverai_logo.png  # optional — add your own logo here
│   │
│   └── views/                  # named "views", not "pages" -- see note below
│       ├── overview.py             # Page 1: Executive Overview
│       ├── risk_queue.py           # Page 2: Revenue Risk Queue
│       ├── recovery_decision.py    # Page 3: Recovery Decision drill-down
│       ├── execution.py            # Page 4: Recovery Execution (live run)
│       ├── audit_trail.py          # Page 5: Audit Trail
│       └── model_performance.py    # Page 6: Model Performance
│
├── tests/
│   ├── test_policy.py
│   ├── test_recovery.py
│   ├── test_risk.py
│   ├── test_recoverability.py
│   └── test_simulation.py
│
├── scripts/
│   ├── generate_data.py       # python scripts/generate_data.py
│   ├── train.py                # python scripts/train.py
│   └── run_pipeline.py         # python scripts/run_pipeline.py
│
├── docs/
│   ├── architecture.md
│   ├── methodology.md
│   ├── safety.md
│   └── decisions.md
│
└── outputs/
    ├── reports/     # CSV/JSON exports from recovery_report.py
    ├── charts/
    └── audit_logs/
```

> **Note on `app/views/` vs `app/pages/`:** the folder is intentionally named
> `views`, not `pages`. Streamlit automatically turns any folder named
> `pages/` sitting next to the entry script into its own native multi-page
> navigation, which conflicts with this project's custom sidebar nav in
> `app.py` and causes a `StreamlitDuplicateElementId` crash. Don't rename it
> back to `pages/`.
