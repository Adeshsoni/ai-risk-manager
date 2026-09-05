import os

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from utils.risk_engine import calculate_decision, calculate_rule_risk
from utils.explainer import explain_transaction
from utils.audit_logger import log_transaction


app = FastAPI(
    title="AI Risk Manager API",
    description=(
        "AI-powered transaction risk detection API using "
        "Machine Learning and rule-based risk signals."
    ),
    version="1.0.0"
)


MODEL_PATH = "models/fraud_model.pkl"


class Transaction(BaseModel):
    amount: float = Field(..., gt=0)
    hour: int = Field(..., ge=0, le=23)
    transactions_last_hour: int = Field(..., ge=0)
    is_new_device: int = Field(..., ge=0, le=1)
    is_international: int = Field(..., ge=0, le=1)
    failed_attempts: int = Field(..., ge=0)


def load_model():
    if not os.path.exists(MODEL_PATH):
        return None

    return joblib.load(MODEL_PATH)


@app.get("/")
def home():
    return {
        "message": "AI Risk Manager API is running",
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    model = load_model()

    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/analyze")
def analyze_transaction(transaction: Transaction):

    model_package = load_model()

    if model_package is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Model not found. "
                "Run generate_data.py and train_model.py first."
            )
        )

    model = model_package["model"]
    features = model_package["features"]

    transaction_data = {
        "amount": transaction.amount,
        "hour": transaction.hour,
        "transactions_last_hour":
            transaction.transactions_last_hour,
        "is_new_device": transaction.is_new_device,
        "is_international": transaction.is_international,
        "failed_attempts": transaction.failed_attempts
    }

    input_data = pd.DataFrame([transaction_data])
    input_data = input_data[features]

    ml_probability = float(
        model.predict_proba(input_data)[0][1]
    )

    rule_score, rule_signals = calculate_rule_risk(
        transaction.amount,
        transaction.hour,
        transaction.transactions_last_hour,
        transaction.is_new_device,
        transaction.is_international,
        transaction.failed_attempts
    )

    ml_score = ml_probability * 100

    final_probability = (
        (ml_score * 0.70) +
        (rule_score * 0.30)
    ) / 100

    risk_score, decision = calculate_decision(
        final_probability
    )

    reasons = explain_transaction(
        transaction.amount,
        transaction.hour,
        transaction.transactions_last_hour,
        transaction.is_new_device,
        transaction.is_international,
        transaction.failed_attempts,
        ml_probability
    )

    log_transaction(
        transaction.amount,
        transaction.hour,
        transaction.transactions_last_hour,
        transaction.is_new_device,
        transaction.is_international,
        transaction.failed_attempts,
        ml_probability,
        risk_score,
        decision
    )

    return {
        "transaction": transaction_data,
        "ml_fraud_probability": round(
            ml_probability * 100,
            2
        ),
        "rule_risk_score": rule_score,
        "final_risk_score": risk_score,
        "decision": decision,
        "risk_reasons": reasons,
        "rule_signals": rule_signals
    }
