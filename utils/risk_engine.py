def calculate_decision(probability):
    """
    Convert fraud probability into a risk score and decision.
    """

    risk_score = round(float(probability) * 100, 2)

    if risk_score < 30:
        decision = "APPROVE"
    elif risk_score < 70:
        decision = "REVIEW"
    else:
        decision = "BLOCK"

    return risk_score, decision


def calculate_rule_risk(
    amount,
    hour,
    transactions_last_hour,
    is_new_device,
    is_international,
    failed_attempts
):
    """
    Rule-based secondary risk score.
    Used alongside the ML model for additional safety signals.
    """

    score = 0
    signals = []

    if amount > 10000:
        score += 20
        signals.append("High transaction amount")

    if 0 <= hour <= 5:
        score += 15
        signals.append("Unusual transaction hour")

    if transactions_last_hour > 8:
        score += 20
        signals.append("High transaction velocity")

    if is_new_device == 1:
        score += 10
        signals.append("New device detected")

    if is_international == 1:
        score += 10
        signals.append("International transaction")

    if failed_attempts >= 3:
        score += 25
        signals.append("Multiple failed attempts")

    return min(score, 100), signals
