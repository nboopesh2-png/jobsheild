"""
Company Verification Engine for JobShield AI.
Maintains verified corporate registry, detects look-alike domains and typo-squatting.
"""
import difflib
from typing import Dict, Any, Optional

VERIFIED_ENTERPRISES = [
    {"name": "Tata Consultancy Services (TCS)", "aliases": ["tcs", "tata consultancy"], "domain": "tcs.com", "careers": "https://nextstep.tcs.com"},
    {"name": "Infosys Limited", "aliases": ["infosys"], "domain": "infosys.com", "careers": "https://career.infosys.com"},
    {"name": "Wipro", "aliases": ["wipro limited"], "domain": "wipro.com", "careers": "https://careers.wipro.com"},
    {"name": "Google India", "aliases": ["google", "alphabet"], "domain": "google.com", "careers": "https://careers.google.com"},
    {"name": "Microsoft India", "aliases": ["microsoft"], "domain": "microsoft.com", "careers": "https://careers.microsoft.com"},
    {"name": "Amazon India", "aliases": ["amazon", "aws"], "domain": "amazon.jobs", "careers": "https://amazon.jobs"},
    {"name": "Zoho Corporation", "aliases": ["zoho"], "domain": "zohocorp.com", "careers": "https://www.zohocorp.com/careers"},
    {"name": "Cognizant Technology Solutions", "aliases": ["cognizant", "cts"], "domain": "cognizant.com", "careers": "https://careers.cognizant.com"},
    {"name": "Accenture India", "aliases": ["accenture"], "domain": "accenture.com", "careers": "https://www.accenture.com/in-en/careers"},
    {"name": "HCLTech", "aliases": ["hcl", "hcl technologies"], "domain": "hcltech.com", "careers": "https://www.hcltech.com/careers"},
    {"name": "Tech Mahindra", "aliases": ["tech mahindra"], "domain": "techmahindra.com", "careers": "https://careers.techmahindra.com"},
    {"name": "IBM India", "aliases": ["ibm"], "domain": "ibm.com", "careers": "https://www.ibm.com/careers"},
    {"name": "Flipkart", "aliases": ["flipkart internet"], "domain": "flipkartcareers.com", "careers": "https://www.flipkartcareers.com"},
    {"name": "Swiggy", "aliases": ["swiggy", "bundl technologies"], "domain": "swiggy.com", "careers": "https://careers.swiggy.com"},
    {"name": "Zomato", "aliases": ["zomato"], "domain": "zomato.com", "careers": "https://www.zomato.com/careers"}
]

def verify_company(company_name: str, offered_domain: Optional[str] = None) -> Dict[str, Any]:
    """
    Verifies company authenticity and checks whether the offered website/domain matches the official enterprise domain.
    Detects typo-squatting spoofing attempts.
    """
    if not company_name:
        return {
            "query_company": "",
            "is_verified": False,
            "matched_official_name": None,
            "official_domain": None,
            "careers_url": None,
            "domain_match": False,
            "warning": "No company name provided for verification."
        }

    q = company_name.strip().lower()
    matched = None

    # Search in verified enterprises
    for entry in VERIFIED_ENTERPRISES:
        if q in entry["name"].lower() or any(alias in q for alias in entry["aliases"]):
            matched = entry
            break

    if not matched:
        # Check closest match via difflib
        all_names = [e["name"] for e in VERIFIED_ENTERPRISES]
        close_matches = difflib.get_close_matches(company_name, all_names, n=1, cutoff=0.6)
        if close_matches:
            matched = next(e for e in VERIFIED_ENTERPRISES if e["name"] == close_matches[0])

    if not matched:
        return {
            "query_company": company_name,
            "is_verified": False,
            "matched_official_name": None,
            "official_domain": None,
            "careers_url": None,
            "domain_match": False,
            "warning": f"'{company_name}' is not in the verified tier-1 enterprise registry. Exercise extra vigilance."
        }

    # If domain provided, check for spoofing or typo-squatting
    domain_match = True
    warning = None

    if offered_domain:
        offered = offered_domain.strip().lower()
        official = matched["domain"].lower()

        # Clean protocols/slashes
        for prefix in ["https://", "http://", "www."]:
            if offered.startswith(prefix):
                offered = offered[len(prefix):]
        offered = offered.split("/")[0]

        if official in offered:
            domain_match = True
        else:
            domain_match = False
            # Check typo similarity
            similarity = difflib.SequenceMatcher(None, official, offered).ratio()
            if similarity > 0.65 or matched["aliases"][0] in offered:
                warning = (
                    f"CRITICAL SPOOFING WARNING: The offered domain '{offered_domain}' appears to be a "
                    f"typo-squatted clone of the legitimate enterprise domain '{official}'."
                )
            else:
                warning = f"Domain mismatch: Claimed company uses '{official}', but offer points to '{offered_domain}'."

    return {
        "query_company": company_name,
        "is_verified": True,
        "matched_official_name": matched["name"],
        "official_domain": matched["domain"],
        "careers_url": matched["careers"],
        "domain_match": domain_match,
        "warning": warning
    }
