"""
Generates exportable recovery reports from the audit trail — the kind of
artifact you'd attach to a buildathon submission or send to a stakeholder.
"""

import json
import os
from datetime import datetime, timezone

from config import settings
from src.audit.audit_logger import read_audit_trail
from src.analytics.metrics import compute_summary


def generate_report():
    df = read_audit_trail()
    summary = compute_summary(df)

    os.makedirs(settings.REPORTS_DIR, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    csv_path = os.path.join(settings.REPORTS_DIR, f"audit_trail_{stamp}.csv")
    json_path = os.path.join(settings.REPORTS_DIR, f"summary_{stamp}.json")

    df.to_csv(csv_path, index=False)
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Audit trail exported -> {csv_path}")
    print(f"Summary exported -> {json_path}")
    return csv_path, json_path


if __name__ == "__main__":
    generate_report()
