import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import altair as alt

from pathlib import Path
from utils.load import load_data
from utils.prediction_page import xxx
from src.config import load_config


# -------------------
# Setup paths
# -------------------
root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(root_path)

config_file = 'config.yaml'
config_path = os.path.join(root_path, config_file)
config = load_config(config_path)

TRAIN_PATH = os.path.join(root_path, config['preprocessed_dir'], config['preprocessed_train_df_name'] + '.csv')
TEST_PATH = os.path.join(root_path, config['preprocessed_dir'], config['preprocessed_test_df_name'] + '.csv')
DATE_COL = config['date_column']
SEASON_COL = config['season_column']
HOME_COL = config['home_column']
AWAY_COL = config['away_column']
HOME_GOALS = config['nb_goals_home_column']
AWAY_GOALS = config['nb_goals_away_column']
FINAL_RESULT = config['final_result_column']
df = load_data(TRAIN_PATH, TEST_PATH, DATE_COL)


# ---------------------------------------------------------
# Prediction page formatting
# ---------------------------------------------------------
def render_prediction():

    st.set_page_config(page_title="Match Prediction", page_icon="🔮", layout="wide")
    st.title("🔮 Prediction Dashboard")

    # ---------------------------------------------------------
    # Team selection
    # ---------------------------------------------------------
    teams = sorted(pd.unique(df[[HOME_COL, AWAY_COL]].values.ravel()))

    st.subheader("⚽ Select teams")

    col1, col2 = st.columns(2)
    home_team = col1.selectbox("🏠 Home team", teams)
    away_team = col2.selectbox("🚗 Away team", teams)

    if home_team == away_team:
        st.warning("⚠️ Teams must be different.")
        return

    # ---------------------------------------------------------
    # Model selection
    # ---------------------------------------------------------
    st.subheader("🧠 Select predictive models")

    st.warning("⚠️ Predictions are made on preprocessed data (cf home page to check timerange of registered matches)")

    primary_models = ["LogisticRegression", "RandomForest", "XGBoost"]
    secondary_models = ["Poisson", "RandomForest", "XGBoost"]

    col3, col4 = st.columns(2)
    primary_model = col3.selectbox("🔹 Primary model", primary_models)
    secondary_model = col4.selectbox("🔸 Secondary model", secondary_models)

    # ---------------------------------------------------------
    # Button
    # ---------------------------------------------------------
    if st.button("🔮 Predict match"):
        with st.spinner("Computing prediction..."):
            predicted_score, score_probs = predict_match(
                home_team, away_team, primary_model, secondary_model
            )

        # ---------------------------------------------------------
        # Output: score prediction
        # ---------------------------------------------------------
        st.success("Prediction complete!")

        st.subheader("🏆 Predicted final score")
        st.markdown(
            f"""
            <div style='font-size:36px; font-weight:bold; text-align:center;'>
            {home_team} <span style='color:#666;'>vs</span> {away_team}<br>
            <span style='font-size:48px;color:#0A84FF;'>{predicted_score}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---------------------------------------------------------
        # Output: probabilities table
        # ---------------------------------------------------------
        st.subheader("📊 Score probability distribution")

        score_df = pd.DataFrame(
            [{"Score": s, "Probability": round(p * 100, 2)} for s, p in score_probs.items()]
        ).sort_values("Probability", ascending=False)

        st.dataframe(
            score_df.reset_index(drop=True),
            hide_index=True,
            use_container_width=True
        )

        # Optional bar chart (clean)
        st.subheader("📈 Probability Chart")
        st.bar_chart(score_df.set_index("Score"))