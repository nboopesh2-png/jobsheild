"""
Screenshot OCR Scanner View for JobShield AI.
Extracts text from screenshots of fake offer letters, WhatsApp chats, and Telegram messages
and runs comprehensive AI recruitment fraud inspection.
"""
import streamlit as st
import plotly.graph_objects as go
from frontend.i18n import t
from frontend.api_client import api_client
from backend.services.pdf_generator import generate_pdf_report

def render_ocr_scanner(lang: str = "en"):
    st.markdown("## 📷 Screenshot OCR Job Offer Scanner")
    st.markdown(
        "<p style='color:#94A3B8;'>Upload a screenshot or document image of a suspicious offer letter, "
        "WhatsApp chat, or Telegram recruitment message for automated optical character recognition & forensic audit.</p>",
        unsafe_allow_html=True
    )

    col_up, col_info = st.columns([6, 4])
    with col_up:
        uploaded_file = st.file_uploader(
            "Upload Offer Screenshot (PNG, JPG, JPEG)",
            type=["png", "jpg", "jpeg", "webp"],
            help="High-contrast screenshots with legible text yield highest OCR precision."
        )

    with col_info:
        st.markdown(
            """<div style="background:#0F172E; padding:16px; border-radius:8px; border:1px solid #1E293B;">
                <h5 style="color:#00F0FF; margin-top:0;">💡 Supported Evidence Types</h5>
                <ul style="color:#94A3B8; font-size:0.85rem; padding-left:18px;">
                    <li>Appointment Letter PDFs / PNGs</li>
                    <li>WhatsApp recruiter chats</li>
                    <li>Telegram task channel screenshots</li>
                    <li>Payment QR code solicitations</li>
                </ul>
            </div>""",
            unsafe_allow_html=True
        )

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image Preview", use_column_width=True)

        c_opt1, c_opt2 = st.columns(2)
        with c_opt1:
            claimed_comp = st.text_input("Claimed Company (Optional)", placeholder="e.g. Infosys, TCS, Amazon")
        with c_opt2:
            rec_email = st.text_input("Recruiter Email (Optional)", placeholder="e.g. hr@wipro.com or hr@gmail.com")

        if st.button("🔍 Extract Text & Run Forensic OCR Audit", use_container_width=True):
            file_bytes = uploaded_file.getvalue()
            with st.spinner("Processing image through computer vision filters and OCR model..."):
                token = st.session_state.get("token")
                res = api_client.scan_ocr(
                    file_bytes=file_bytes,
                    filename=uploaded_file.name,
                    company=claimed_comp if claimed_comp.strip() else None,
                    recruiter_email=rec_email if rec_email.strip() else None,
                    token=token
                )
                st.session_state["ocr_scan_result"] = res

    # Display OCR Result
    res = st.session_state.get("ocr_scan_result")
    if res:
        st.markdown("<br><hr style='border-color:#1E293B;'><br>", unsafe_allow_html=True)
        st.markdown("### Extracted Text Content")
        with st.expander("📄 View Extracted Text", expanded=True):
            st.code(res.get("input_preview", "No text extracted."), language="text")

        score = res.get("risk_score", 0.0)
        level = res.get("risk_level", "Unknown")
        verdict = res.get("verdict", "")

        # Gauge & Summary
        col_g, col_s = st.columns([5, 6])
        with col_g:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "OCR Fraud Risk Score", "font": {"size": 20, "color": "#FFFFFF"}},
                number={"suffix": "%", "font": {"size": 38, "color": "#FFFFFF"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#94A3B8"},
                    "bar": {"color": "#FF0055" if score >= 65 else ("#FFAA00" if score >= 28 else "#00FF9D")},
                    "bgcolor": "rgba(0,0,0,0)",
                    "steps": [
                        {"range": [0, 28], "color": "rgba(0, 255, 157, 0.15)"},
                        {"range": [28, 65], "color": "rgba(255, 170, 0, 0.15)"},
                        {"range": [65, 100], "color": "rgba(255, 0, 85, 0.15)"}
                    ]
                }
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#FFFFFF"}, height=240, margin=dict(t=30, b=10, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)

        with col_s:
            badge_cls = "badge-danger" if score >= 65 else ("badge-warning" if score >= 28 else "badge-success")
            st.markdown(
                f"""<div style="background:#0F172E; padding:20px; border-radius:12px; border:1px solid #1E293B; height:220px;">
                    <div style="margin-bottom:12px;">
                        <span class="{badge_cls}" style="font-size:1rem;">{level.upper()} RISK</span>
                    </div>
                    <h4 style="color:#FFFFFF; margin:0 0 10px 0;">{verdict}</h4>
                    <p style="color:#94A3B8; font-size:0.9rem;">
                        <strong>AI Confidence:</strong> {res.get('confidence', 0)}%
                    </p>
                </div>""",
                unsafe_allow_html=True
            )

        # Flagged Indicators
        st.markdown(f"### {t('flagged_signals_title', lang)}")
        flags = res.get("flags", [])
        if not flags:
            st.success("No critical scam indicators identified in the OCR text.")
        else:
            for flag in flags:
                sev = flag.get("severity", "medium").lower()
                border_col = "#FF0055" if sev == "critical" else ("#FFAA00" if sev == "high" else "#38B6FF")
                st.markdown(
                    f"""<div style="background:#111A35; border-left:4px solid {border_col}; border-radius:6px; padding:12px 16px; margin-bottom:8px;">
                        <strong style="color:#FFFFFF;">{flag.get('rule')}</strong>
                        <span style="float:right; text-transform:uppercase; font-size:0.8rem; color:{border_col}; font-weight:700;">{sev}</span>
                        <p style="color:#94A3B8; font-size:0.88rem; margin:6px 0 2px 0;">{flag.get('description')}</p>
                    </div>""",
                    unsafe_allow_html=True
                )

        # PDF Download Button
        user = st.session_state.get("user")
        uname = user.get("full_name") if user else "Student Candidate"
        pdf_bytes = generate_pdf_report(res, uname)

        st.download_button(
            label="📄 " + t("export_pdf_btn", lang),
            data=pdf_bytes,
            file_name=f"jobshield_ocr_report_{res.get('id', 'temp')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
