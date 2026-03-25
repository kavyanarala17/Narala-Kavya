def detect_hallucination(agreement_percentage):

    if agreement_percentage >= 90:
        return "Low"

    elif agreement_percentage >= 60:
        return "Medium"

    else:
        return "High"
    
def calculate_trust_score(agreement_percentage, hallucination_risk, evidence):

    score = 0

    # Agreement weight
    score += agreement_percentage * 0.5

    # Hallucination weight
    if hallucination_risk == "Low":
        score += 30
    elif hallucination_risk == "Medium":
        score += 20
    else:
        score += 10

    # Evidence weight
    if evidence["evidence"] != "No evidence found":
        score += 20

    return round(score,2)