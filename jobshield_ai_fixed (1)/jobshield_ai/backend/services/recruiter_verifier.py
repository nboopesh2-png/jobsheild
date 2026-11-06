"""
Recruiter Identity & Email Legitimacy Verifier for JobShield AI.
Detects free mail accounts, disposable domains, and brand impersonation.
"""
from typing import Dict, Any, List, Optional

FREE_EMAIL_PROVIDERS = [
    "gmail.com", "yahoo.com", "ymail.com", "rocketmail.com", "hotmail.com",
    "outlook.com", "live.com", "msn.com", "aol.com", "icloud.com",
    "zoho.com", "rediffmail.com", "mail.com", "gmx.com", "proton.me",
    "protonmail.com"
]

DISPOSABLE_PROVIDERS = [
    "mailinator.com", "yopmail.com", "tempmail.com", "10minutemail.com",
    "guerrillamail.com", "throwawaymail.com", "dispostable.com"
]

def verify_recruiter_email(
    email: str,
    claimed_company: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluates recruiter email domain legitimacy and cross-checks corporate claims.
    """
    if not email or "@" not in email:
        return {
            "email": email or "",
            "is_free_provider": False,
            "provider_name": "Unknown",
            "is_disposable": False,
            "domain_matches_company": False,
            "risk_score": 50.0,
            "verdict": "Invalid email address format.",
            "flags": ["Invalid email syntax."]
        }

    email_clean = email.strip().lower()
    local_part, domain = email_clean.split("@", 1)

    is_free = domain in FREE_EMAIL_PROVIDERS
    is_disposable = domain in DISPOSABLE_PROVIDERS

    flags: List[str] = []
    risk_score = 0.0

    if is_disposable:
        flags.append(f"High risk: Recruiter is using a disposable/burner email domain (@{domain}).")
        risk_score += 85.0
    elif is_free:
        flags.append(f"Suspicious: Recruiter is using a free public email provider (@{domain}).")
        risk_score += 45.0
    else:
        flags.append(f"Domain appears to be an enterprise/private domain (@{domain}).")

    domain_matches_company = True
    if claimed_company:
        cmp = claimed_company.lower().replace(" ", "")
        # Check if company name appears in email domain
        if is_free:
            flags.append(
                f"Impersonation Warning: Claiming to represent '{claimed_company}' "
                f"while communicating from a generic @{domain} account is a primary scam technique."
            )
            risk_score += 35.0
            domain_matches_company = False
        elif not any(part in domain for part in [cmp, cmp[:5]]):
            flags.append(
                f"Domain discrepancy: Email domain '@{domain}' does not clearly match claimed company '{claimed_company}'."
            )
            risk_score += 25.0
            domain_matches_company = False

    risk_score = min(risk_score, 100.0)

    if risk_score >= 60.0:
        verdict = "HIGH RECRUITER FRAUD RISK"
    elif risk_score >= 30.0:
        verdict = "SUSPICIOUS SENDER"
    else:
        verdict = "REPUTABLE ENTERPRISE DOMAIN"

    return {
        "email": email,
        "is_free_provider": is_free,
        "provider_name": domain,
        "is_disposable": is_disposable,
        "domain_matches_company": domain_matches_company,
        "risk_score": round(risk_score, 1),
        "verdict": verdict,
        "flags": flags
    }
