import streamlit as st
from web.styles.style import apply_custom_styling
from web.ui.screens import setup_screen, visualization_screen


def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="🤖 Pathfinding Visualizer",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'env' not in st.session_state:
        st.session_state.env = None
    if 'robot' not in st.session_state:
        st.session_state.robot = None
    if 'problem' not in st.session_state:
        st.session_state.problem = None
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'algorithm' not in st.session_state:
        st.session_state.algorithm = None
    if 'setup_complete' not in st.session_state:
        st.session_state.setup_complete = False


def main():
    """Main application entry point - handles routing between screens"""
    # Configure page
    configure_page()
    
    # Apply custom styling
    apply_custom_styling()
    
    # Initialize session state
    initialize_session_state()
    
    # Route to appropriate screen
    if st.session_state.setup_complete:
        visualization_screen()
    else:
        setup_screen()


if __name__ == "__main__":
    main()
