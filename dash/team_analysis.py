import streamlit as st
import pandas as pd
from app_test_page1 import load_data, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS, FINAL_RESULT, SEASON_COL, DATE_COL

df = load_data()
current_season = df[SEASON_COL].max()
df_season = df[df[SEASON_COL] == current_season].copy()

st.title("📈 Team Analysis")

teams = pd.unique(df_season[[HOME_COL, AWAY_COL]].values.ravel())
selected_team = st.selectbox("Select a team", teams)

team_matches = df_season[(df_season[HOME_COL] == selected_team) | (df_season[AWAY_COL] == selected_team)].sort_values(DATE_COL, ascending=False)

# Last matches
st.subheader("📅 Last matches")
last_team_matches = team_matches.head(9)
st.dataframe(last_team_matches[[DATE_COL, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS]])

# Form / last 5 matches
st.subheader("🔥 Form over last 5 matches")
last5 = team_matches.head(5)
last5['Result'] = last5.apply(
    lambda row: 'W' if (row[HOME_COL]==selected_team and row[FINAL_RESULT]=='home') or
                        (row[AWAY_COL]==selected_team and row[FINAL_RESULT]=='away')
                else ('D' if row[FINAL_RESULT]=='draw' else 'L'), axis=1
)
st.bar_chart(last5['Result'].map({'W':3, 'D':1, 'L':0}))

# Current ranking of the team
st.subheader("🏆 Current ranking")
# (tu peux réutiliser ton code de ranking général pour récupérer la ligne du team)

# Evolution du classement sur la saison
st.subheader("📊 Ranking evolution")
# Exemple : construire un dataframe cumulative points par match

# Largest win / loss
st.subheader("💥 Biggest victory / defeat")
team_home = team_matches[team_matches[HOME_COL]==selected_team]
team_away = team_matches[team_matches[AWAY_COL]==selected_team]

# Calculer goal diff
team_home['goal_diff'] = team_home[HOME_GOALS] - team_home[AWAY_GOALS]
team_away['goal_diff'] = team_away[AWAY_GOALS] - team_away[HOME_GOALS]
all_matches = pd.concat([team_home, team_away])
st.write(all_matches.loc[all_matches['goal_diff'].idxmax(), ['Date', HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS]])
st.write(all_matches.loc[all_matches['goal_diff'].idxmin(), ['Date', HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS]])
