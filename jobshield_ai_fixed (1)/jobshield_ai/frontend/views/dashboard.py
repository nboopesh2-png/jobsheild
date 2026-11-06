"""
Student Dashboard View for JobShield AI.
Visualizes real database metrics, risk distribution Plotly doughnut chart,
recent scan audit history, and quick scan action buttons.
"""
import streamlit as st
import plotly.graph_objects as go
from frontend.i18n import t
from frontend.api_client import api_client

def render_dashboard(lang: str = "en"):
    user = st.session_state.get("user")
    user_name = user.get("full_name") if user else "Student Researcher"

    st.markdown(
        f"## 📊 Student Threat Intelligence Dashboard"
    )
    st.markdown(f"<span style='color:#94A3B8;'>Welcome back, <strong>{user_name}</strong>. Here is your recruitment fraud protection overview.</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Fetch live history and stats from database
    token = st.session_state.get("token")
    user_id = user.get("id") if user else None
    history = api_client.get_user_history(token=token, user_id=user_id)

    total_scans = len(history)
    high_risk_count = sum(1 for h in history if "high" in h.get("risk_level", "").lower())
    med_risk_count = sum(1 for h in history if "medium" in h.get("risk_level", "").lower())
    low_risk_count = sum(1 for h in history if "low" in h.get("risk_level", "").lower())

    # Stat metric cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""<div class="metric-box">
                <div class="metric-title">TOTAL AUDITS</div>
                <div class="metric-value">{total_scans}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""<div class="metric-box" style="border-left-color: #FF0055;">
                <div class="metric-title">HIGH-RISK SCAMS</div>
                <div class="metric-value" style="color: #FF0055;">{high_risk_count}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""<div class="metric-box" style="border-left-color: #FFAA00;">
                <div class="metric-title">MEDIUM SUSPICIONS</div>
                <div class="metric-value" style="color: #FFAA00;">{med_risk_count}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""<div class="metric-box" style="border-left-color: #00FF9D;">
                <div class="metric-title">LEGITIMATE OFFERS</div>
                <div class="metric-value" style="color: #00FF9D;">{low_risk_count}</div>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly Visualizations & Quick Actions
    col_chart, col_actions = st.columns([6, 4])

    with col_chart:
        st.markdown("### Risk Distribution Breakdown")
        if total_scans == 0:
            st.info("No scans recorded yet. Perform your first scan using the quick scan button.")
        else:
            fig = go.Figure(data=[go.Pie(
                labels=["High Risk / Scam", "Medium Suspicion", "Low Risk / Safe"],
                values=[high_risk_count, med_risk_count, low_risk_count],
                hole=0.6,
                marker=dict(colors=["#FF0055", "#FFAA00", "#00FF9D"]),
                textinfo="label+percent",
                hoverinfo="label+value"
            )])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E2E8F0"),
                margin=dict(t=20, b=20, l=10, r=10),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_actions:
        st.markdown("### Rapid Protection Actions")
        st.markdown(
            """<div style="background:#0F172E; padding:18px; border-radius:10px; margin-bottom:14px; border:1px solid #1F2E54;">
                <p style="color:#00F0FF; margin:0 0 8px 0; font-weight:600;">⚡ Instant Text Inspection</p>
                <span style="color:#94A3B8; font-size:0.85rem;">Paste an offer email or Telegram message to assess fraud probability.</span>
            </div>""",
            unsafe_allow_html=True
        )
        if st.button("🛡️ Launch AI Text Scanner", use_container_width=True):
            st.session_state["current_page"] = "text_scanner"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """<div style="background:#0F172E; padding:18px; border-radius:10px; margin-bottom:14px; border:1px solid #1F2E54;">
                <p style="color:#B794F4; margin:0 0 8px 0; font-weight:600;">📷 Screenshot OCR Ingestion</p>
                <span style="color:#94A3B8; font-size:0.85rem;">Upload an offer letter screenshot or chat image for OCR extraction.</span>
            </div>""",
            unsafe_allow_html=True
        )
        if st.button("📷 Launch OCR Screenshot Scanner", use_container_width=True):
            st.session_state["current_page"] = "ocr_scanner"
            st.rerun()

    st.markdown("<br><hr style='border-color:#1E293B;'><br>", unsafe_allow_html=True)

    # Recent Scans Table
    st.markdown("### Recent Verification Activity")
    if not history:
        st.write("No recent audit records found.")
    else:
        for item in history[:5]:
            score = item.get("risk_score", 0)
            level = item.get("risk_level", "Unknown")
            badge_class = "badge-danger" if "high" in level.lower() else ("badge-warning" if "medium" in level.lower() else "badge-success")

            with st.container():
                st.markdown(
                    f"""<div style="background:#111A35; border:1px solid #1E293B; border-radius:8px; padding:14px 18px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="color:#00F0FF; font-weight:600; font-size:0.95rem;">Type: {item.get('scan_type', '').upper()}</span>
                            <span class="{badge_class}">{level.upper()} ({score}%)</span>
                        </div>
                        <p style="color:#CBD5E1; margin:8px 0 4px 0; font-size:0.9rem;">{item.get('input_preview', '')}</p>
                        <small style="color:#64748B;">Audited at: {item.get('created_at', '')}</small>
                    </div>""",
                    unsafe_allow_html=True
                )
