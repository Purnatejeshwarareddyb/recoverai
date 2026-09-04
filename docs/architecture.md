# RecoverAI Architecture

## Pipeline

```
                    PAYMENT DATA
                         │
                         ▼
                 DATA INGESTION            src/ingestion/payment_loader.py
                         │
                         ▼
               REVENUE RISK ENGINE         src/risk/risk_detector.py
                         │
                         ▼
             RECOVERABILITY ML MODEL       src/ml/predict_recoverability.py
                         │
                         ▼
              ROOT CAUSE INTELLIGENCE      src/diagnosis/root_cause_analyzer.py
                         │
                         ▼
             RECOVERY STRATEGY ENGINE      src/recovery/strategy_engine.py
                         │
                         ▼
           EXPECTED RECOVERY VALUE ENGINE  src/recovery/expected_value.py
                         │
                         ▼
              SAFETY POLICY ENGINE         src/policy/policy_engine.py
                    │         │
                APPROVED     BLOCKED
                    │         │
                    ▼         ▼
             RECOVERY       ESCALATE
             EXECUTION       / STOP
                    │
                    ▼
             OUTCOME ENGINE                src/simulation/outcome_simulator.py
                    │
                    ▼
              AUDIT SYSTEM                 src/audit/audit_logger.py
                    │
                    ▼
             METRICS ENGINE                src/analytics/metrics.py
                    │
                    ▼
           PYTHON STREAMLIT UI             app/app.py
```

## Design principles

1. **The LLM/rules layer never controls money.** `root_cause_analyzer.py`
   only explains and recommends. Only `policy_engine.py` can approve execution.
2. **Every decision is auditable.** `audit_logger.py` writes every prediction,
   recommendation, policy verdict, and outcome to SQLite — nothing is silent.
3. **Value-driven, not failure-driven.** The system doesn't ask "did this
   fail?" — it asks "is intervening here worth it?" via Expected Recovery Value.
4. **Hard safety boundaries live in one place.** `config/policy_config.py` —
   max retries, high-value approval threshold, minimum probability, contact
   limits. Change policy without touching any engine code.
5. **Reproducible.** Fixed random seed (`config/settings.py`) means the
   synthetic dataset, the train/test split, and the simulated outcomes are
   consistent across runs and across evaluators.
