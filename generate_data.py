import os
import random

import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

os.makedirs("data", exist_ok=True)

data = []

for transaction_id in range(1, 5001):
    amount = round(float(np.random.exponential(scale=2500)), 2)
    amount = min(amount, 50000)

    hour = random.randint(0, 23)
    transactions_last_hour = random.randint(0, 15)
    is_new_device = random.choice([0, 1])
    is_international = random.choice([0, 1])
    failed_attempts = random.randint(0, 5)

    fraud_probability = 0.02

    if amount > 10000:
        fraud_probability += 0.20

    if 0 <= hour <= 5:
        fraud_probability += 0.15

    if transactions_last_hour > 8:
        fraud_probability += 0.20

    if is_new_device:
        fraud_probability += 0.10

    if is_international:
        fraud_probability += 0.10

    if failed_attempts >= 3:
        fraud_probability += 0.25

    fraud_probability = min(fraud_probability, 0.95)

    is_fraud = int(np.random.random() < fraud_probability)

    data.append({
        "transaction_id": transaction_id,
        "amount": amount,
        "hour": hour,
        "transactions_last_hour": transactions_last_hour,
        "is_new_device": is_new_device,
        "is_international": is_international,
        "failed_attempts": failed_attempts,
        "is_fraud": is_fraud
    })

df = pd.DataFrame(data)

df.to_csv("data/transactions.csv", index=False)

print("Dataset created successfully!")
print(f"Total transactions: {len(df)}")
print("\nClass distribution:")
print(df["is_fraud"].value_counts())
