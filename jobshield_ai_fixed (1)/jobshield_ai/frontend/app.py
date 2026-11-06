"""
Main Streamlit Application for JobShield AI.
Integrates custom cyber styling, bilingual language switcher, sidebar navigation,
and routes across all 14 cybersecurity modules.
"""
import sys
import os

# Ensure project root is in sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="JobShield AI — Fake Job & Internship Scam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Cyber Dark Theme Styles
from frontend.styles import CYBER_CSS, get_shield_svg
st.markdown(CYBER_CSS, unsafe_allow_html=True)

# 3. Initialize Session State
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "landing"
if "language" not in st.session_state:
    st.session_state["language"] = "en"
if "token" not in st.session_state:
    st.session_state["token"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None

# Local mode only: when no remote API is configured, initialise the local DB here.
# If API_BASE_URL is set (backend hosted on Vercel), the backend seeds its own database.
if not os.getenv("API_BASE_URL"):
    try:
        from backend.main import ensure_initialized
        ensure_initialized()
    except Exception as _init_err:
        st.warning(f"Local database initialisation failed: {_init_err}")

from frontend.i18n import t

# 4. Sidebar Branding & Navigation
with st.sidebar:
    st.markdown(
        f"""<div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            {get_shield_svg(46)}
            <div>
                <h2 style="margin:0; font-size:1.4rem;" class="glow-text-cyan">JobShield AI</h2>
                <small style="color:#94A3B8; font-size:0.75rem;">AI Scam Detection System</small>
            </div>
        </div>""",
        unsafe_allow_html=True
    )

    # Language Switcher
    lang_choice = st.radio(
        t("language_selector", st.session_state["language"]),
        options=["English", "தமிழ்"],
        index=0 if st.session_state["language"] == "en" else 1,
        horizontal=True
    )
    st.session_state["language"] = "en" if lang_choice == "English" else "ta"
    lang = st.session_state["language"]

    st.markdown("<hr style='border-color:#1E293B; margin:12px 0;'>", unsafe_allow_html=True)

    # Navigation Menu
    nav_items = [
        ("landing", "🏠 " + t("nav_home", lang)),
        ("dashboard", "📊 " + t("nav_dashboard", lang)),
        ("text_scanner", "🛡️ " + t("nav_text_scanner", lang)),
        ("ocr_scanner", "📷 " + t("nav_ocr_scanner", lang)),
        ("url_scanner", "🌐 " + t("nav_url_scanner", lang)),
        ("verification", "🏢 " + t("nav_verification", lang)),
        ("history", "📜 " + t("nav_history", lang)),
        ("community", "📢 " + t("nav_community", lang)),
        ("admin", "⚙️ " + t("nav_admin", lang)),
        ("auth", "🔐 " + (t("nav_login", lang) if not st.session_state.get("user") else "👤 Profile"))
    ]

    for page_key, label in nav_items:
        is_active = (st.session_state["current_page"] == page_key)
        btn_style = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=btn_style):
            st.session_state["current_page"] = page_key
            st.rerun()

    st.markdown("<hr style='border-color:#1E293B; margin:16px 0;'>", unsafe_allow_html=True)

    # User Profile Status Pill
    user = st.session_state.get("user")
    if user:
        role = user.get("role", "student")
        badge_cls = "badge-success" if role == "student" else "badge-danger"
        st.markdown(
            f"""<div style="background:#0F172E; padding:12px; border-radius:8px; border:1px solid #1E293B; margin-bottom:10px;">
                <span class="{badge_cls}" style="font-size:0.75rem;">{role.upper()}</span>
                <p style="color:#FFFFFF; margin:6px 0 2px 0; font-size:0.88rem; font-weight:600;">{user.get('full_name')}</p>
                <small style="color:#64748B;">{user.get('email')}</small>
            </div>""",
            unsafe_allow_html=True
        )
        if st.button("🚪 " + t("nav_logout", lang), key="btn_sidebar_logout", use_container_width=True):
            st.session_state["token"] = None
            st.session_state["user"] = None
            st.rerun()

    # Emergency Helpline Card
    st.markdown(
        """<div style="background:#1B1226; border:1px solid #FF0055; border-radius:8px; padding:12px; margin-top:20px;">
            <strong style="color:#FF0055; font-size:0.8rem;">🚨 CYBER FRAUD HELPLINE</strong>
            <p style="color:#CBD5E1; font-size:0.85rem; margin:4px 0 0 0;">Dial <strong>1930</strong> (Toll-Free)</p>
            <small style="color:#94A3B8;">cybercrime.gov.in</small>
        </div>""",
        unsafe_allow_html=True
    )

# 5. Route to Active Page View
current = st.session_state.get("current_page", "landing")

if current == "landing":
    from frontend.views.landing import render_landing
    render_landing(lang)
elif current == "dashboard":
    from frontend.views.dashboard import render_dashboard
    render_dashboard(lang)
elif current == "text_scanner":
    from frontend.views.text_scanner import render_text_scanner
    render_text_scanner(lang)
elif current == "ocr_scanner":
    from frontend.views.ocr_scanner import render_ocr_scanner
    render_ocr_scanner(lang)
elif current == "url_scanner":
    from frontend.views.url_scanner import render_url_scanner
    render_url_scanner(lang)
elif current == "verification":
    from frontend.views.company_recruiter import render_company_recruiter
    render_company_recruiter(lang)
elif current == "history":
    from frontend.views.history_view import render_history
    render_history(lang)
elif current == "community":
    from frontend.views.community_view import render_community
    render_community(lang)
elif current == "admin":
    from frontend.views.admin_view import render_admin
    render_admin(lang)
elif current == "auth":
    from frontend.views.auth_view import render_auth
    render_auth(lang)
else:
    from frontend.views.landing import render_landing
    render_landing(lang)
