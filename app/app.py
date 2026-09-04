"""
RecoverAI -- Autonomous Revenue Recovery Intelligence System
Streamlit entry point.

Run from the project root:
    streamlit run app/app.py
"""

import sys
import os
import importlib
import streamlit as st

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

st.set_page_config(
    page_title="RecoverAI",
    page_icon=None,
    layout="wide",
)

LOGO_PATH = os.path.join(PROJECT_ROOT, "app", "assets", "recoverai_logo.png")

if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
else:
    # Falls back cleanly if no logo has been added to app/assets/
    st.sidebar.title("RecoverAI")
    st.sidebar.caption("Autonomous Revenue Recovery Intelligence System")

st.sidebar.markdown("---")

PAGES = {
    "Executive Overview": "overview",
    "Revenue Risk Queue": "risk_queue",
    "Recovery Decision": "recovery_decision",
    "Recovery Execution": "execution",
    "Audit Trail": "audit_trail",
    "Model Performance": "model_performance",
}

choice = st.sidebar.radio("Navigate", list(PAGES.keys()))

st.sidebar.markdown("---")
st.sidebar.info(
    "RecoverAI does not attempt to recover every failed payment. "
    "It identifies where intervention creates the highest expected "
    "financial value, selects a safe recovery strategy, and knows "
    "when to stop."
)

module_name = PAGES[choice]
module = importlib.import_module(f"app.views.{module_name}")
module.render()
