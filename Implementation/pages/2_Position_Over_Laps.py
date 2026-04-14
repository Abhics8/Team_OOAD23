"""
Position Over Laps Page
Implements the PositionTrackingView boundary class from the Class Diagram.
Displays position changes over race laps for two selected drivers.
"""

import streamlit as st
from controllers.position_controller import PositionController

st.set_page_config(page_title="Position Over Laps", page_icon="📈", layout="wide")

st.markdown("""
<style>
    .page-title {
        color: #E10600;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .page-desc {
        color: #888;
        font-size: 1rem;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


def requestPositionChart():
    """
    PositionTrackingView.requestPositionChart()
    Entry point for the position tracking view.
    """
    st.markdown('<div class="page-title">📈 Position Over Laps</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-desc">Track position changes and overtakes across the race</div>', unsafe_allow_html=True)

    # Check prerequisites
    if not st.session_state.get("session_loaded", False):
        st.warning("⚠️ Please load a session first from the sidebar.")
        return

    if not st.session_state.get("drivers_selected", False):
        st.warning("⚠️ Please select two drivers from the sidebar.")
        return

    ff1_session = st.session_state.ff1_session
    driver1 = st.session_state.driver1
    driver2 = st.session_state.driver2

    # Display driver comparison header
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        color1 = driver1.team.getColor() if driver1.team else "#FFF"
        st.markdown(
            f'<div style="text-align:right;font-size:1.5rem;font-weight:700;">'
            f'<span style="color:{color1}">●</span> {driver1.getName()}</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div style="text-align:center;font-size:1.2rem;color:#888;">VS</div>',
            unsafe_allow_html=True,
        )
    with col3:
        color2 = driver2.team.getColor() if driver2.team else "#FFF"
        st.markdown(
            f'<div style="font-size:1.5rem;font-weight:700;">'
            f'{driver2.getName()} <span style="color:{color2}">●</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    if "position_ctrl" not in st.session_state:
        st.session_state.position_ctrl = PositionController()
    controller = st.session_state.position_ctrl

    session_id = ff1_session.session_info['Meeting']['Key'] if hasattr(ff1_session, 'session_info') else "session"
    cache_key = f"chart_position_{session_id}_{driver1.getAbbreviation()}_{driver2.getAbbreviation()}"

    if cache_key not in st.session_state:
        with st.spinner("Generating position chart..."):
            st.session_state[cache_key] = controller.loadPositionData(ff1_session, driver1, driver2)
            
    displayChart(st.session_state[cache_key])


def displayChart(chart):
    """
    PositionTrackingView.displayChart(chart)
    Display the generated chart in the Streamlit view.
    """
    st.plotly_chart(chart, use_container_width=True)


# ─── Run ───
requestPositionChart()
