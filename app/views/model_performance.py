import json
import os
import streamlit as st
import pandas as pd
from config import settings


def render():
    st.title(" Model Performance")
    st.caption("Recoverability Predictor — Logistic Regression vs Random Forest")

    if not os.path.exists(settings.MODEL_METRICS_PATH):
        st.warning(
            "No trained model yet. Run `python scripts/train.py` "
            "from the project root, then reload this page."
        )
        return

    with open(settings.MODEL_METRICS_PATH) as f:
        metrics = json.load(f)

    st.success(f"Selected model: **{metrics['selected_model']}** (highest ROC-AUC)")

    rows = []
    for name, m in metrics["candidates"].items():
        rows.append({
            "Model": name, "Accuracy": m["accuracy"], "Precision": m["precision"],
            "Recall": m["recall"], "F1 Score": m["f1_score"], "ROC-AUC": m["roc_auc"],
        })
    st.dataframe(pd.DataFrame(rows).set_index("Model"), use_container_width=True)

    st.subheader("Confusion Matrix")
    chosen = metrics["candidates"][metrics["selected_model"]]
    cm = chosen["confusion_matrix"]
    cm_df = pd.DataFrame(
        cm, index=["Actual: Not Recovered", "Actual: Recovered"],
        columns=["Predicted: Not Recovered", "Predicted: Recovered"],
    )
    st.table(cm_df)

    st.subheader("ROC Curve")
    roc = chosen["roc_curve"]
    roc_df = pd.DataFrame({"False Positive Rate": roc["fpr"], "True Positive Rate": roc["tpr"]})
    st.line_chart(roc_df.set_index("False Positive Rate"))
