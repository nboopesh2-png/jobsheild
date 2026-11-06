"""
Cybersecurity Rule-Based Heuristic Detection Engine for Recruitment Fraud.
Matches structured linguistic patterns, financial solicitation, suspicious channels,
urgency tactics, and bilingual fraud indicators.
"""
import re
from typing import List, Dict, Any

RULES_DEFINITIONS = [
    # 1. Financial Demands
    {
        "id": "RULE_FEE_DEMAND",
        "name": "Upfront Payment or Deposit Demand",
        "severity": "critical",
        "points": 35,
        "patterns": [
            r"(?i)\b(registration|processing|verification|caution|security|training|admission|application|interview|courier|uniform|biometric)\s*(fee|charges?|amount|deposit|money)\b",
            r"(?i)\b(refundable\s*deposit|pay\s*rs\.?|transfer\s*rs\.?|deposit\s*rs\.?|send\s*rs\.?)\b",
            r"(?i)\b(pay|transfer|send|deposit)\s*(₹|\$|rs\.?)\s*\d+",
            r"(?i)(முன்பணம்|பதிவுக்\s*கட்டணம்|பயிற்சிக்\s*கட்டணம்|வைப்புத்\s*தொகை)"
        ],
        "description": "Legitimate employers never demand application, registration, uniform, or security deposit fees."
    },
    {
        "id": "RULE_PAYMENT_CHANNELS",
        "name": "Non-Corporate Payment Channel (UPI / Crypto)",
        "severity": "critical",
        "points": 30,
        "patterns": [
            r"(?i)\b(upi|gpay|google\s*pay|phonepe|paytm|qr\s*code|crypto|bitcoin|usdt|binance)\b",
            r"[\w\.\-]+@(okaxis|okhdfcbank|okicici|oksbi|ybl|ibl|paytm|upi)\b",
            r"(?i)(ஜிபே|போன்பே|பேடிஎம்|கிரிப்டோ)"
        ],
        "description": "Asking candidates to transfer funds via personal UPI IDs or cryptocurrency is a definitive fraud indicator."
    },

    # 2. Channel Redirection
    {
        "id": "RULE_TELEGRAM_REDIRECTION",
        "name": "Telegram Redirection Scheme",
        "severity": "high",
        "points": 25,
        "patterns": [
            r"(?i)\b(t\.me\/|telegram\s*(app|channel|group|handle|id|chat)|contact.*on\s*telegram|join.*telegram)\b",
            r"@[a-zA-Z0-9_]+.*telegram",
            r"(?i)(டெலிகிராம்)"
        ],
        "description": "Scammers redirect victims to anonymous Telegram channels to coordinate fraudulent tasks and extortion."
    },
    {
        "id": "RULE_WHATSAPP_ONLY_HIRING",
        "name": "Unverified WhatsApp-Only Recruitment",
        "severity": "medium",
        "points": 15,
        "patterns": [
            r"(?i)\b(wa\.me\/|whatsapp\s*only|contact.*via\s*whatsapp|whatsapp\s*hr|send.*screenshot.*whatsapp)\b",
            r"(?i)(வாட்ஸ்அப்)"
        ],
        "description": "Exclusive recruitment communication via WhatsApp without an enterprise ATS or corporate email domain."
    },

    # 3. Unrealistic Compensation & Task Scams
    {
        "id": "RULE_TASK_SCAM",
        "name": "Paid Social Task / Video Liking Scam",
        "severity": "critical",
        "points": 35,
        "patterns": [
            r"(?i)\b(like\s*youtube\s*videos|product\s*rating|hotel\s*review|google\s*map\s*review|daily\s*payout|instant\s*payout)\b",
            r"(?i)\b(earn\s*(rs\.?|₹|\$)\s*[0-9,]+\s*(daily|per\s*day|per\s*page))\b",
            r"(?i)\b(recharge.*return|vip\s*task|commission\s*per\s*task)\b"
        ],
        "description": "Promising daily payouts for liking videos or writing reviews is the hallmark of task refund investment scams."
    },
    {
        "id": "RULE_NO_INTERVIEW",
        "name": "No Interview Direct Appointment Lure",
        "severity": "high",
        "points": 20,
        "patterns": [
            r"(?i)\b(no\s*interview|without\s*(any\s*)?interview|direct\s*selection|direct\s*placement|exempt\s*from\s*(test|interview)|instant\s*appointment)\b",
            r"(?i)(நேர்முகத்\s*தேர்வு\s*இல்லை|தேர்வு\s*இல்லாமல்)"
        ],
        "description": "Reputable enterprises never issue employment offers without thorough technical or behavioral assessments."
    },

    # 4. Urgency & Pressure Tactics
    {
        "id": "RULE_URGENCY_TACTIC",
        "name": "Artificial High-Pressure Urgency",
        "severity": "medium",
        "points": 15,
        "patterns": [
            r"(?i)\b(offer\s*(expires|valid)\s*(in\s*\d+|today|within\s*24\s*hours|immediately)|limited\s*seats|last\s*chance|hurry\s*up|pay\s*within\s*\d+\s*(hours?|mins?))\b",
            r"(?i)(உடனே\s*இணையுங்கள்|இன்றே\s*கடைசி|உடனடி\s*வாய்ப்பு)"
        ],
        "description": "Fraudsters create false urgency to pressure candidates into transferring money before verifying the offer."
    },

    # 5. Generic Impersonation Signals
    {
        "id": "RULE_GENERIC_SALUTATION",
        "name": "Generic Anonymous Recipient",
        "severity": "low",
        "points": 10,
        "patterns": [
            r"(?i)\b(dear\s*(candidate|applicant|job\s*seeker|aspirant|friend))\b"
        ],
        "description": "Mass spam campaigns often use impersonal salutations instead of candidate-specific identifiers."
    }
]

def evaluate_rules(text: str) -> List[Dict[str, Any]]:
    """
    Evaluates raw offer text against cybersecurity heuristic rules.
    Returns matched rules with severity, points, and matched text snippets.
    """
    matched_flags = []

    for rule in RULES_DEFINITIONS:
        for pattern in rule["patterns"]:
            match = re.search(pattern, text)
            if match:
                matched_flags.append({
                    "rule": rule["name"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "match_text": match.group(0),
                    "points": rule["points"]
                })
                break  # avoid multiple triggers for same rule

    return matched_flags
