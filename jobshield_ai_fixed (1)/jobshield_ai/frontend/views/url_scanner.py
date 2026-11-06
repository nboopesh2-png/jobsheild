"""
URL Security & Phishing Scanner View for JobShield AI.
Inspects recruiting links, career portals, and interview URLs for typosquatting,
dangerous TLDs, IP hosting, and malware reputation.
"""
import streamlit as st
import plotly.graph_objects as go
from frontend.i18n import t
from frontend.api_client import api_client

def render_url_scanner(lang: str = "en"):
    st.markdown("## 🌐 URL Security & Phishing Scanner")
    st.markdown(
        "<p style='color:#94A3B8;'>Verify the legitimacy of job application portals, interview links, "
        "and registration URLs to prevent credential harvesting and drive-by malware.</p>",
        unsafe_allow_html=True
    )

    # Sample Quick Buttons
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚨 Test Typo-squat Clone"):
            st.session_state["target_url_input"] = "http://tcs-careers-interview.online/portal/apply"
            st.rerun()
    with c2:
        if st.button("🚨 Test Suspicious TLD"):
            st.session_state["target_url_input"] = "https://amazon-parttime-tasks.xyz/register"
            st.rerun()
    with c3:
        if st.button("✅ Test Official TCS Portal"):
            st.session_state["target_url_input"] = "https://nextstep.tcs.com"
            st.rerun()

    target_url = st.text_input(
        "Job Application or Interview URL",
        value=st.session_state.get("target_url_input", ""),
        placeholder="https://company-careers.com/apply"
    )

    if st.button("🔍 Scan URL Reputation", use_container_width=True):
        if not target_url.strip():
            st.error("Please enter a URL to scan.")
            return

        with st.spinner("Analyzing domain DNS, checking suspicious TLDs, and inspecting VirusTotal threat database..."):
            token = st.session_state.get("token")
            res = api_client.scan_url(target_url, token)
            st.session_state["url_scan_result"] = res

    res = st.session_state.get("url_scan_result")
    if res:
        st.markdown("<br><hr style='border-color:#1E293B;'><br>", unsafe_allow_html=True)
        st.markdown("### URL Forensic Inspection Result")

        score = res.get("risk_score", 0.0)
        level = res.get("risk_level", "Unknown")
        verdict = res.get("verdict", "")

        col_g, col_details = st.columns([5, 6])
        with col_g:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "URL Security Threat Score", "font": {"size": 20, "color": "#FFFFFF"}},
                number={"suffix": "%", "font": {"size": 38, "color": "#FFFFFF"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#94A3B8"},
                    "bar": {"color": "#FF0055" if score >= 60 else ("#FFAA00" if score >= 25 else "#00FF9D")},
                    "bgcolor": "rgba(0,0,0,0)",
                    "steps": [
                        {"range": [0, 25], "color": "rgba(0, 255, 157, 0.15)"},
                        {"range": [25, 60], "color": "rgba(255, 170, 0, 0.15)"},
                        {"range": [60, 100], "color": "rgba(255, 0, 85, 0.15)"}
                    ]
                }
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#FFFFFF"}, height=240, margin=dict(t=30, b=10, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)

        with col_details:
            badge_cls = "badge-danger" if score >= 60 else ("badge-warning" if score >= 25 else "badge-success")
            st.markdown(
                f"""<div style="background:#0F172E; padding:20px; border-radius:12px; border:1px solid #1E293B; height:220px;">
                    <div style="margin-bottom:12px;">
                        <span class="{badge_cls}" style="font-size:1rem;">{level.upper()}</span>
                    </div>
                    <h4 style="color:#FFFFFF; margin:0 0 8px 0;">{verdict}</h4>
                    <p style="color:#94A3B8; font-size:0.9rem; margin-bottom:4px;">
                        <strong>Target Domain:</strong> <code>{res.get('domain', '')}</code>
                    </p>
                    <p style="color:#94A3B8; font-size:0.9rem;">
                        <strong>VirusTotal Detections:</strong> {res.get('virustotal_malicious', 0)} engines flagged
                    </p>
                </div>""",
                unsafe_allow_html=True
            )

        # Technical Indicators
        st.markdown("### Technical Findings & Security Signals")
        for d in res.get("details", []):
            st.markdown(
                f"""<div style="background:#111A35; border-left:3px solid #00F0FF; padding:10px 14px; border-radius:6px; margin-bottom:8px;">
                    <span style="color:#E2E8F0; font-size:0.9rem;">{d}</span>
                </div>""",
                unsafe_allow_html=True
            )
