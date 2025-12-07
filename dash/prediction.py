import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import altair as alt

from scipy.stats import poisson
from pathlib import Path
from utils.load import load_data
from utils.prediction_page import build_preprocessed_input_row, primary_prediction, secondary_prediction
from src.config import load_config
from src.feature_engineering import create_diff_features


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
    seasons = sorted(pd.unique(df[[SEASON_COL]].values.ravel()))

    st.subheader("⚽ Select match context")

    col1, col2, col3 = st.columns(3)
    season = col1.selectbox("⌛ Season", seasons)
    home_team = col2.selectbox("🏠 Home team", teams)
    away_team = col3.selectbox("🚗 Away team", teams)

    if home_team == away_team:
        st.warning("⚠️ Teams must be different.")
        return

    st.subheader("💲 Specify odds")
    col1, col2, col3 = st.columns(3)
    odd_home = col1.number_input("↗️ Odd home victory", min_value=1.0, step=0.1, format="%.2f")
    odd_draw = col2.number_input("➡️ Odd draw", min_value=1.0, step=0.1, format="%.2f")
    odd_away = col3.number_input("↘️ Odd away victory", min_value=1.0, step=0.1, format="%.2f")

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

            input_row = build_preprocessed_input_row(df, home_team, away_team, season, odd_home, odd_draw, odd_away, config)
            input_row = pd.DataFrame([input_row])

            patterns = [
                    ("_home_team_ranking_at_home", "_away_team_ranking_away"),
                    ("_home_team_at_home", "_away_team_away"),
                    ("_home_team", "_away_team"),
                    ("_at_home", "_away"),
                    ("_home", "_away")
            ]
            input_row_processed = create_diff_features(input_row, patterns=patterns)

            
            proba_home, proba_draw, proba_away = primary_prediction(
                input_row_processed, primary_model, config
            )

            lambda_home, lambda_away = secondary_prediction(input_row, secondary_model, proba_home, proba_draw, proba_away, config)

        # ---------------------------------------------------------
        # Output: score prediction
        # ---------------------------------------------------------
        st.success("Prediction complete!")

        st.subheader("🏆 Predicted final score")
        st.markdown(
            f"""
            <div style='font-size:36px; font-weight:bold; text-align:center;'>
            {home_team} <span style='color:#666;'>vs</span> {away_team}<br>
            <span style='font-size:48px;color:#0A84FF;'>{int(round(lambda_home, 0))}-{int(lambda_away)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        ) # advantage for home team / penalization for away team

        # ---------------------------------------------------------
        # Output: probabilities table
        # ---------------------------------------------------------
        st.subheader("📊 Result probability distribution")

        result_probs = {
            f"{home_team} win": round(proba_home * 100, 2),
            "Draw": round(proba_draw * 100, 2),
            f"{away_team} win": round(proba_away * 100, 2)
        }
        st.table(pd.DataFrame(list(result_probs.items()), columns=["Result", "Probability (%)"]))

        # Secondary models
        st.subheader("📈 Goal Distribution per Team")

        max_goals_plot = 8
        x = np.arange(0, max_goals_plot + 1)

        if secondary_model == "Poisson":
            home_probs = poisson.pmf(x, lambda_home)
            away_probs = poisson.pmf(x, lambda_away)
        else:
            N_sim = 5000

            home_goals_samples = np.round(lambda_home + np.random.randn(N_sim) * 1.5).clip(0, max_goals_plot).astype(int)
            away_goals_samples = np.round(lambda_away + np.random.randn(N_sim) * 1.5).clip(0, max_goals_plot).astype(int)
    
            home_probs = np.array([np.mean(home_goals_samples == i) for i in x])
            away_probs = np.array([np.mean(away_goals_samples == i) for i in x])
    
        df_goals = pd.DataFrame({
            f"{home_team}": home_probs,
            f"{away_team}": away_probs
        }, index=x)
        
        df_goals_chart = df_goals.reset_index().melt(id_vars='index', var_name='Team', value_name='Probability')
        df_goals_chart.rename(columns={'index': 'Goals'}, inplace=True)
        
        chart = alt.Chart(df_goals_chart).mark_line(point=True).encode(
            x=alt.X('Goals:O', axis=alt.Axis(labelAngle=0, title="Goals")),
            y='Probability:Q',
            color='Team:N'
        ).properties(
            width=600,
            height=400
        )
        
        st.altair_chart(chart, use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.caption("Developed by Elias Mourdi — 2025")