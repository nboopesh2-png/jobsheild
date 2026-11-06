"""
Composite Risk Scoring & Verdict Determination Engine for JobShield AI.
Integrates Machine Learning probabilities, heuristic rule flags, and domain/recruiter signals.
"""
from typing import Dict, Any, List

def calculate_composite_risk(
    ml_confidence_score: float,
    heuristic_flags: List[Dict[str, Any]],
    recruiter_risk: float = 0.0,
    company_risk: float = 0.0
) -> Dict[str, Any]:
    """
    Computes weighted composite risk score (0-100) and assigns risk tier and actionable safety advice.
    """
    # Sum heuristic points
    raw_heuristic = sum(flag.get("points", 15) for flag in heuristic_flags)
    heuristic_score = min(float(raw_heuristic), 100.0)

    # Check for critical triggers
    has_critical_flag = any(f.get("severity") == "critical" for f in heuristic_flags)

    # Weighted calculation
    composite = (
        (0.35 * ml_confidence_score) +
        (0.35 * heuristic_score) +
        (0.15 * recruiter_risk) +
        (0.15 * company_risk)
    )

    # If critical flags like upfront fee or personal UPI transfer are present, ensure High Risk tier
    if has_critical_flag:
        composite = max(composite, 75.0)

    # Cap between 0 and 100
    composite_score = round(min(max(composite, 0.0), 100.0), 1)

    # Risk Tier & Verdict
    if composite_score >= 65.0:
        risk_level = "High / Critical"
        verdict = "CONFIRMED RECRUITMENT SCAM - DO NOT PAY OR PROCEED"
    elif composite_score >= 28.0:
        risk_level = "Medium"
        verdict = "SUSPICIOUS OFFER - MANUAL VERIFICATION RECOMMENDED"
    else:
        risk_level = "Low"
        verdict = "OFFER APPEARS LEGITIMATE - VERIFY VIA OFFICIAL PORTAL"

    # Contextual safety recommendations
    recommendations = []
    if has_critical_flag or any("fee" in f.get("rule", "").lower() for f in heuristic_flags):
        recommendations.append("NEVER transfer money: Genuine employers never ask candidates to pay for interviews, tests, IDs, or laptops.")
    if any("telegram" in f.get("rule", "").lower() or "whatsapp" in f.get("rule", "").lower() for f in heuristic_flags):
        recommendations.append("Do not engage via anonymous messaging apps: Official HR communication occurs via verified corporate email domains.")
    if recruiter_risk > 30:
        recommendations.append("Check the sender email address: Legitimate multinational companies do not send job offers from @gmail.com or @yahoo.com.")
    if company_risk > 30:
        recommendations.append("Beware of domain spoofing: Verify the official careers portal directly via Google rather than clicking provided links.")

    # General best practice
    if not recommendations:
        recommendations.append("Always cross-check your offer letter on the employer's official careers portal.")
        recommendations.append("Ensure official emails originate from the registered enterprise domain.")
    else:
        recommendations.append("If money was lost to this scam, immediately report to the National Cyber Crime Portal at cybercrime.gov.in (Toll-Free 1930).")

    return {
        "composite_risk_score": composite_score,
        "risk_level": risk_level,
        "verdict": verdict,
        "breakdown": {
            "ml_confidence_score": round(ml_confidence_score, 1),
            "heuristic_risk_score": round(heuristic_score, 1),
            "recruiter_risk_score": round(recruiter_risk, 1),
            "company_risk_score": round(company_risk, 1),
            "composite_risk_score": composite_score
        },
        "recommendations": recommendations
    }
