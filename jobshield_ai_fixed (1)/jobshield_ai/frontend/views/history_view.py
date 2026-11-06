"""
Scan History & Audit Reports View for JobShield AI.
Allows students to review all past scans, examine flagged indicators,
and download cryptographic ReportLab PDF audit reports.
"""
import streamlit as st
from frontend.i18n import t
from frontend.api_client import api_client
from backend.services.pdf_generator import generate_pdf_report

def render_history(lang: str = "en"):
    st.markdown("## 📜 Forensic Audit History & Reports")
    st.markdown(
        "<p style='color:#94A3B8;'>Review previously audited job offers, inspect historical threat indicators, "
        "and export PDF audit certificates for academic, institutional, or cybercrime filing purposes.</p>",
        unsafe_allow_html=True
    )

    token = st.session_state.get("token")
    user = st.session_state.get("user")
    user_id = user.get("id") if user else None

    history = api_client.get_user_history(token=token, user_id=user_id)

    if not history:
        st.info("No scan history found. Run a scan from the AI Text Scanner or Screenshot OCR Scanner.")
        return

    # Filter controls
    c_f1, c_f2 = st.columns([4, 4])
    with c_f1:
        type_filter = st.selectbox("Filter by Scan Type", ["All Types", "Text", "OCR", "URL"])
    with c_f2:
        level_filter = st.selectbox("Filter by Risk Level", ["All Levels", "High / Critical", "Medium", "Low"])

    filtered = history
    if type_filter != "All Types":
        filtered = [h for h in filtered if h.get("scan_type", "").lower() == type_filter.lower()]
    if level_filter != "All Levels":
        filtered = [h for h in filtered if level_filter.lower() in h.get("risk_level", "").lower()]

    st.markdown(f"<span style='color:#64748B;'>Displaying {len(filtered)} audit records</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    for item in filtered:
        scan_id = item.get("id")
        score = item.get("risk_score", 0)
        level = item.get("risk_level", "Unknown")
        verdict = item.get("verdict", "")
        badge_cls = "badge-danger" if "high" in level.lower() else ("badge-warning" if "medium" in level.lower() else "badge-success")

        with st.expander(f"Audit #{scan_id} — {item.get('scan_type', '').upper()} | Risk: {score}% ({level})", expanded=False):
            st.markdown(
                f"""<div style="background:#0F172E; padding:16px; border-radius:8px; border:1px solid #1E293B; margin-bottom:12px;">
                    <span class="{badge_cls}" style="float:right;">{level.upper()}</span>
                    <h4 style="color:#FFFFFF; margin:0 0 6px 0;">{verdict}</h4>
                    <p style="color:#94A3B8; font-size:0.85rem; margin:0;">Timestamp: {item.get('created_at')}</p>
                </div>""",
                unsafe_allow_html=True
            )

            st.markdown("**Sample Preview:**")
            st.code(item.get("input_preview", ""), language="text")

            # Flagged Indicators
            flags = item.get("flags", [])
            if flags:
                st.markdown("**Triggered Threat Indicators:**")
                for f in flags:
                    st.markdown(f"- **{f.get('rule')}** ({f.get('severity', '').upper()}): {f.get('description')}")

            # PDF Download
            user_name = user.get("full_name") if user else "Student Candidate"
            scan_data_for_pdf = {
                "id": scan_id,
                "scan_type": item.get("scan_type", "Text"),
                "risk_score": score,
                "risk_level": level,
                "verdict": verdict,
                "breakdown": item.get("breakdown", {}),
                "flags": flags,
                "recommendations": [
                    "Never transfer money: Genuine employers never charge for applications or equipment.",
                    "Verify all offers on official corporate careers portals.",
                    "Report cyber fraud incidents to the National Cyber Crime Helpline (1930)."
                ]
            }
            pdf_bytes = generate_pdf_report(scan_data_for_pdf, user_name)

            st.download_button(
                label=f"📥 Download Audit PDF (JS-AUDIT-{scan_id})",
                data=pdf_bytes,
                file_name=f"jobshield_audit_{scan_id}.pdf",
                mime="application/pdf",
                key=f"pdf_btn_{scan_id}"
            )
