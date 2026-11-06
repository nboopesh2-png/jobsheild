"""
Admin Control Center View for JobShield AI.
Telemetry, threat blacklist management, registered user audit, and AI pipeline status.
"""
import streamlit as st
from frontend.i18n import t
from frontend.api_client import api_client

def render_admin(lang: str = "en"):
    st.markdown("## 🛡️ Security Administrator Control Center")

    user = st.session_state.get("user")
    token = st.session_state.get("token")

    # Access Control Verification
    if not user or user.get("role") != "admin":
        st.warning("🔒 Administrative Privileges Required")
        st.markdown(
            """<div style="background:#0F172E; padding:18px; border-radius:10px; border-left:4px solid #FF0055; margin-bottom:14px;">
                <p style="color:#FFFFFF; margin:0 0 8px 0; font-weight:600;">You must be signed in as a System Administrator to access this module.</p>
                <span style="color:#94A3B8; font-size:0.9rem;">
                    Use the Demo Accounts in the Login portal: <code>admin@jobshield.ai</code> / <code>Admin@123456</code>.
                </span>
            </div>""",
            unsafe_allow_html=True
        )
        if st.button("Go to Sign In Portal"):
            st.session_state["current_page"] = "auth"
            st.rerun()
        return

    # Real Telemetry
    stats = api_client.get_admin_stats(token)

    st.markdown("### System-Wide Threat Telemetry")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""<div class="metric-box">
                <div class="metric-title">TOTAL USERS</div>
                <div class="metric-value">{stats.get('total_users', 0)}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""<div class="metric-box" style="border-left-color: #38B6FF;">
                <div class="metric-title">TOTAL AUDITS</div>
                <div class="metric-value" style="color: #38B6FF;">{stats.get('total_scans', 0)}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""<div class="metric-box" style="border-left-color: #FF0055;">
                <div class="metric-title">FRAUD DETECTIONS</div>
                <div class="metric-value" style="color: #FF0055;">{stats.get('high_risk_scans', 0)}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""<div class="metric-box" style="border-left-color: #7928CA;">
                <div class="metric-title">BLACKLISTED THREATS</div>
                <div class="metric-value" style="color: #B794F4;">{stats.get('blacklisted_entries_count', 0)}</div>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    tab_blacklist, tab_users, tab_model = st.tabs([
        "🚫 Threat Blacklist",
        "👥 Registered Users",
        "🤖 AI Model & Training Pipeline"
    ])

    # Tab 1: Blacklist Management
    with tab_blacklist:
        st.markdown("### Threat Indicator Blacklist")
        st.markdown("<p style='color:#94A3B8;'>Blacklisted domains, emails, and payment handles are automatically blocked across all student scans.</p>", unsafe_allow_html=True)

        col_b_add, col_b_list = st.columns([4, 6])
        with col_b_add:
            st.markdown("#### Add Threat Indicator")
            b_type = st.selectbox("Indicator Type", ["domain", "email", "phone", "upi", "keyword"])
            b_val = st.text_input("Threat Value", placeholder="e.g. scam-tcs-careers.xyz")
            b_reason = st.text_input("Flag Reason", placeholder="e.g. Phishing clone demanding UPI fees")

            if st.button("Add to Blacklist", key="btn_add_b"):
                if not b_val.strip() or not b_reason.strip():
                    st.error("Please specify both value and justification.")
                else:
                    res = api_client.add_blacklist(b_type, b_val, b_reason, token)
                    if "error" in res:
                        st.error(res["error"])
                    else:
                        st.success(f"Added '{b_val}' to threat blacklist.")
                        st.rerun()

        with col_b_list:
            st.markdown("#### Active Blacklisted Indicators")
            entries = api_client.get_blacklist(token)
            if not entries:
                st.write("No blacklisted indicators.")
            else:
                for e in entries:
                    st.markdown(
                        f"""<div style="background:#111A35; padding:10px 14px; border-radius:6px; border-left:3px solid #FF0055; margin-bottom:8px;">
                            <strong style="color:#FF0055;">[{e.get('entry_type', '').upper()}]</strong>
                            <code style="color:#FFFFFF; background:#0B132B;">{e.get('value')}</code><br>
                            <span style="color:#94A3B8; font-size:0.85rem;">Reason: {e.get('reason')}</span>
                        </div>""",
                        unsafe_allow_html=True
                    )

    # Tab 2: Users
    with tab_users:
        st.markdown("### Registered Platform Users")
        from backend.database import SessionLocal
        from backend.models import User
        db = SessionLocal()
        try:
            users_list = db.query(User).order_by(User.created_at.desc()).all()
            for u in users_list:
                role_col = "#FF0055" if u.role == "admin" else "#00FF9D"
                st.markdown(
                    f"""<div style="background:#111A35; padding:12px 16px; border-radius:6px; margin-bottom:8px; border:1px solid #1E293B;">
                        <strong style="color:#FFFFFF;">{u.full_name}</strong>
                        <span style="color:{role_col}; font-weight:700; float:right; font-size:0.85rem;">{u.role.upper()}</span><br>
                        <span style="color:#94A3B8; font-size:0.85rem;">Email: {u.email} | Joined: {str(u.created_at)[:19]}</span>
                    </div>""",
                    unsafe_allow_html=True
                )
        finally:
            db.close()

    # Tab 3: AI Model Pipeline
    with tab_model:
        st.markdown("### Scikit-Learn NLP Model Architecture")
        from backend.ai.dataset import TRAINING_DATA
        st.markdown(
            f"""
            - **Model Type**: Scikit-Learn Pipeline (`TfidfVectorizer` + `LogisticRegression`)
            - **Feature Extraction**: TF-IDF N-grams (1, 2) with Sublinear Term Frequency Scaling
            - **Max Feature Capacity**: 4,000 vocabulary tokens
            - **Optimization Solver**: `liblinear` with balanced class weights
            - **Training Corpus**: {len(TRAINING_DATA)} real-world authentic and fraudulent recruitment offers
            - **Explainability**: Integrated Feature Contribution Weights (XAI)
            """
        )
        st.success("AI Classifier status: ONLINE & ACCELERATED")
