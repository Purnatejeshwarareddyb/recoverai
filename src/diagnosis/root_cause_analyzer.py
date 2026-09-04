"""
Module 3: Root Cause Intelligence.

Combines the already-known structured failure_reason (rules layer) with a
human-readable explanation (the "LLM reasoning" layer). In this offline
project the explanation is template-based so the system runs with zero
external API dependency; src.diagnosis.llm_explainer can be swapped in
to call a real LLM for the same explain(row) contract.

Principle enforced here: this module only ever RECOMMENDS / EXPLAINS.
It never authorizes money movement -- that is the Policy Engine's job.
"""

EXPLANATIONS = {
    "BANK_TECHNICAL_FAILURE": "The customer's bank had a temporary technical issue. "
                               "These usually resolve on their own -- a delayed retry is highly effective.",
    "NETWORK_FAILURE": "The payment failed due to a network/connectivity issue during authorization. "
                        "A short-delay retry is typically sufficient.",
    "INSUFFICIENT_FUNDS": "The customer did not have sufficient balance at the time of the attempt. "
                           "Immediate retries rarely help; a reminder timed for payday works better.",
    "EXPIRED_PAYMENT_METHOD": "The saved card/UPI mandate had expired. The customer needs a fresh "
                               "payment link rather than a retry on the same instrument.",
    "REPEATED_DECLINE": "This payment has failed multiple times already, which usually signals a "
                         "deeper issue (fraud check, blocked card, wrong details). Escalation is safer than more retries.",
    "CUSTOMER_ABANDONMENT": "The customer started checkout but did not complete it. A well-timed "
                             "reminder or an easier payment link is more effective than a silent retry.",
    "UNKNOWN": "The failure reason could not be classified with confidence. Treat cautiously and "
               "prefer low-cost, low-risk interventions until more signal is available.",
}


def diagnose(row) -> dict:
    reason = row["failure_reason"]
    return {
        "root_cause": reason,
        "explanation": EXPLANATIONS.get(reason, EXPLANATIONS["UNKNOWN"]),
    }
