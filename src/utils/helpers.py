"""Small shared helpers used across the Streamlit pages."""

import streamlit as st
from src.audit.audit_logger import read_audit_trail
from src.ingestion.payment_loader import load_raw_payments
from src.risk.risk_detector import detect_risk
from src.ml.predict_recoverability import predict_recovery_probability


@st.cache_data(ttl=30)
def get_audit_trail():
    return read_audit_trail()


@st.cache_data
def get_scored_payments():
    """Full pipeline scoring (risk + ML) without executing recovery — used
    by the Risk Queue and Recovery Decision pages."""
    df = load_raw_payments()
    df = detect_risk(df)
    df = predict_recovery_probability(df)
    return df


def format_inr(value: float) -> str:
    return f"₹{value:,.0f}"
