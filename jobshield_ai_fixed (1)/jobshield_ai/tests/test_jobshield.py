"""
Automated Test Suite for JobShield AI.
Verifies AI classification, heuristic rules, company verification, recruiter audit,
URL inspection, password hashing, and PDF generation.
"""
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_ml_model():
    print("[*] Testing AI ML Model Pipeline...")
    from backend.ai.model import get_classifier
    clf = get_classifier()

    scam_sample = "Pay registration fee of Rs. 1500 via UPI to secure job at TCS. Contact on Telegram."
    res_scam = clf.predict(scam_sample)
    assert res_scam["scam_probability"] > 40.0, f"Expected high scam probability, got {res_scam['scam_probability']}"
    assert len(res_scam["scam_indicators"]) > 0, "Expected explainable scam indicators"

    genuine_sample = "Thank you for interviewing with TCS. We are pleased to extend an offer. Check nextstep.tcs.com."
    res_gen = clf.predict(genuine_sample)
    assert res_gen["genuine_probability"] > 40.0, f"Expected high genuine probability, got {res_gen['genuine_probability']}"
    print("  [+] ML Model Pipeline test passed successfully.")

def test_rules_engine():
    print("[*] Testing Heuristic Rules Engine...")
    from backend.ai.rules_engine import evaluate_rules

    # Test fee demand
    text = "Kindly transfer Rs. 2,000 security deposit to confirm your interview."
    flags = evaluate_rules(text)
    assert any("fee" in f["rule"].lower() or "deposit" in f["rule"].lower() for f in flags), "Failed to flag deposit"

    # Test telegram
    text_tg = "Contact HR immediately on Telegram @tcs_hr_group"
    flags_tg = evaluate_rules(text_tg)
    assert any("telegram" in f["rule"].lower() for f in flags_tg), "Failed to flag Telegram"

    # Test Tamil keywords
    text_ta = "முன்பணம் ரூ. 1000 செலுத்தி பணியில் சேரவும்"
    flags_ta = evaluate_rules(text_ta)
    assert len(flags_ta) > 0, "Failed to flag Tamil scam phrase"
    print("  [+] Heuristic Rules Engine test passed successfully.")

def test_recruiter_verifier():
    print("[*] Testing Recruiter Verifier...")
    from backend.services.recruiter_verifier import verify_recruiter_email

    # Free email pretending to be Google
    eval_free = verify_recruiter_email("google.campus.hr@gmail.com", "Google India")
    assert eval_free["is_free_provider"] is True
    assert eval_free["risk_score"] >= 60.0, f"Expected high risk score for fake corporate email, got {eval_free['risk_score']}"

    # Legitimate corporate email
    eval_legit = verify_recruiter_email("recruiter@google.com", "Google India")
    assert eval_legit["is_free_provider"] is False
    assert eval_legit["risk_score"] < 40.0
    print("  [+] Recruiter Verifier test passed successfully.")

def test_company_verifier():
    print("[*] Testing Company Verifier...")
    from backend.services.company_verifier import verify_company

    # Look-alike domain check
    eval_spoof = verify_company("Tata Consultancy Services", "tcs-careers-interview.online")
    assert eval_spoof["is_verified"] is True
    assert eval_spoof["domain_match"] is False
    assert "SPOOFING" in eval_spoof["warning"] or "mismatch" in eval_spoof["warning"].lower()

    # Legitimate domain check
    eval_real = verify_company("Tata Consultancy Services", "nextstep.tcs.com")
    assert eval_real["is_verified"] is True
    assert eval_real["domain_match"] is True
    print("  [+] Company Verifier test passed successfully.")

def test_url_scanner():
    print("[*] Testing URL Security Scanner...")
    from backend.services.url_scanner import scan_url_security

    # Suspicious TLD
    res_tld = scan_url_security("https://fake-amazon-jobs.xyz/apply")
    assert res_tld["is_suspicious_tld"] is True
    assert res_tld["risk_score"] >= 35.0

    # Clean domain
    res_clean = scan_url_security("https://nextstep.tcs.com")
    assert res_clean["risk_score"] < 40.0
    print("  [+] URL Security Scanner test passed successfully.")

def test_password_hashing():
    print("[*] Testing Password Hashing & Security...")
    from backend.auth import hash_password, verify_password

    pw = "SuperSecurePassword@2025"
    hashed = hash_password(pw)
    assert hashed != pw, "Hash should not equal plaintext"
    assert verify_password(pw, hashed) is True, "Password verification failed"
    assert verify_password("WrongPassword", hashed) is False, "False positive in password verification"
    print("  [+] Password Hashing test passed successfully.")

def test_pdf_report_generation():
    print("[*] Testing ReportLab PDF Generation...")
    from backend.services.pdf_generator import generate_pdf_report

    mock_scan_data = {
        "id": 999,
        "scan_type": "text",
        "risk_score": 88.5,
        "risk_level": "High / Critical",
        "verdict": "CONFIRMED RECRUITMENT SCAM",
        "confidence": 94.2,
        "breakdown": {
            "ml_confidence_score": 92.0,
            "heuristic_risk_score": 85.0,
            "recruiter_risk_score": 75.0,
            "company_risk_score": 25.0
        },
        "flags": [
            {"rule": "Upfront Payment Demand", "severity": "critical", "description": "Demanded Rs. 1500 registration fee", "match_text": "Rs. 1500"},
            {"rule": "Telegram Redirection", "severity": "high", "description": "Redirected candidate to Telegram", "match_text": "t.me/fake_hr"}
        ],
        "recommendations": [
            "Never pay money for employment.",
            "Report to cybercrime.gov.in."
        ]
    }
    pdf_bytes = generate_pdf_report(mock_scan_data, "Praveen Kumar")
    assert len(pdf_bytes) > 1000, "PDF byte length suspiciously small"
    assert pdf_bytes.startswith(b"%PDF"), "Generated file does not have valid PDF magic header"
    print("  [+] ReportLab PDF Generation test passed successfully.")

def run_all_tests():
    print("==================================================")
    print("        JOBSHIELD AI COMPREHENSIVE TEST RUN       ")
    print("==================================================")
    test_ml_model()
    test_rules_engine()
    test_recruiter_verifier()
    test_company_verifier()
    test_url_scanner()
    test_password_hashing()
    test_pdf_report_generation()
    print("==================================================")
    print("       ALL JOBSHIELD AI MODULE TESTS PASSED!      ")
    print("==================================================")

if __name__ == "__main__":
    run_all_tests()
