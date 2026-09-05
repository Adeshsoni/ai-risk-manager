import os

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split


DATA_PATH = "data/transactions.csv"
MODEL_PATH = "models/fraud_model.pkl"

FEATURES = [
    "amount",
    "hour",
    "transactions_last_hour",
    "is_new_device",
    "is_international",
    "failed_attempts"
]


def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            "Dataset not found. Run generate_data.py first."
        )

    os.makedirs("models", exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df["is_fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_split=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print("\nModel Evaluation")
    print("=" * 50)
    print(classification_report(y_test, predictions))

    try:
        auc = roc_auc_score(y_test, probabilities)
        print(f"ROC-AUC Score: {auc:.4f}")
    except ValueError:
        print("ROC-AUC could not be calculated.")

    model_package = {
        "model": model,
        "features": FEATURES
    }

    joblib.dump(model_package, MODEL_PATH)

    print(f"\nModel saved successfully to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
