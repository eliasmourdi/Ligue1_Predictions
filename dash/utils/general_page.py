import pandas as pd
import numpy as np
import streamlit as st
import altair as alt


def print_last_registered_matches(df, DATE_COL, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS):
    """
    Display the last registered matches in the dataset
    """
    st.header("📅 Last registered matches")

    last_matches = df.sort_values(DATE_COL, ascending=False).head(9).reset_index(drop=True)
    last_matches[DATE_COL] = pd.to_datetime(last_matches[DATE_COL]).dt.date
    
    last_matches_display = last_matches[
        [DATE_COL, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS]
    ].copy()

    last_matches_display.columns = ['Date', 'Home Team', 'Away Team', 'Home Goals', 'Away Goals']

    st.dataframe(last_matches_display)


def print_general_ranking(df, SEASON_COL, FINAL_RESULT, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS):
    """
    Compute and display the general ranking table for the current season
    """
    current_season = df[SEASON_COL].max()
    df_season = df[df[SEASON_COL] == current_season].copy()

    st.header(f"🏆 Current table — Season {current_season}")

    # Point mapping
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


def print_ranking_last_matches(df, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS, LAST_N_MATCHES=5):
    """
    Compute and display the ranking based on the last N matches
    """
    current_season = df['season'].max()
    df_season = df[df['season'] == current_season].copy()

    st.header(f"🔥 Form table — Last {LAST_N_MATCHES} matches (Season {current_season})")

    df_season['home_points'] = df_season['final_result'].map({'home': 3, 'draw': 1, 'away': 0})
    df_season['away_points'] = df_season['final_result'].map({'home': 0, 'draw': 1, 'away': 3})

    teams = pd.unique(df_season[[HOME_COL, AWAY_COL]].values.ravel())

    ranking_lastN = []

    for team in teams:
        team_matches = df_season[(df_season[HOME_COL] == team) | (df_season[AWAY_COL] == team)]
        team_matches = team_matches.tail(LAST_N_MATCHES)

        points = 0
        goals_scored = 0
        goals_conceded = 0

        for _, row in team_matches.iterrows():
            if row[HOME_COL] == team:
                points += row['home_points']
                goals_scored += row[HOME_GOALS]
                goals_conceded += row[AWAY_GOALS]
            else:
                points += row['away_points']
                goals_scored += row[AWAY_GOALS]
                goals_conceded += row[HOME_GOALS]

        ranking_lastN.append({
            'Team': team,
            'Points': points,
            'Goals scored': goals_scored,
            'Goals conceded': goals_conceded,
            'Goal difference': goals_scored - goals_conceded
        })

    ranking_lastN_df = pd.DataFrame(ranking_lastN)
    ranking_lastN_df = ranking_lastN_df.sort_values(by=['Points', 'Goal difference'], ascending=False)
    ranking_lastN_df.set_index('Team', inplace=True)

    st.dataframe(
        ranking_lastN_df.style.format({
            'Points': '{:.0f}',
            'Goals scored': '{:.0f}',
            'Goals conceded': '{:.0f}',
            'Goal difference': '{:.0f}'
        })
        .set_properties(**{'text-align': 'center'})
        .set_properties(subset=['Points'], **{'font-weight': 'bold'})
    )

    # ===== Top 5 teams form bar chart =====
    form_chart_df = ranking_lastN_df[['Points']].sort_values("Points", ascending=False).head(5).reset_index()

    chart = (
        alt.Chart(form_chart_df)
        .mark_bar(color='blue')
        .encode(
            x=alt.X("Team:N", sort=form_chart_df["Team"].tolist()),
            y=alt.Y("Points:Q"),
            tooltip=["Team", "Points"]
        )
    )

    st.altair_chart(chart, use_container_width=True)