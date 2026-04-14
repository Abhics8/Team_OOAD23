"""
F1 Insights & Strategy Explorer — Main Application
This is the entry point for the Streamlit dashboard.
Implements SessionSelectionView and DriverSelectionView boundary classes
from the Class Diagram via the sidebar widgets.
"""

import streamlit as st
from controllers.session_controller import SessionController
from controllers.driver_controller import DriverController

# ─── Page Config ───
st.set_page_config(
    page_title="F1 Insights & Strategy Explorer",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───
st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        background: linear-gradient(135deg, #E10600 0%, #FF6B6B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    .subtitle {
        color: #888;
        font-size: 1.1rem;
        margin-top: -10px;
    }
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #E10600;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1117 0%, #1A1A2E 100%);
    }
    .sidebar-header {
        color: #E10600;
        font-size: 1.3rem;
        font-weight: 700;
        border-bottom: 2px solid #E10600;
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #333, transparent);
        margin: 20px 0;
    }
    .stSelectbox label, .stMultiSelect label {
        color: #CCC !important;
    }
</style>
""", unsafe_allow_html=True)


def init_controllers():
    """Initialize controllers in session state."""
    if "session_ctrl" not in st.session_state:
        st.session_state.session_ctrl = SessionController()
    if "driver_ctrl" not in st.session_state:
        st.session_state.driver_ctrl = DriverController()


def render_sidebar():
    """
    Render the sidebar with session and driver selection.
    Implements SessionSelectionView and DriverSelectionView boundary classes.
    """
    session_ctrl = st.session_state.session_ctrl
    driver_ctrl = st.session_state.driver_ctrl

    with st.sidebar:
        st.markdown('<div class="sidebar-header">🏎️ Session Selection</div>', unsafe_allow_html=True)

        # ─── Season Selection ───
        seasons = session_ctrl.loadAvailableSeasons()
        selected_year = st.selectbox("Season", seasons, index=0)

        # ─── Race Selection ───
        races = session_ctrl.loadRaces(selected_year)
        race_names = [r.getName() for r in races]

        if race_names:
            selected_race = st.selectbox("Race", race_names, index=0)
        else:
            st.warning("No races found for this season.")
            return

        # ─── Session Selection ───
        session_types = session_ctrl.loadSessions(selected_year, selected_race)
        selected_session = st.selectbox("Session", session_types, index=len(session_types) - 1)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ─── Load Session ───
        load_btn = st.button("🔄 Load Session", use_container_width=True, type="primary")

        if load_btn:
            with st.spinner("Loading session data from FastF1..."):
                ff1_session = session_ctrl.setActiveSession(selected_year, selected_race, selected_session)
                if ff1_session is not None:
                    # Clear chart caches from previous sessions
                    for key in list(st.session_state.keys()):
                        if key.startswith("chart_"):
                            del st.session_state[key]

                    drivers = driver_ctrl.getAvailableDrivers(ff1_session)
                    st.session_state.ff1_session = ff1_session
                    st.session_state.drivers = drivers
                    st.session_state.session_loaded = True
                    st.session_state.selected_year = selected_year
                    st.session_state.selected_race = selected_race
                    st.session_state.selected_session_type = selected_session
                    st.success(f"✅ Loaded {selected_race} - {selected_session}")
                else:
                    st.error("Failed to load session.")

        # ─── Driver Selection ───
        if st.session_state.get("session_loaded", False):
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-header">👤 Driver Selection</div>', unsafe_allow_html=True)

            drivers = st.session_state.get("drivers", [])
            driver_options = {f"{d.getAbbreviation()} - {d.getName()}": d for d in drivers}
            driver_labels = list(driver_options.keys())

            if len(driver_labels) >= 2:
                d1_label = st.selectbox("Driver 1", driver_labels, index=0)
                d2_label = st.selectbox("Driver 2", driver_labels, index=1)

                d1 = driver_options[d1_label]
                d2 = driver_options[d2_label]

                is_valid, msg = driver_ctrl.validateSelection(d1, d2)
                if not is_valid:
                    st.warning(msg)
                else:
                    st.session_state.driver1 = d1
                    st.session_state.driver2 = d2
                    st.session_state.drivers_selected = True

                    # Show team color indicators
                    col1, col2 = st.columns(2)
                    with col1:
                        color1 = d1.team.getColor() if d1.team else "#FFF"
                        st.markdown(
                            f'<div style="background:{color1};height:4px;border-radius:2px;"></div>',
                            unsafe_allow_html=True,
                        )
                        st.caption(d1.getAbbreviation())
                    with col2:
                        color2 = d2.team.getColor() if d2.team else "#FFF"
                        st.markdown(
                            f'<div style="background:{color2};height:4px;border-radius:2px;"></div>',
                            unsafe_allow_html=True,
                        )
                        st.caption(d2.getAbbreviation())
            else:
                st.warning("Not enough drivers available.")


def render_home():
    """Render the home page with project overview."""
    st.markdown('<h1 class="main-title">F1 Insights & Strategy Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Analyze Formula 1 race data with interactive visualizations</p>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.get("session_loaded", False):
        # Welcome state
        st.markdown("### 👋 Welcome!")
        st.markdown("""
        Use the **sidebar** to get started:
        1. **Select a Season** — Choose from 2018 to 2024
        2. **Pick a Race** — Any Grand Prix from the calendar
        3. **Choose a Session** — Practice, Qualifying, or Race
        4. **Load the data** — Click "Load Session"
        5. **Select 2 Drivers** — Compare their performance

        Then navigate to the analysis pages using the sidebar:
        - 📊 **Lap Time Comparison** — Side-by-side pace analysis
        - 📈 **Position Over Laps** — Track position changes & overtakes
        - 🔧 **Tyre Strategy** — Visualize pit stop strategy & compounds
        """)

        # Feature cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">📊</div>
                <div class="metric-label">Lap Time Analysis</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">📈</div>
                <div class="metric-label">Position Tracking</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">🔧</div>
                <div class="metric-label">Tyre Strategy</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Session loaded state — show summary
        year = st.session_state.get("selected_year", "")
        race = st.session_state.get("selected_race", "")
        session_type = st.session_state.get("selected_session_type", "")
        drivers = st.session_state.get("drivers", [])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{year}</div>
                <div class="metric-label">Season</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">🏁</div>
                <div class="metric-label">{race}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{session_type}</div>
                <div class="metric-label">Session</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(drivers)}</div>
                <div class="metric-label">Drivers</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        if st.session_state.get("drivers_selected", False):
            d1 = st.session_state.driver1
            d2 = st.session_state.driver2
            st.markdown(f"### 🏎️ Comparing: **{d1.getName()}** vs **{d2.getName()}**")
            st.info("👈 Navigate to analysis pages using the sidebar to see detailed charts.")
        else:
            st.info("👈 Select two drivers from the sidebar to begin analysis.")


# ─── Main ───
def main():
    init_controllers()
    render_sidebar()
    render_home()


if __name__ == "__main__":
    main()
