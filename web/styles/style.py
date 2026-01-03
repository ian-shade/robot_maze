"""Streamlit styling and CSS for the application"""

import streamlit as st


def apply_custom_styling():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown("""
        <style>
        /* Make sidebar text bigger */
        [data-testid="stSidebar"] {
            font-size: 16px;
        }
        [data-testid="stSidebar"] h2 {
            font-size: 20px;
        }
        [data-testid="stSidebar"] h3 {
            font-size: 18px;
        }
        [data-testid="stSidebar"] label {
            font-size: 16px;
        }
        [data-testid="stSidebar"] .stRadio label {
            font-size: 16px;
        }

        .main {
            background-color: #f5f5f5;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
        }
        .metric-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        h1 {
            color: #2c3e50;
        }
        h2 {
            color: #34495e;
        }
        </style>
    """, unsafe_allow_html=True)
