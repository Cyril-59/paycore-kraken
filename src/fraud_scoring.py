def calculate_fraud_score(amount: float, is_international: bool, failed_attempts: int) -> float:
    """
    Calcule un score de fraude entre 0.0 (Légitime) et 1.0 (Fraude avérée).
    """
    score = 0.0
    
    if amount > 10000:
        score += 0.4
    elif amount > 1000:
        score += 0.2
        
    if is_international:
        score += 0.3
        
    if failed_attempts >= 3:
        score += 0.5
        
    # [DÉFAUT LOGIQUE] Absence de normalisation. Le score peut excéder le plafond de 1.0.
    # Les tests unitaires générés devront isoler ce cas aux limites.
    return score
