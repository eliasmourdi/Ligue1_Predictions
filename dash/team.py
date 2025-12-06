import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import altair as alt

from pathlib import Path
from utils.load import load_data
from utils.team_page import compute_team_history, compute_season_kpis
from src.data_analysis import ClubAnalysis
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


# -------------------
# Render Team Page
# -------------------
def render_team():
    st.set_page_config(page_title="Team", page_icon="🎯", layout="wide")

    df = load_data(TRAIN_PATH, TEST_PATH, DATE_COL)
    
    st.title("🎯 Team Dashboard")
    
    # --- Markdown explanation ---
    st.markdown("""
    ### About this page
    Here you can analyze a specific Ligue 1 team:
    - Global KPIs over all seasons   
    - Favorite opponents and "nemesis"  
    - Filter by season to get season-specific KPIs and last matches
    """)
    
    # --- Team selector (bigger) ---
    teams = sorted(pd.unique(df[[HOME_COL, AWAY_COL]].values.ravel()))
    selected_team = st.selectbox("🔹 Select a team", teams, index=0)

    
    # --- Global KPIs ---
    team_history, all_matches = compute_team_history(
        df, selected_team,
        DATE_COL,
        SEASON_COL,
        HOME_COL,
        AWAY_COL,
        HOME_GOALS,
        AWAY_GOALS,
        FINAL_RESULT
    )
    
    st.subheader("📌 Global KPIs")
    
    # Top row 5 metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total seasons", team_history['total_seasons'])
    col2.metric("Consecutive seasons", team_history['consecutive_seasons'])
    col3.metric("Max consecutive seasons", team_history['max_consecutive_seasons'])

    col5, col6 = st.columns(2)
    col5.metric("Favorite opponent", team_history['favorite_opponent'] or "N/A")
    col6.metric("Nemesis", team_history['nemesis'] or "N/A")

    # Bottom row 3 metrics
    last = team_history['last_match']

    st.subheader("📍​ Last match")
    with st.container():
        if last is not None:
            st.markdown(f"<div style='text-align:center;'>"
                    f"<h3>{last[HOME_COL]} {last[HOME_GOALS]} - {last[AWAY_GOALS]} {last[AWAY_COL]}</h3>"
                    f"</div>", unsafe_allow_html=True)

    
    # --- Evolution charts using ClubAnalysis ---
    st.subheader("📊 Evolution")
    club = ClubAnalysis(df, selected_team, config)
    
    st.write("Points per season:")

    points_df = pd.DataFrame({
        'Season': club.points_per_season.index,
        'Points': club.points_per_season.values
    })

    chart_points = alt.Chart(points_df).mark_bar(color='blue').encode(
        x=alt.X('Season', sort=None),
        y='Points'
    ).properties(
        width=700, height=300,
        title=f"{selected_team} - Points per season"
    )
    st.altair_chart(chart_points, use_container_width=True)

    
    # Ranking per season
    st.write("Ranking per season:")

    rank_df = pd.DataFrame({
        'Season': club.rank_per_season.index,
        'Rank': club.rank_per_season.values
    }).fillna(0)

    chart_rank = alt.Chart(rank_df).mark_bar().encode(
        x=alt.X('Season:N', sort=None),
        y=alt.Y('Rank:Q', scale=alt.Scale(reverse=True)),
        color=alt.value('blue')
    ).properties(
        width=700,
        height=300,
        title=f"{selected_team} - Ranking per season"
    )
    st.altair_chart(chart_rank, use_container_width=True)

    
    # Opponent performances
    st.subheader("⚡ Opponent performance")
    opponents = pd.unique(club.club_matches[[club.config['home_column'], club.config['away_column']]].values.ravel())
    opponents = [op for op in opponents if op != selected_team]

    fav_list = []

    for op in opponents:
        matches_vs = club.club_matches[
        ((club.club_matches[club.config['home_column']] == selected_team) & (club.club_matches[club.config['away_column']] == op)) |
        ((club.club_matches[club.config['home_column']] == op) & (club.club_matches[club.config['away_column']] == selected_team))
        ]
        if len(matches_vs) >= 5:  # min 5 matches
            points = matches_vs.apply(lambda row:
            3 if (row[club.config['home_column']] == selected_team and row['home_points'] == 3) or
                 (row[club.config['away_column']] == selected_team and row['away_points'] == 3)
            else (1 if (row['home_points'] == 1 or row['away_points'] == 1) else 0),
            axis=1
            ).mean()
            fav_list.append({'Opponent': op, 'AvgPoints': round(points, 2)})

    fav_df = pd.DataFrame(fav_list).sort_values('AvgPoints', ascending=False)

    # Graphiques Altair
    chart_fav = alt.Chart(fav_df).mark_bar(color='blue').encode(
        x=alt.X('Opponent', sort='-y'),
        y='AvgPoints'
    ).properties(title=f"{selected_team} - Favorite opponents")

    st.altair_chart(chart_fav, use_container_width=True)


    # --- Filter by season ---
    st.subheader("📅 Season-specific KPIs")
    seasons = sorted(df[SEASON_COL].unique(), reverse=True)
    selected_season = st.selectbox("🔹 Select a season", seasons)
    
    df_season = df[df[SEASON_COL] == selected_season]
    season_kpis, season_matches = compute_season_kpis(
        df_season, selected_team, DATE_COL,
        HOME_COL, AWAY_COL,
        HOME_GOALS, AWAY_GOALS, FINAL_RESULT
    )
    
    last = season_kpis['last_match']
    st.subheader("📍​ Last match")
    with st.container():
        if last is not None:
            st.markdown(f"<div style='text-align:center;'>"
                    f"<h3>{last[HOME_COL]} {last[HOME_GOALS]} - {last[AWAY_GOALS]} {last[AWAY_COL]}</h3>"
                    f"</div>", unsafe_allow_html=True)

    # Table of matches
    st.subheader("📋 Matches of the selected season")
    season_matches['Date_only'] = season_matches[DATE_COL].dt.date
    season_matches.rename(columns={'Date_only': 'Date', HOME_COL: 'Home Team', AWAY_COL: 'Away Team', HOME_GOALS: 'Home Goals', AWAY_GOALS: 'Away Goals'}, inplace=True)
    st.dataframe(season_matches[['Date', 'Home Team', 'Away Team', 'Home Goals', 'Away Goals']].reset_index(drop=True))

    # Best match
    st.subheader("🚀​ Best match of the season:")
    with st.container():
        if season_kpis['best_match'] is not None:
            st.markdown(f"<div style='text-align:center;'>"
                    f"<h3>{season_kpis['best_match'][HOME_COL]} {season_kpis['best_match'][HOME_GOALS]} - {season_kpis['best_match'][AWAY_GOALS]} {season_kpis['best_match'][AWAY_COL]}</h3>"
                    f"</div>", unsafe_allow_html=True)
    
    # Worst match
    st.subheader("💢 Worst match of the season:")
    with st.container():
        if season_kpis['worst_match'] is not None:
            st.markdown(f"<div style='text-align:center;'>"
                    f"<h3>{season_kpis['worst_match'][HOME_COL]} {season_kpis['worst_match'][HOME_GOALS]} - {season_kpis['worst_match'][AWAY_GOALS]} {season_kpis['worst_match'][AWAY_COL]}</h3>"
                    f"</div>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.caption("Developed by Elias Mourdi — 2025")