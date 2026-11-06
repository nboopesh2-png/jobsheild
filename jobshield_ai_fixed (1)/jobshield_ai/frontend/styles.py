"""
Enterprise Cybersecurity Design System & CSS Styling for JobShield AI.
Features a dark navy blue palette, cyber glow accents, custom cards, and shield icons.
"""

def get_shield_svg(size: int = 40) -> str:
    """Generates an inline SVG for the JobShield verified security emblem."""
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#00F0FF" />
                <stop offset="50%" stop-color="#7928CA" />
                <stop offset="100%" stop-color="#0080FF" />
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <!-- Outer Shield -->
        <path d="M50 8 L85 24 V52 C85 72 50 92 50 92 C50 92 15 72 15 52 V24 L50 8 Z"
              fill="#0D152D" stroke="url(#shieldGrad)" stroke-width="4" filter="url(#glow)"/>
        <!-- Inner Accent -->
        <path d="M50 16 L78 29 V50 C78 66 50 82 50 82 C50 82 22 66 22 50 V29 L50 16 Z"
              fill="#141E3C" opacity="0.6"/>
        <!-- Verified Checkmark -->
        <path d="M38 50 L46 58 L64 40"
              stroke="#00FF9D" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """

CYBER_CSS = """
<style>
/* Global Dark Theme Settings */
.stApp {
    background-color: #0A0F24;
    color: #E2E8F0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #0B132B !important;
    border-right: 1px solid #1E293B;
}

/* Custom Card Container */
.cyber-card {
    background: linear-gradient(145deg, #121B36 0%, #0E162C 100%);
    border: 1px solid #1F2E54;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
}

.cyber-card:hover {
    border-color: #00F0FF;
    box-shadow: 0 10px 30px rgba(0, 240, 255, 0.15);
}

/* Metric Display Cards */
.metric-box {
    background: #111A35;
    border-left: 4px solid #00F0FF;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 8px 0;
}

.metric-title {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94A3B8;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 4px;
}

/* Status Badges */
.badge-danger {
    background-color: rgba(255, 0, 85, 0.15);
    color: #FF0055;
    border: 1px solid #FF0055;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}

.badge-warning {
    background-color: rgba(255, 170, 0, 0.15);
    color: #FFAA00;
    border: 1px solid #FFAA00;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}

.badge-success {
    background-color: rgba(0, 255, 157, 0.15);
    color: #00FF9D;
    border: 1px solid #00FF9D;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}

/* Glow Text */
.glow-text-cyan {
    color: #00F0FF;
    text-shadow: 0 0 12px rgba(0, 240, 255, 0.5);
}

.glow-text-purple {
    color: #B794F4;
    text-shadow: 0 0 12px rgba(183, 148, 244, 0.5);
}

/* Streamlit Button Styling */
div.stButton > button {
    background: linear-gradient(135deg, #1C2E5C 0%, #0F1C3F 100%);
    color: #FFFFFF;
    border: 1px solid #38B6FF;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #00F0FF 0%, #7928CA 100%);
    color: #FFFFFF;
    border-color: #00F0FF;
    box-shadow: 0 0 16px rgba(0, 240, 255, 0.4);
    transform: translateY(-2px);
}

/* Input Fields */
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background-color: #0B132B !important;
    border: 1px solid #23355C !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within {
    border-color: #00F0FF !important;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.25) !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    background-color: transparent !important;
    color: #94A3B8 !important;
    font-weight: 600;
    border-bottom: 2px solid transparent !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #00F0FF !important;
    border-bottom: 2px solid #00F0FF !important;
}

/* Footer Container */
.cyber-footer {
    border-top: 1px solid #1E293B;
    padding-top: 24px;
    margin-top: 48px;
    color: #64748B;
    font-size: 0.85rem;
    text-align: center;
}
</style>
"""
