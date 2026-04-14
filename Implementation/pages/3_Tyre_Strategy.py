"""
Tyre Strategy Page
Implements the TyreStintView boundary class from the Class Diagram.
Displays tyre stint information with compound colors and pit-stop timing.
"""

import streamlit as st
from controllers.tyre_controller import TyreStrategyController
from services.fastf1_service import COMPOUND_COLORS

st.set_page_config(page_title="Tyre Strategy", page_icon="🔧", layout="wide")

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
    .compound-legend {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-right: 20px;
        font-size: 0.9rem;
    }
    .compound-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        display: inline-block;
        border: 1px solid #555;
    }
</style>
""", unsafe_allow_html=True)


def requestTyreStrategy():
    """
    TyreStintView.requestTyreStrategy()
    Entry point for the tyre strategy view.
    """
    st.markdown('<div class="page-title">🔧 Tyre Strategy</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-desc">Compare pit stop strategy and tyre compound usage</div>', unsafe_allow_html=True)

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

    # Compound legend
    legend_html = '<div style="margin-bottom:15px;">'
    for compound, color in COMPOUND_COLORS.items():
        if compound != "UNKNOWN":
            text_color = "black" if compound in ["MEDIUM", "HARD"] else "white"
            legend_html += (
                f'<span class="compound-legend">'
                f'<span class="compound-dot" style="background:{color};"></span>'
                f'<span style="color:#CCC;">{compound}</span>'
                f'</span>'
            )
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

    st.markdown("---")

    if "tyre_ctrl" not in st.session_state:
        st.session_state.tyre_ctrl = TyreStrategyController()
    controller = st.session_state.tyre_ctrl

    session_id = ff1_session.session_info['Meeting']['Key'] if hasattr(ff1_session, 'session_info') else "session"
    cache_key = f"chart_tyre_{session_id}_{driver1.getAbbreviation()}_{driver2.getAbbreviation()}"

    if cache_key not in st.session_state:
        with st.spinner("Generating tyre strategy chart..."):
            st.session_state[cache_key] = controller.loadTyreStints(ff1_session, driver1, driver2)
            
    displayChart(st.session_state[cache_key])


def displayChart(chart):
    """
    TyreStintView.displayChart(chart)
    Display the generated chart in the Streamlit view.
    """
    st.plotly_chart(chart, use_container_width=True)


# ─── Run ───
requestTyreStrategy()
