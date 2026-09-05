def explain_transaction(
    amount,
    hour,
    transactions_last_hour,
    is_new_device,
    is_international,
    failed_attempts,
    ml_probability
):
    """
    Generate human-readable explanations for a transaction decision.
    """

    reasons = []

    if amount > 10000:
        reasons.append(
            "High transaction amount compared with normal risk thresholds."
        )

    if 0 <= hour <= 5:
        reasons.append(
            "Transaction occurred during an unusual hour."
        )

    if transactions_last_hour > 8:
        reasons.append(
            "High transaction velocity detected."
        )

    if is_new_device == 1:
        reasons.append(
            "Transaction initiated from a new device."
        )

    if is_international == 1:
        reasons.append(
            "International transaction detected."
        )

    if failed_attempts >= 3:
        reasons.append(
            "Multiple failed authentication attempts detected."
        )

    if ml_probability >= 0.70:
        reasons.append(
            "Machine learning model detected a high probability of fraud."
        )
    elif ml_probability >= 0.30:
        reasons.append(
            "Machine learning model detected moderate transaction risk."
        )

    if not reasons:
        reasons.append(
            "No significant risk indicators were detected."
        )

    return reasons
