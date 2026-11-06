"""
AI Job Offer Text Scanner View for JobShield AI.
Analyzes pasted job offers using TF-IDF NLP model, rule-based heuristics,
recruiter domain checks, and renders a Plotly risk gauge, radar chart, and PDF export.
"""
import streamlit as st
import plotly.graph_objects as go
from frontend.i18n import t
from frontend.api_client import api_client
from backend.services.pdf_generator import generate_pdf_report

def render_text_scanner(lang: str = "en"):
    st.markdown("## 🛡️ AI Job & Internship Offer Text Scanner")
    st.markdown(
        "<p style='color:#94A3B8;'>Paste full email bodies, WhatsApp / Telegram recruiting messages, "
        "or internship offer letters for comprehensive multi-layer cybersecurity verification.</p>",
        unsafe_allow_html=True
    )

    # Demo Fill Buttons
    c_btn1, c_btn2, c_btn3 = st.columns([2, 2, 3])
    with c_btn1:
        if st.button("🚨 Load Scam Sample (English)"):
            st.session_state["scan_text_input"] = (
                "Congratulations! You have been selected for Data Entry Specialist at Global Tech. "
                "Salary Rs. 45,000/month for 2 hours daily work. "
                "To confirm your seat, you must deposit a refundable registration fee of Rs. 1,500 via Google Pay to hrdept@upi. "
                "Contact HR Priya on Telegram @globaltech_hr immediately. Offer valid for 24 hours only."
            )
            st.session_state["scan_company_input"] = "Global Tech"
            st.session_state["scan_recruiter_input"] = "globaltech.recruiter@gmail.com"
            st.rerun()

    with c_btn2:
        if st.button("🚨 Load Scam Sample (Tamil)"):
            st.session_state["scan_text_input"] = (
                "அவசர வேலைவாய்ப்பு! வீட்டில் இருந்தபடியே மொபைலில் வேலை செய்து மாதம் ரூ. 40,000 சம்பாதிக்கலாம். "
                "பதிவுக் கட்டணம் ரூ. 1,000 முன்பணம் செலுத்த வேண்டும். "
                "உடனடி வருமானம் பெற டெலிகிராம் குரூப்பில் இணையவும் t.me/tamil_job_earn. கல்வித்தகுதி தேவையில்லை."
            )
            st.session_state["scan_company_input"] = "Tamil Fast Jobs"
            st.session_state["scan_recruiter_input"] = "tamiljobs.hr@gmail.com"
            st.rerun()

    with c_btn3:
        if st.button("✅ Load Genuine TCS Offer"):
            st.session_state["scan_text_input"] = (
                "Dear Candidate, Thank you for interviewing with Tata Consultancy Services (TCS). "
                "We are pleased to extend an offer of employment for Assistant Systems Engineer. "
                "Your annual CTC is INR 4,20,000. Accept your offer letter via https://nextstep.tcs.com. "
                "Please note that TCS never charges any registration, interview, or processing fees at any stage."
            )
            st.session_state["scan_company_input"] = "Tata Consultancy Services (TCS)"
            st.session_state["scan_recruiter_input"] = "campus.recruitment@tcs.com"
            st.rerun()

    # Form Inputs
    offer_text = st.text_area(
        t("paste_offer_placeholder", lang),
        value=st.session_state.get("scan_text_input", ""),
        height=180,
        key="main_offer_text"
    )

    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
        comp_name = st.text_input(
            t("claimed_company_label", lang),
            value=st.session_state.get("scan_company_input", ""),
            placeholder="e.g. Tata Consultancy Services, Amazon, Google"
        )
    with col_meta2:
        rec_email = st.text_input(
            t("recruiter_email_label", lang),
            value=st.session_state.get("scan_recruiter_input", ""),
            placeholder="e.g. recruiter@company.com or hr@gmail.com"
        )

    # Action Trigger
    if st.button("🔍 " + t("btn_analyze", lang), use_container_width=True):
        if not offer_text.strip():
            st.error("Please paste offer text to analyze.")
            return

        with st.spinner("Analyzing text with NLP model, inspecting heuristics, and cross-checking recruiter credentials..."):
            token = st.session_state.get("token")
            res = api_client.scan_text(
                text=offer_text,
                company=comp_name if comp_name.strip() else None,
                recruiter_email=rec_email if rec_email.strip() else None,
                token=token
            )
            st.session_state["last_scan_result"] = res

    # Display Scan Result
    res = st.session_state.get("last_scan_result")
    if res:
        st.markdown("<br><hr style='border-color:#1E293B;'><br>", unsafe_allow_html=True)
        st.markdown("## 📋 Forensic Audit Results")

        score = res.get("risk_score", 0.0)
        level = res.get("risk_level", "Unknown")
        verdict = res.get("verdict", "")

        # Gauge & Summary Columns
        col_gauge, col_summary = st.columns([5, 6])

        with col_gauge:
            # Plotly Gauge Indicator
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "Composite Fraud Risk", "font": {"size": 20, "color": "#FFFFFF"}},
                number={"suffix": "%", "font": {"size": 38, "color": "#FFFFFF"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94A3B8"},
                    "bar": {"color": "#FF0055" if score >= 65 else ("#FFAA00" if score >= 28 else "#00FF9D")},
                    "bgcolor": "rgba(0,0,0,0)",
                    "borderwidth": 1,
                    "bordercolor": "#1E293B",
                    "steps": [
                        {"range": [0, 28], "color": "rgba(0, 255, 157, 0.15)"},
                        {"range": [28, 65], "color": "rgba(255, 170, 0, 0.15)"},
                        {"range": [65, 100], "color": "rgba(255, 0, 85, 0.15)"}
                    ]
                }
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font={"color": "#FFFFFF"},
                height=260,
                margin=dict(t=30, b=10, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_summary:
            badge_cls = "badge-danger" if score >= 65 else ("badge-warning" if score >= 28 else "badge-success")
            st.markdown(
                f"""<div style="background:#0F172E; padding:20px; border-radius:12px; border:1px solid #1E293B; height:240px;">
                    <div style="margin-bottom:12px;">
                        <span class="{badge_cls}" style="font-size:1rem;">{level.upper()} RISK</span>
                    </div>
                    <h4 style="color:#FFFFFF; margin:0 0 10px 0;">{verdict}</h4>
                    <p style="color:#94A3B8; font-size:0.9rem; margin-bottom:8px;">
                        <strong>NLP Model Confidence:</strong> {res.get('confidence', 0)}%
                    </p>
                    <p style="color:#94A3B8; font-size:0.9rem;">
                        <strong>Flagged Heuristic Rules:</strong> {len(res.get('flags', []))} triggered
                    </p>
                </div>""",
                unsafe_allow_html=True
            )

        # Factor Decomposition Table
        st.markdown("### Risk Decomposition Breakdown")
        bd = res.get("breakdown", {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("NLP Content Risk", f"{bd.get('ml_confidence_score', 0)}%")
        c2.metric("Heuristic Rule Points", f"{bd.get('heuristic_risk_score', 0)} pts")
        c3.metric("Recruiter Domain Risk", f"{bd.get('recruiter_risk_score', 0)}%")
        c4.metric("Company Legitimacy", f"{bd.get('company_risk_score', 0)}%")

        # Flagged Indicators
        st.markdown(f"### {t('flagged_signals_title', lang)}")
        flags = res.get("flags", [])
        if not flags:
            st.success("No suspicious phrases, payment demands, or fraudulent patterns detected.")
        else:
            for flag in flags:
                sev = flag.get("severity", "medium").lower()
                border_col = "#FF0055" if sev == "critical" else ("#FFAA00" if sev == "high" else "#38B6FF")
                st.markdown(
                    f"""<div style="background:#111A35; border-left:4px solid {border_col}; border-radius:6px; padding:12px 16px; margin-bottom:8px;">
                        <strong style="color:#FFFFFF;">{flag.get('rule')}</strong>
                        <span style="float:right; text-transform:uppercase; font-size:0.8rem; color:{border_col}; font-weight:700;">{sev}</span>
                        <p style="color:#94A3B8; font-size:0.88rem; margin:6px 0 2px 0;">{flag.get('description')}</p>
                        {f"<code style='color:#00F0FF; background:#0B132B;'>Matched: {flag.get('match_text')}</code>" if flag.get('match_text') else ""}
                    </div>""",
                    unsafe_allow_html=True
                )

        # Safety Recommendations
        st.markdown(f"### {t('safety_advice_title', lang)}")
        for rec in res.get("recommendations", []):
            st.info(f"💡 {rec}")

        # PDF Download Button
        st.markdown("<br>", unsafe_allow_html=True)
        user = st.session_state.get("user")
        uname = user.get("full_name") if user else "Student Candidate"
        pdf_bytes = generate_pdf_report(res, uname)

        st.download_button(
            label="📄 " + t("export_pdf_btn", lang),
            data=pdf_bytes,
            file_name=f"jobshield_audit_report_{res.get('id', 'temp')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
