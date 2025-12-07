import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import altair as alt
from pathlib import Path

from utils.load import load_data
from utils.general_page import print_last_registered_matches, print_general_ranking, print_ranking_last_matches

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
# General page formatting
# -----------------------------------
def render_general():
    st.set_page_config(page_title="General", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
    st.title("📊 General Dashboard")
    
    SEASON_COL = config['season_column']
    HOME_COL = config['home_column']
    AWAY_COL = config['away_column']
    HOME_GOALS = config['nb_goals_home_column']
    AWAY_GOALS = config['nb_goals_away_column']
    FINAL_RESULT = config['final_result_column']

    start_date = df[DATE_COL].min().date()
    end_date = df[DATE_COL].max().date()

    print_last_registered_matches(df, DATE_COL, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS)
    print_general_ranking(df, SEASON_COL, FINAL_RESULT, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS)
    print_ranking_last_matches(df, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.caption("Developed by Elias Mourdi — 2025")
