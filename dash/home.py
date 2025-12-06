import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import os
import sys
from pathlib import Path

from utils.load import load_data

root_path = os.path.abspath(os.path.join(os.getcwd(), "..")) 
sys.path.append(root_path)

from src.config import load_config


# -----------------------------------
# Useful import
# -----------------------------------
# config.yaml import
config_file = 'config.yaml'
config_path = os.path.join(root_path, config_file) 
config = load_config(config_path) 

# Train test dataframes import 
TRAIN_PATH = os.path.join(os.path.join(root_path, config['preprocessed_dir']), config['preprocessed_train_df_name'] + '.csv') 
TEST_PATH = os.path.join(os.path.join(root_path, config['preprocessed_dir']), config['preprocessed_test_df_name'] + '.csv')
DATE_COL = config['date_column']
df = load_data(TRAIN_PATH, TEST_PATH, DATE_COL)

start_date = df[DATE_COL].min().date()
end_date = df[DATE_COL].max().date()


# -----------------------------------
# Home page formatting
# -----------------------------------
def render_home():
    st.set_page_config(page_title="Home", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

    st.title("🏠 Ligue 1 — Dashboard Overview")

    st.markdown(f"""
### 📝 About this platform

Welcome to the **Ligue 1 Football Analytics Dashboard**!

Here, you will find:

- 📊 **General dashboard** – global rankings, form indicators, match history  
- 🎯 **Team dashboard** – detailed team-level insights, trends, performance profiles  
- 🔮 **Prediction module** – compute match probabilities using trained statistical models

**Data coverage:**  
➡ The dataset currently includes Ligue 1 matches from **{start_date}** to **{end_date}**

If you wish to update the data, please follow the repository documentation explaining how to rerun the full pipeline.

---

📨 *Email:* **eliasmourdi@gmail.com**  
🔗 *GitHub:* https://github.com/eliasmourdi  
🔗 *LinkedIn:* https://www.linkedin.com/in/elias-mourdi-601112205/  
    """)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.caption("Developed by Elias Mourdi — 2025")
