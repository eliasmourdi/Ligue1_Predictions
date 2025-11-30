import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(root_path)

from src.config import load_config
from src.modeling import load_model

# config.yaml importation
config_file = 'config.yaml'
config_path = os.path.join(root_path, config_file)
config = load_config(config_path)


# -----------------------------
# Constants
# -----------------------------
TRAIN_PATH = os.path.join(os.path.join(root_path, config['preprocessed_dir']), config['preprocessed_train_df_name'] + '.csv')
TEST_PATH = os.path.join(os.path.join(root_path, config['preprocessed_dir']), config['preprocessed_test_df_name'] + '.csv')

DATE_COL = config['date_column']
SEASON_COL = config['season_column']
HOME_COL = config['home_column']
AWAY_COL = config['away_column']
HOME_GOALS = config['nb_goals_home_column']
AWAY_GOALS = config['nb_goals_away_column']
FINAL_RESULT = config['final_result_column']


# -----------------------------
# Data loading
# -----------------------------
@st.cache_data
def load_data():
    train = pd.read_csv(TRAIN_PATH, parse_dates=[DATE_COL])
    test = pd.read_csv(TEST_PATH, parse_dates=[DATE_COL])
    df = pd.concat([train, test], ignore_index=True)
    return df.sort_values(DATE_COL)

df = load_data()


# -----------------------------
# Overview page
# -----------------------------
st.title("📊 Ligue 1 — Dashboard Overview")

# ===== Last matches =====
st.header("📅 Last registered matches")

last_matches = df.sort_values(DATE_COL, ascending=False).head(9).reset_index(drop=True)
last_matches[DATE_COL] = pd.to_datetime(last_matches[DATE_COL]).dt.date
last_matches_display = last_matches[
    [DATE_COL, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS]
].copy()
last_matches_display.columns = ['Date', 'Home Team', 'Away Team', 'Home Goals', 'Away Goals']

st.dataframe(
    last_matches_display
)

# ===== General ranking =====
current_season = df[SEASON_COL].max()
df_season = df[df[SEASON_COL] == current_season].copy()

st.header(f"🏆 Current table {current_season}")

# Mapping points
df_season['home_points'] = df_season[FINAL_RESULT].map({'home': 3, 'draw': 1, 'away': 0})
df_season['away_points'] = df_season[FINAL_RESULT].map({'home': 0, 'draw': 1, 'away': 3})

home_stats = df_season.groupby(HOME_COL).agg(
    points_home=('home_points', 'sum'),
    goals_scored_home=(HOME_GOALS, 'sum'),
    goals_conceded_home=(AWAY_GOALS, 'sum'),
    matches_home=('home_points', 'count')
)

away_stats = df_season.groupby(AWAY_COL).agg(
    points_away=('away_points', 'sum'),
    goals_scored_away=(AWAY_GOALS, 'sum'),
    goals_conceded_away=(HOME_GOALS, 'sum'),
    matches_away=('away_points', 'count')
)

# Fusion
ranking = home_stats.join(away_stats, how='outer').fillna(0)

ranking['Points'] = ranking['points_home'] + ranking['points_away']
ranking['Played Matches'] = ranking['matches_home'] + ranking['matches_away']
ranking['Goals scored'] = ranking['goals_scored_home'] + ranking['goals_scored_away']
ranking['Goals conceded'] = ranking['goals_conceded_home'] + ranking['goals_conceded_away']
ranking['Goal difference'] = ranking['Goals scored'] - ranking['Goals conceded']

ranking = ranking.sort_values(by=['Points', 'Goal difference'], ascending=False)

ranking.index.name = 'Team'

st.dataframe(
    ranking[['Points', 'Played Matches', 'Goals scored', 'Goals conceded', 'Goal difference']]
    .style.format({
        'Points': '{:.0f}',
        'Played Matches': '{:.0f}',
        'Goals scored': '{:.0f}',
        'Goals conceded': '{:.0f}',
        'Goal difference': '{:.0f}'
    })
    .set_properties(**{'text-align': 'center'})
    .set_properties(subset=['Points'], **{'font-weight': 'bold'})
)

# ===== 3. Ranking on last 5 matches =====
LAST_N_MATCHES = 5

current_season = df['season'].max()
df_season = df[df['season'] == current_season].copy()

st.header(f"🔥 Table over last {LAST_N_MATCHES} matches - {current_season}")

# Mapping points
df_season['home_points'] = df_season['final_result'].map({'home': 3, 'draw': 1, 'away': 0})
df_season['away_points'] = df_season['final_result'].map({'home': 0, 'draw': 1, 'away': 3})

teams = pd.unique(df_season[[HOME_COL, AWAY_COL]].values.ravel())

ranking_last5 = []

for team in teams:
    team_matches = df_season[(df_season[HOME_COL] == team) | (df_season[AWAY_COL] == team)].tail(LAST_N_MATCHES)
    
    points = 0
    goals_scored = 0
    goals_conceded = 0
    played_matches = len(team_matches)
    
    for _, row in team_matches.iterrows():
        if row[HOME_COL] == team:
            points += row['home_points']
            goals_scored += row[HOME_GOALS]
            goals_conceded += row[AWAY_GOALS]
        else:
            points += row['away_points']
            goals_scored += row[AWAY_GOALS]
            goals_conceded += row[HOME_GOALS]
    
    ranking_last5.append({
        'Team': team,
        'Points': points,
        'Played Matches': played_matches,
        'Goals scored': goals_scored,
        'Goals conceded': goals_conceded,
        'Goal difference': goals_scored - goals_conceded
    })

ranking_last5_df = pd.DataFrame(ranking_last5)
ranking_last5_df = ranking_last5_df.sort_values(by=['Points', 'Goal difference'], ascending=False)
ranking_last5_df.set_index('Team', inplace=True)

st.dataframe(
    ranking_last5_df.style.format({
        'Points': '{:.0f}',
        'Played Matches': '{:.0f}',
        'Goals scored': '{:.0f}',
        'Goals conceded': '{:.0f}',
        'Goal difference': '{:.0f}'
    })
    .set_properties(**{'text-align': 'center'})
    .set_properties(subset=['Points'], **{'font-weight': 'bold'})
)