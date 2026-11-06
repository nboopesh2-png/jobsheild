"""
Landing Page View for JobShield AI.
Features high-impact cybersecurity hero banner, live verified database metrics,
feature highlights, process workflow, tech stack overview, and FAQ.
"""
import streamlit as st
from frontend.i18n import t
from frontend.styles import get_shield_svg
from frontend.api_client import api_client

def render_landing(lang: str = "en"):
    # Header Banner
    col_logo, col_text = st.columns([1, 10])
    with col_logo:
        st.markdown(get_shield_svg(70), unsafe_allow_html=True)
    with col_text:
        st.markdown(
            f"<h1 style='margin-bottom:0px; padding-bottom:0px;' class='glow-text-cyan'>{t('hero_title', lang)}</h1>"
            f"<p style='color:#94A3B8; font-size:1.2rem; margin-top:4px;'>{t('hero_subtitle', lang)}</p>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Hero Action Buttons
    c_btn1, c_btn2, _ = st.columns([2, 2, 4])
    with c_btn1:
        if st.button("🛡️ " + t("btn_scan_offer", lang), use_container_width=True):
            st.session_state["current_page"] = "text_scanner"
            st.rerun()
    with c_btn2:
        if st.button("🚀 " + t("btn_get_started", lang), use_container_width=True):
            st.session_state["current_page"] = "dashboard"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Live Database Statistics (No invented numbers!)
    stats = api_client.get_admin_stats()
    st.markdown(
        "<div style='border-left: 3px solid #00F0FF; padding-left: 12px; margin-bottom: 12px;'>"
        "<h3 style='margin:0; color:#FFFFFF;'>Real-Time Threat Telemetry</h3>"
        "<span style='color:#64748B; font-size:0.85rem;'>Real database metrics. Never fabricated or hardcoded.</span>"
        "</div>",
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""<div class="metric-box">
                <div class="metric-title">TOTAL AUDITS</div>
                <div class="metric-value">{stats.get('total_scans', 0)}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""<div class="metric-box" style="border-left-color: #FF0055;">
                <div class="metric-title">FRAUD IDENTIFIED</div>
                <div class="metric-value" style="color: #FF0055;">{stats.get('high_risk_scans', 0)}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""<div class="metric-box" style="border-left-color: #00FF9D;">
                <div class="metric-title">VERIFIED ENTERPRISES</div>
                <div class="metric-value" style="color: #00FF9D;">{stats.get('verified_companies_count', 0)}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f"""<div class="metric-box" style="border-left-color: #7928CA;">
                <div class="metric-title">COMMUNITY ALERTS</div>
                <div class="metric-value" style="color: #B794F4;">{stats.get('total_community_reports', 0)}</div>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<br><hr style='border-color:#1E293B;'><br>", unsafe_allow_html=True)

    # Core Features Section
    st.markdown(f"## {t('features_title', lang)}")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(
            """<div class="cyber-card">
                <h4 style="color:#00F0FF; margin-top:0;">🤖 AI Scam Text Scanner</h4>
                <p style="color:#94A3B8; font-size:0.92rem;">
                    TF-IDF vectorizer and Scikit-Learn Logistic Regression model trained on authentic corporate & fraudulent offers.
                </p>
            </div>""",
            unsafe_allow_html=True
        )
        st.markdown(
            """<div class="cyber-card">
                <h4 style="color:#00F0FF; margin-top:0;">📷 Screenshot OCR Scanner</h4>
                <p style="color:#94A3B8; font-size:0.92rem;">
                    Upload offer letter screenshots, WhatsApp conversations, or Telegram chat images for instant visual forensic analysis.
                </p>
            </div>""",
            unsafe_allow_html=True
        )

    with f2:
        st.markdown(
            """<div class="cyber-card">
                <h4 style="color:#00F0FF; margin-top:0;">🌐 URL Security & Phishing</h4>
                <p style="color:#94A3B8; font-size:0.92rem;">
                    Scans application portals for typo-squatting, suspicious top-level domains (.xyz, .top), and VirusTotal threat intelligence.
                </p>
            </div>""",
            unsafe_allow_html=True
        )
        st.markdown(
            """<div class="cyber-card">
                <h4 style="color:#00F0FF; margin-top:0;">🏢 Company Verification</h4>
                <p style="color:#94A3B8; font-size:0.92rem;">
                    Cross-checks recruiters against verified enterprise directories, detecting look-alike domains like tcs-careers.online.
                </p>
            </div>""",
            unsafe_allow_html=True
        )

    with f3:
        st.markdown(
            """<div class="cyber-card">
                <h4 style="color:#00F0FF; margin-top:0;">🧠 Explainable AI (XAI)</h4>
                <p style="color:#94A3B8; font-size:0.92rem;">
                    Clear, transparent breakdown of exactly why an offer was flagged, showing high-risk words, deposit demands, and signals.
                </p>
            </div>""",
            unsafe_allow_html=True
        )
        st.markdown(
            """<div class="cyber-card">
                <h4 style="color:#00F0FF; margin-top:0;">🌐 Bilingual Tamil & English</h4>
                <p style="color:#94A3B8; font-size:0.92rem;">
                    Complete native Tamil (தமிழ்) and English UI localization with detection of regional fraudulent schemes.
                </p>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<br><hr style='border-color:#1E293B;'><br>", unsafe_allow_html=True)

    # How It Works Workflow
    st.markdown(f"## {t('how_it_works_title', lang)}")
    w1, w2, w3, w4 = st.columns(4)
    with w1:
        st.markdown(
            """<div style="background:#0F172E; padding:18px; border-radius:10px; border-top:3px solid #00F0FF;">
                <h5 style="color:#00F0FF; margin-top:0;">STEP 1: INGESTION</h5>
                <p style="color:#94A3B8; font-size:0.88rem;">Paste text, upload an offer screenshot, or provide a job portal link.</p>
            </div>""",
            unsafe_allow_html=True
        )
    with w2:
        st.markdown(
            """<div style="background:#0F172E; padding:18px; border-radius:10px; border-top:3px solid #7928CA;">
                <h5 style="color:#B794F4; margin-top:0;">STEP 2: AI & RULES</h5>
                <p style="color:#94A3B8; font-size:0.88rem;">Dual analysis: NLP vectorizer prediction plus 10+ cybersecurity heuristic rules.</p>
            </div>""",
            unsafe_allow_html=True
        )
    with w3:
        st.markdown(
            """<div style="background:#0F172E; padding:18px; border-radius:10px; border-top:3px solid #00FF9D;">
                <h5 style="color:#00FF9D; margin-top:0;">STEP 3: VERIFICATION</h5>
                <p style="color:#94A3B8; font-size:0.88rem;">Email domain check, free-mail detector, and typo-squatting domain validation.</p>
            </div>""",
            unsafe_allow_html=True
        )
    with w4:
        st.markdown(
            """<div style="background:#0F172E; padding:18px; border-radius:10px; border-top:3px solid #38B6FF;">
                <h5 style="color:#38B6FF; margin-top:0;">STEP 4: AUDIT PDF</h5>
                <p style="color:#94A3B8; font-size:0.88rem;">Generate an official forensic PDF audit report with risk gauge and safety checklist.</p>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<br><hr style='border-color:#1E293B;'><br>", unsafe_allow_html=True)

    # Technology Stack & College Project Attribution
    st.markdown("## Technical Architecture")
    tech_col1, tech_col2 = st.columns(2)
    with tech_col1:
        st.markdown(
            """
            - **Frontend**: Streamlit, Custom Cyber CSS, Plotly Interactive Visualizations
            - **Backend**: FastAPI, Uvicorn ASGI Server, Pydantic Data Contracts
            - **Database**: MySQL / SQLite via SQLAlchemy 2.0 ORM
            - **Security**: JWT Authentication, PBKDF2-HMAC Password Hashing
            """
        )
    with tech_col2:
        st.markdown(
            """
            - **AI / NLP**: Scikit-Learn TF-IDF, Logistic Regression, Feature Importance
            - **OCR**: EasyOCR, Pillow Image Contrast & Noise Reduction
            - **Reports**: ReportLab Automated PDF Audit Engine
            - **Threat Intelligence**: VirusTotal API, Domain Typosquatting Matcher
            """
        )

    # FAQ Section
    st.markdown(f"## {t('faq_title', lang)}")
    with st.expander("❓ Does any legitimate corporate employer charge an application or security fee?"):
        st.write("Never. Tier-1 employers including TCS, Infosys, Wipro, Google, and Amazon explicitly prohibit collecting money, training fees, uniform charges, or laptop security deposits at any stage of recruitment.")

    with st.expander("❓ How does JobShield AI detect recruiter impersonation?"):
        st.write("JobShield AI inspects the sender's email domain. If a recruiter claims to represent a multinational corporation like Amazon or TCS but sends messages from a generic @gmail.com or disposable address, the system immediately flags high risk.")

    with st.expander("❓ Can I generate an audit report for legal or academic submission?"):
        st.write("Yes. Every scan provides an instant download button for a forensic ReportLab PDF audit report with a cryptographic timestamp, risk breakdown, and official helpline references.")

    # Footer
    st.markdown(
        f"""<div class="cyber-footer">
            <p><strong>JobShield AI</strong> — Final Year College Project & Student Recruitment Protection Initiative.</p>
            <p>Developed with Python Full-Stack, Machine Learning, and Cybersecurity Engineering.</p>
            <p style="color:#475569;">National Cyber Crime Helpline: 1930 | cybercrime.gov.in</p>
        </div>""",
        unsafe_allow_html=True
    )
