"""
Community Scam Intelligence Feed View for JobShield AI.
Enables students to report emerging scams and upvote active threats to protect peers.
"""
import streamlit as st
from frontend.i18n import t
from frontend.api_client import api_client

def render_community(lang: str = "en"):
    st.markdown("## 📢 Community Scam Intelligence & Threat Feed")
    st.markdown(
        "<p style='color:#94A3B8;'>Crowdsourced student recruitment fraud warnings. "
        "Report suspicious recruiters, fake company letters, or fraudulent UPI IDs to protect the academic community.</p>",
        unsafe_allow_html=True
    )

    tab_feed, tab_report = st.tabs(["🚨 Public Threat Feed", "✍️ Submit Scam Alert"])

    with tab_feed:
        reports = api_client.get_community_reports()

        if not reports:
            st.info("No community scam reports submitted yet. Be the first to alert other students!")
        else:
            st.markdown(f"<span style='color:#64748B;'>Active Community Alerts: {len(reports)}</span>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            for rep in reports:
                rep_id = rep.get("id")
                upvotes = rep.get("upvotes", 1)

                with st.container():
                    st.markdown(
                        f"""<div style="background:#0F172E; border:1px solid #1E293B; border-radius:10px; padding:18px; margin-bottom:14px;">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                <div>
                                    <h4 style="color:#FF0055; margin:0 0 4px 0;">🚨 {rep.get('scam_title')}</h4>
                                    <span style="color:#00F0FF; font-size:0.88rem; font-weight:600;">Targeted Employer: {rep.get('company_claimed')}</span>
                                </div>
                                <span class="badge-danger">VERIFIED SCAM</span>
                            </div>
                            <p style="color:#CBD5E1; font-size:0.92rem; margin:12px 0;">{rep.get('scam_description')}</p>
                            <div style="background:#111A35; padding:10px 14px; border-radius:6px; margin-bottom:12px; font-size:0.85rem; color:#94A3B8;">
                                <span><strong>Contact Channel:</strong> <code>{rep.get('recruiter_contact')}</code></span> &nbsp;|&nbsp;
                                <span style="color:#FF70A6;"><strong>Extortion Demanded:</strong> {rep.get('payment_demanded')}</span>
                            </div>
                            <small style="color:#64748B;">Reported: {rep.get('created_at')} | Community Upvotes: <strong>{upvotes}</strong></small>
                        </div>""",
                        unsafe_allow_html=True
                    )

                    c_up, _ = st.columns([2, 8])
                    with c_up:
                        if st.button(f"🔺 Upvote Alert ({upvotes})", key=f"up_{rep_id}"):
                            api_client.upvote_report(rep_id)
                            st.success("Upvoted! Thank you for alerting fellow candidates.")
                            st.rerun()

    with tab_report:
        st.markdown("### Report a Recruitment Scam")
        st.markdown("<p style='color:#94A3B8;'>Help protect other college students by providing accurate details of the fraudulent solicitation:</p>", unsafe_allow_html=True)

        s_title = st.text_input("Alert Title", placeholder="e.g. Telegram YouTube Video Liking Deposit Scam")
        s_comp = st.text_input("Company Claimed by Scammer", placeholder="e.g. Amazon India / Fake TCS HR")
        s_contact = st.text_input("Scammer Contact / Telegram / Phone / UPI ID", placeholder="e.g. @amz_recruiter on Telegram or +919876543210")
        s_payment = st.text_input("Amount & Payment Mode Demanded", placeholder="e.g. Rs. 1,500 via Google Pay / PhonePe")
        s_desc = st.text_area("Detailed Scam Description & Modus Operandi", placeholder="Explain how the scam unfolded, promises made, and payment requests...", height=120)

        if st.button("Submit Fraud Report", key="btn_submit_report", use_container_width=True):
            if not s_title or not s_comp or not s_contact or not s_desc:
                st.error("Please complete all required fields before submitting.")
            else:
                token = st.session_state.get("token")
                api_client.submit_community_report(
                    title=s_title,
                    company=s_comp,
                    contact=s_contact,
                    desc=s_desc,
                    payment=s_payment or "None",
                    token=token
                )
                st.success("Scam report submitted and verified for public display. Thank you for protecting students!")
                st.rerun()
