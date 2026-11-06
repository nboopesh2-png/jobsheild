"""
Bilingual Localization Engine for JobShield AI.
Full English & Tamil (தமிழ்) translation dictionary for all navigation,
scanners, verdicts, heuristics, and cybersecurity guidance.
"""

TRANSLATIONS = {
    # Common & Navigation
    "app_name": {"en": "JobShield AI", "ta": "ஜாப்ஷீல்ட் ஏஐ"},
    "tagline": {"en": "Detect Fake Offers. Protect Your Future.", "ta": "போலி வேலைவாய்ப்புகளைக் கண்டறிந்து உங்கள் எதிர்காலத்தைப் பாதுகாத்திடுங்கள்."},
    "nav_home": {"en": "Home", "ta": "முகப்பு"},
    "nav_dashboard": {"en": "Dashboard", "ta": "கட்டுப்பாட்டகம்"},
    "nav_text_scanner": {"en": "AI Text Scanner", "ta": "ஏஐ உரை ஸ்கேனர்"},
    "nav_ocr_scanner": {"en": "Screenshot OCR Scanner", "ta": "ஸ்கிரீன்ஷாட் OCR ஸ்கேனர்"},
    "nav_url_scanner": {"en": "URL Security Scanner", "ta": "இணையதள முகவரி ஸ்கேனர்"},
    "nav_verification": {"en": "Company & Recruiter Check", "ta": "நிறுவனம் & பணியமர்த்துபவர் சரிபார்ப்பு"},
    "nav_history": {"en": "Scan History & Reports", "ta": "ஸ்கேன் வரலாறு & அறிக்கைகள்"},
    "nav_community": {"en": "Community Scam Feed", "ta": "சமூக மோசடி எச்சரிக்கைகள்"},
    "nav_admin": {"en": "Admin Control Center", "ta": "நிர்வாகி கட்டுப்பாட்டு மையம்"},
    "nav_login": {"en": "Login / Register", "ta": "உள்நுழைவு / பதிவு"},
    "nav_logout": {"en": "Logout", "ta": "வெளியேறு"},
    "language_selector": {"en": "Language / மொழி", "ta": "மொழி / Language"},

    # Landing Page
    "hero_title": {"en": "Don't Fall for Fake Job Offers.", "ta": "போலி வேலைவாய்ப்பு சலுகைகளில் ஏமாறாதீர்கள்."},
    "hero_subtitle": {
        "en": "Protect your career with AI-powered job and internship fraud detection.",
        "ta": "செயற்கை நுண்ணறிவு மூலம் போலி வேலை மற்றும் பயிற்சி மோசடிகளைக் கண்டறிந்து உங்கள் வாழ்க்கையைப் பாதுகாத்துக் கொள்ளுங்கள்."
    },
    "btn_scan_offer": {"en": "Scan Job Offer Now", "ta": "வேலை சலுகையை இப்போதே ஸ்கேன் செய்"},
    "btn_get_started": {"en": "Get Started", "ta": "தொடங்குங்கள்"},
    "features_title": {"en": "Military-Grade Defense Against Recruitment Fraud", "ta": "வேலைவாய்ப்பு மோசடிக்கு எதிரான நவீன ஏஐ பாதுகாப்பு"},
    "how_it_works_title": {"en": "How JobShield AI Works", "ta": "ஜாப்ஷீல்ட் ஏஐ எவ்வாறு செயல்படுகிறது"},
    "faq_title": {"en": "Frequently Asked Questions", "ta": "அடிக்கடி கேட்கப்படும் கேள்விகள்"},

    # Scanner Terminology
    "paste_offer_placeholder": {
        "en": "Paste email text, WhatsApp / Telegram message, or job offer details here...",
        "ta": "மின்னஞ்சல் உரை, வாட்ஸ்அப் / டெலிகிராம் செய்தி அல்லது வேலை சலுகை விவரங்களை இங்கே ஒட்டவும்..."
    },
    "claimed_company_label": {"en": "Claimed Company Name (Optional)", "ta": "கூறப்படும் நிறுவனத்தின் பெயர் (விருப்பத்திற்குரியது)"},
    "recruiter_email_label": {"en": "Recruiter Email Address (Optional)", "ta": "பணியமர்த்துபவர் மின்னஞ்சல் (விருப்பத்திற்குரியது)"},
    "btn_analyze": {"en": "Analyze with AI Shield", "ta": "ஏஐ மூலம் பகுப்பாய்வு செய்"},
    "btn_load_sample_scam": {"en": "Load Sample Scam (Demo)", "ta": "போலி சலுகை உதாரணத்தை ஏற்று (டெமோ)"},
    "btn_load_sample_genuine": {"en": "Load Genuine Offer (Demo)", "ta": "உண்மையான சலுகை உதாரணத்தை ஏற்று"},

    # Results & Verdicts
    "risk_score_label": {"en": "Composite Risk Score", "ta": "ஒருங்கிணைந்த ஆபத்து மதிப்பெண்"},
    "verdict_label": {"en": "Security Verdict", "ta": "பாதுகாப்பு தீர்ப்பு"},
    "confidence_label": {"en": "AI Model Confidence", "ta": "ஏஐ மாதிரி நம்பகத்தன்மை"},
    "risk_low": {"en": "Low Risk (Legitimate)", "ta": "குறைந்த ஆபத்து (உண்மையானது)"},
    "risk_medium": {"en": "Medium Risk (Caution)", "ta": "நடுத்தர ஆபத்து (எச்சரிக்கை)"},
    "risk_high": {"en": "High / Critical Risk (Scam Alert)", "ta": "அதிக / தீவிர ஆபத்து (மோசடி எச்சரிக்கை)"},
    "export_pdf_btn": {"en": "Download Forensic PDF Audit Report", "ta": "ஆய்வு அறிக்கையை PDF ஆக பதிவிறக்கு"},
    "flagged_signals_title": {"en": "Detected Fraud Indicators & Rules", "ta": "கண்டறியப்பட்ட மோசடி குறிகாட்டிகள்"},
    "safety_advice_title": {"en": "Official Student Safety Advisory", "ta": "மாணவர்களுக்கான அதிகாரப்பூர்வ பாதுகாப்பு ஆலோசனை"}
}

def t(key: str, lang: str = "en") -> str:
    """Translates a UI key to the selected language with fallback to English."""
    item = TRANSLATIONS.get(key)
    if not item:
        return key
    return item.get(lang, item.get("en", key))
