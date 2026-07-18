"""
Simple illustrative premium calculator.
NOTE: This is a simplified educational model, not an actuarial pricing engine.
"""

BASE_RATE_PER_1000 = {
    "term": 1.2,       # cheapest, pure protection
    "endowment": 3.5,  # protection + savings
    "health": 2.0,     # health/medical cover
}


def _age_loading(age: int) -> float:
    if age < 25:
        return 1.0
    if age < 35:
        return 1.15
    if age < 45:
        return 1.4
    if age < 55:
        return 1.8
    return 2.5


def calculate_premium(age: int, sum_assured: float, term_years: int, plan_type: str, smoker: bool):
    plan_type = plan_type.lower()
    base_rate = BASE_RATE_PER_1000.get(plan_type, BASE_RATE_PER_1000["term"])

    age_factor = _age_loading(age)
    smoker_factor = 1.5 if smoker else 1.0
    term_factor = max(0.8, 1.0 - (term_years / 100))  # longer term -> slightly lower per-year rate

    base_annual_premium = (sum_assured / 1000) * base_rate
    risk_loading = age_factor * smoker_factor
    annual_premium = base_annual_premium * risk_loading * term_factor

    breakdown = {
        "base_annual_premium": round(base_annual_premium, 2),
        "age_factor": age_factor,
        "smoker_factor": smoker_factor,
        "term_factor": round(term_factor, 3),
        "plan_type": plan_type,
    }

    return {
        "estimated_annual_premium": round(annual_premium, 2),
        "estimated_monthly_premium": round(annual_premium / 12, 2),
        "risk_loading_applied": round(risk_loading, 2),
        "breakdown": breakdown,
    }
