import streamlit as st
import os
import sys
from pathlib import Path

root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

from home import render_home
from general import render_general
from team import render_team
from prediction import render_prediction

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Ligue 1 Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Sidebar custom
# -----------------------------
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio(
    "Go to:",
    options=[
        "🏠 Home",
        "📊 General",
        "🎯 Team",
        "🔮 Prediction"
    ]
)

# -----------------------------
# Render selected page
# -----------------------------
if page == "🏠 Home":
    render_home()
elif page == "📊 General":
    render_general()
elif page == "🎯 Team":
    render_team()
elif page == "🔮 Prediction":
    render_prediction()
