"""
Company & Recruiter Verification View for JobShield AI.
Cross-references corporate employers against verified registries,
detects look-alike domain spoofing, and exposes fraudulent recruiter email addresses.
"""
import streamlit as st
from frontend.i18n import t
from frontend.api_client import api_client

def render_company_recruiter(lang: str = "en"):
    st.markdown("## 🏢 Company & Recruiter Identity Verification")
    st.markdown(
        "<p style='color:#94A3B8;'>Validate the authenticity of employers and recruiter contact channels "
        "before submitting sensitive personal identity documents or attending unverified interviews.</p>",
        unsafe_allow_html=True
    )

    tab_company, tab_recruiter, tab_directory = st.tabs([
        "🏢 Verify Company / Domain",
        "👤 Verify Recruiter Email",
        "📚 Verified Enterprise Directory"
    ])

    # Tab 1: Company Verification
    with tab_company:
        st.markdown("### Employer Legitimacy & Typo-Squatting Check")
        c1, c2 = st.columns(2)
        with c1:
            comp_input = st.text_input("Employer / Organization Name", placeholder="e.g. Tata Consultancy Services (TCS), Infosys")
        with c2:
            domain_input = st.text_input("Provided Website / Domain", placeholder="e.g. tcs-careers.online or tcs.com")

        if st.button("Check Company Authenticity", key="btn_check_comp"):
            if not comp_input.strip():
                st.error("Please enter a company name.")
            else:
                with st.spinner("Checking corporate directory and domain similarity..."):
                    res = api_client.verify_company(comp_input, domain_input)

                    if res.get("is_verified"):
                        st.success(f"Verified Corporate Employer Found: **{res.get('matched_official_name')}**")
                        st.markdown(
                            f"""<div style="background:#0F172E; padding:18px; border-radius:10px; border-left:4px solid #00FF9D; margin-top:10px;">
                                <p style="color:#00FF9D; margin:0 0 6px 0; font-weight:600;">OFFICIAL DOMAIN: {res.get('official_domain')}</p>
                                <p style="color:#94A3B8; margin:0 0 6px 0;">Official Careers Portal: <a href="{res.get('careers_url')}" target="_blank" style="color:#00F0FF;">{res.get('careers_url')}</a></p>
                            </div>""",
                            unsafe_allow_html=True
                        )
                        if res.get("warning"):
                            st.warning(f"⚠️ {res.get('warning')}")
                    else:
                        st.warning(res.get("warning", "Company not found in verified registry."))

    # Tab 2: Recruiter Verification
    with tab_recruiter:
        st.markdown("### Recruiter Channel & Email Audit")
        r_email = st.text_input("Recruiter Email Address", placeholder="e.g. hr.tcs.placement@gmail.com or recruiter@amazon.com")
        r_comp = st.text_input("Company Claimed by Recruiter", placeholder="e.g. Amazon, Google, Wipro")

        if st.button("Audit Recruiter Email", key="btn_check_rec"):
            if not r_email.strip():
                st.error("Please enter recruiter email.")
            else:
                with st.spinner("Auditing sender reputation and domain consistency..."):
                    res = api_client.verify_recruiter(r_email, r_comp)
                    score = res.get("risk_score", 0)
                    badge_cls = "badge-danger" if score >= 60 else ("badge-warning" if score >= 30 else "badge-success")

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(
                        f"""<div style="background:#0F172E; padding:20px; border-radius:12px; border:1px solid #1E293B;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <h4 style="color:#FFFFFF; margin:0;">Recruiter Evaluation</h4>
                                <span class="{badge_cls}">{res.get('verdict')} ({score}%)</span>
                            </div>
                            <p style="color:#94A3B8; margin:12px 0 6px 0;"><strong>Provider Domain:</strong> @{res.get('provider_name')}</p>
                            <p style="color:#94A3B8; margin:0 0 12px 0;"><strong>Free Public Mailbox:</strong> {'Yes (High Caution)' if res.get('is_free_provider') else 'No (Enterprise Domain)'}</p>
                        </div>""",
                        unsafe_allow_html=True
                    )

                    st.markdown("#### Audit Rationale & Signals")
                    for f in res.get("flags", []):
                        st.info(f"🔍 {f}")

    # Tab 3: Directory
    with tab_directory:
        st.markdown("### Verified Tier-1 Enterprise Registry")
        st.markdown("<p style='color:#94A3B8;'>Official recruitment portals for top employers. Always verify offers directly on these domains:</p>", unsafe_allow_html=True)

        from backend.services.company_verifier import VERIFIED_ENTERPRISES
        for ent in VERIFIED_ENTERPRISES:
            st.markdown(
                f"""<div style="background:#111A35; padding:12px 18px; border-radius:8px; border-left:3px solid #00F0FF; margin-bottom:8px;">
                    <strong style="color:#FFFFFF; font-size:1rem;">{ent['name']}</strong><br>
                    <span style="color:#94A3B8; font-size:0.85rem;">Official Domain: <code>{ent['domain']}</code> | </span>
                    <a href="{ent['careers']}" target="_blank" style="color:#00F0FF; font-size:0.85rem; text-decoration:none;">Official Careers Link ↗</a>
                </div>""",
                unsafe_allow_html=True
            )
