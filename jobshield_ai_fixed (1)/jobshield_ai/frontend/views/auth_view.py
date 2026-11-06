"""
Authentication View for JobShield AI.
Provides Student / Admin sign in, account registration, role badge display, and session management.
"""
import streamlit as st
from frontend.i18n import t
from frontend.api_client import api_client

def render_auth(lang: str = "en"):
    st.markdown("## 🔐 Security Authentication & Access Portal")

    # If already logged in, show profile card
    user = st.session_state.get("user")
    if user:
        st.success(f"Authenticated as: **{user.get('full_name')}** ({user.get('email')})")
        role = user.get("role", "student")
        badge_cls = "badge-success" if role == "student" else "badge-danger"
        st.markdown(f"Access Role: <span class='{badge_cls}'>{role.upper()}</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚪 Logout of JobShield AI"):
            st.session_state["token"] = None
            st.session_state["user"] = None
            st.success("Successfully logged out.")
            st.rerun()
        return

    tab_login, tab_register, tab_demo = st.tabs(["🔑 Sign In", "📝 Create Student Account", "💡 Demo Accounts"])

    with tab_login:
        st.markdown("### Enter Credentials")
        login_email = st.text_input("Institutional / Personal Email", key="login_email")
        login_pass = st.text_input("Password", type="password", key="login_pass")

        if st.button("Authenticate & Enter", key="btn_login", use_container_width=True):
            if not login_email or not login_pass:
                st.error("Please enter both email and password.")
            else:
                with st.spinner("Verifying credentials..."):
                    res = api_client.login(login_email, login_pass)
                    if "error" in res:
                        st.error(res["error"])
                    else:
                        st.session_state["token"] = res.get("access_token")
                        st.session_state["user"] = res.get("user")
                        st.success("Authentication successful! Welcome to JobShield AI.")
                        st.rerun()

    with tab_register:
        st.markdown("### Student Account Registration")
        reg_name = st.text_input("Full Candidate Name", key="reg_name")
        reg_email = st.text_input("College / Personal Email", key="reg_email")
        reg_pass = st.text_input("Choose Strong Password (min 6 chars)", type="password", key="reg_pass")

        if st.button("Create Account", key="btn_register", use_container_width=True):
            if not reg_name or not reg_email or not reg_pass:
                st.error("Please fill in all required registration fields.")
            elif len(reg_pass) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                with st.spinner("Creating candidate profile..."):
                    res = api_client.register(reg_email, reg_name, reg_pass, role="student")
                    if "error" in res:
                        st.error(res["error"])
                    else:
                        st.success("Account created successfully! You can now log in.")

    with tab_demo:
        st.markdown("### Fast Testing Demo Credentials")
        st.info("Pre-seeded for college project evaluations and faculty demonstrations:")

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(
                """<div style="background:#0F172E; padding:16px; border-radius:8px; border-left:3px solid #00F0FF;">
                    <strong style="color:#00F0FF;">🎓 Student Profile</strong><br>
                    Email: <code>student@college.edu</code><br>
                    Password: <code>Student@123456</code><br>
                    Role: Student Candidate
                </div>""",
                unsafe_allow_html=True
            )
            if st.button("Auto-Fill Student Credentials", key="btn_fill_student"):
                st.session_state["login_email"] = "student@college.edu"
                st.session_state["login_pass"] = "Student@123456"
                st.rerun()

        with col_d2:
            st.markdown(
                """<div style="background:#0F172E; padding:16px; border-radius:8px; border-left:3px solid #FF0055;">
                    <strong style="color:#FF0055;">🛡️ Security Administrator</strong><br>
                    Email: <code>admin@jobshield.ai</code><br>
                    Password: <code>Admin@123456</code><br>
                    Role: System Admin
                </div>""",
                unsafe_allow_html=True
            )
            if st.button("Auto-Fill Admin Credentials", key="btn_fill_admin"):
                st.session_state["login_email"] = "admin@jobshield.ai"
                st.session_state["login_pass"] = "Admin@123456"
                st.rerun()
