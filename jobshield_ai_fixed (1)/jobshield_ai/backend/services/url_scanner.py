"""
URL Security & Phishing Scanner for JobShield AI.
Inspects suspicious TLDs, IP hosts, typo-squatting, and queries VirusTotal API.
"""
import re
import urllib.parse
from typing import Dict, Any, List
import requests
from backend.config import VIRUSTOTAL_API_KEY

SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".gq", ".click",
    ".buzz", ".club", ".work", ".fit", ".icu", ".link", ".live",
    ".cam", ".monster", ".rest", ".online", ".site"
}

POPULAR_BRANDS = ["tcs", "infosys", "wipro", "google", "amazon", "microsoft", "zoho", "cognizant", "accenture"]

def scan_url_security(url: str) -> Dict[str, Any]:
    """
    Performs comprehensive cybersecurity inspection on job application links.
    """
    if not url:
        return {
            "url": "",
            "domain": "",
            "is_suspicious_tld": False,
            "is_ip_address": False,
            "typo_squatting_detected": False,
            "matched_legit_company": None,
            "virustotal_malicious": 0,
            "risk_score": 0.0,
            "risk_level": "Low",
            "verdict": "Empty URL provided.",
            "details": ["No URL specified."]
        }

    # Normalize URL
    target_url = url.strip()
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    parsed = urllib.parse.urlparse(target_url)
    domain = parsed.netloc.lower()
    if ":" in domain:
        domain = domain.split(":")[0]

    details: List[str] = []
    risk_score = 0.0

    # 1. Check IP address as host
    is_ip = bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain))
    if is_ip:
        risk_score += 60.0
        details.append("Critical: Host uses a raw IP address instead of an authenticated domain name.")

    # 2. Check Suspicious TLDs
    is_suspicious_tld = any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS)
    if is_suspicious_tld:
        matched_tld = next(tld for tld in SUSPICIOUS_TLDS if domain.endswith(tld))
        risk_score += 35.0
        details.append(f"High risk: Domain uses '{matched_tld}', a top-level domain frequently associated with phishing.")

    # 3. Check Brand Impersonation / Typo-squatting
    typo_squatting_detected = False
    matched_brand = None
    for brand in POPULAR_BRANDS:
        if brand in domain and not (domain.endswith(f"{brand}.com") or domain.endswith(f"{brand}.jobs")):
            typo_squatting_detected = True
            matched_brand = brand
            risk_score += 55.0
            details.append(
                f"Impersonation Alert: Domain '{domain}' contains '{brand}' but is NOT an official enterprise domain."
            )
            break

    # 4. Check for URL shortening services
    shorteners = ["bit.ly", "tinyurl.com", "t.ly", "rb.gy", "cutt.ly", "is.gd"]
    if any(s in domain for s in shorteners):
        risk_score += 30.0
        details.append("Caution: Link is shortened to mask the true destination web address.")

    # 5. External VirusTotal API Check (if configured)
    vt_malicious_count = 0
    if VIRUSTOTAL_API_KEY:
        try:
            import base64
            url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
            headers = {"x-apikey": VIRUSTOTAL_API_KEY}
            resp = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=5)
            if resp.status_code == 200:
                stats = resp.json().get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                vt_malicious_count = stats.get("malicious", 0)
                if vt_malicious_count > 0:
                    risk_score += (vt_malicious_count * 20.0)
                    details.append(f"VirusTotal Security Alert: Flagged malicious by {vt_malicious_count} security engines.")
        except Exception:
            pass  # Fall back smoothly to heuristic engine

    risk_score = round(min(risk_score, 100.0), 1)

    if risk_score >= 60.0:
        risk_level = "High / Critical"
        verdict = "DANGEROUS / MALICIOUS LINK"
    elif risk_score >= 25.0:
        risk_level = "Medium"
        verdict = "SUSPICIOUS URL"
    else:
        risk_level = "Low"
        verdict = "SAFE / REPUTABLE URL"
        if not details:
            details.append("No obvious security anomalies detected on this domain.")

    return {
        "url": target_url,
        "domain": domain,
        "is_suspicious_tld": is_suspicious_tld,
        "is_ip_address": is_ip,
        "typo_squatting_detected": typo_squatting_detected,
        "matched_legit_company": matched_brand,
        "virustotal_malicious": vt_malicious_count,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "verdict": verdict,
        "details": details
    }
