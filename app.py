import os

import joblib
import pandas as pd
import streamlit as st

from utils.risk_engine import calculate_decision, calculate_rule_risk
from utils.explainer import explain_transaction
from utils.audit_logger import log_transaction, get_recent_transactions


st.set_page_config(
    page_title="AI Risk Manager",
    page_icon="🛡️",
    layout="wide"
)


@st.cache_resource
def load_model():
    model_path = "models/fraud_model.pkl"

    if not os.path.exists(model_path):
        return None

    return joblib.load(model_path)


model_package = load_model()


st.title("🛡️ AI Risk Manager")

st.markdown(
    """
    ### Intelligent Transaction Risk Detection

    Analyze transaction patterns using **Machine Learning + Rule-Based Risk Signals**
    and receive an explainable risk decision.
    """
)

st.divider()


if model_package is None:

    st.warning(
        "⚠️ Machine learning model not found."
    )

    st.info(
        """
        Run the following commands first:

        1. `python generate_data.py`
        2. `python train_model.py`
        """
    )

    st.stop()


model = model_package["model"]
features = model_package["features"]


st.subheader("💳 Transaction Details")


col1, col2 = st.columns(2)


with col1:

    amount = st.number_input(
        "Transaction Amount (₹)",
        min_value=1.0,
        value=1000.0,
        step=100.0
    )

    hour = st.slider(
        "Transaction Hour",
        min_value=0,
        max_value=23,
        value=12
    )

    transactions_last_hour = st.slider(
        "Transactions in Last Hour",
        min_value=0,
        max_value=20,
        value=1
    )


with col2:

    is_new_device = st.selectbox(
        "New Device?",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    is_international = st.selectbox(
        "International Transaction?",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    failed_attempts = st.slider(
        "Failed Authentication Attempts",
        min_value=0,
        max_value=10,
        value=0
    )


st.divider()


if st.button("🔍 Analyze Transaction", use_container_width=True):

    input_data = pd.DataFrame([{
        "amount": amount,
        "hour": hour,
        "transactions_last_hour": transactions_last_hour,
        "is_new_device": is_new_device,
        "is_international": is_international,
        "failed_attempts": failed_attempts
    }])

    input_data = input_data[features]

    ml_probability = float(
        model.predict_proba(input_data)[0][1]
    )

    rule_score, rule_signals = calculate_rule_risk(
        amount,
        hour,
        transactions_last_hour,
        is_new_device,
        is_international,
        failed_attempts
    )

    ml_score = ml_probability * 100

    # Hybrid score: ML + rule-based intelligence
    final_probability = (
        (ml_score * 0.70) +
        (rule_score * 0.30)
    ) / 100

    risk_score, decision = calculate_decision(
        final_probability
    )

    reasons = explain_transaction(
        amount,
        hour,
        transactions_last_hour,
        is_new_device,
        is_international,
        failed_attempts,
        ml_probability
    )

    log_transaction(
        amount,
        hour,
        transactions_last_hour,
        is_new_device,
        is_international,
        failed_attempts,
        ml_probability,
        risk_score,
        decision
    )

    st.divider()

    st.subheader("📊 Risk Analysis Result")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Final Risk Score",
            f"{risk_score}%"
        )

    with metric2:
        st.metric(
            "ML Fraud Probability",
            f"{ml_probability:.2%}"
        )

    with metric3:

        if decision == "APPROVE":
            st.success("🟢 APPROVE")

        elif decision == "REVIEW":
            st.warning("🟡 REVIEW")

        else:
            st.error("🔴 BLOCK")

    st.divider()

    st.subheader("🔍 Risk Explanation")

    for reason in reasons:
        st.write(f"• {reason}")

    if rule_signals:

        st.subheader("⚠️ Rule-Based Risk Signals")

        for signal in rule_signals:
            st.write(f"• {signal}")

    st.success(
        "Transaction analysis saved to audit log."
    )


st.divider()


st.subheader("🕒 Recent Transaction Analysis")

recent_transactions = get_recent_transactions(limit=10)

if recent_transactions:

    recent_df = pd.DataFrame(
        recent_transactions,
        columns=[
            "Timestamp",
            "Amount",
            "Risk Score",
            "Decision"
        ]
    )

    st.dataframe(
        recent_df,
        use_container_width=True
    )

else:

    st.info(
        "No transactions analyzed yet."
    )
