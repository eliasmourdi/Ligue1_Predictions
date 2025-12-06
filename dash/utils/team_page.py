import pandas as pd
import numpy as np
import os
import sys

root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
root_path = os.path.abspath(os.path.join(root_path, ".."))
sys.path.append(root_path)

from src.data_analysis import ClubAnalysis


def longest_consecutive_seasons(seasons):
    """Return length of the longest consecutive seasons streak"""
    if len(seasons) == 0:
        return 0
    seasons_sorted = sorted(seasons)
    longest = 1
    current_streak = 1
    for i in range(1, len(seasons_sorted)):
        if seasons_sorted[i] == seasons_sorted[i-1] + 1:
            current_streak += 1
            longest = max(longest, current_streak)
        else:
            current_streak = 1
    return longest


def compute_team_history(df, team, DATE_COL, SEASON_COL, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS, FINAL_RESULT):
    """Returns all matches played by team and KPIs over all seasons"""
    team_matches = df[(df[HOME_COL]==team) | (df[AWAY_COL]==team)].copy()
    team_matches.sort_values(DATE_COL, inplace=True)
    
    # Total and consecutive seasons
    seasons_list = team_matches[SEASON_COL].unique()
    total_seasons = len(seasons_list)
    
    total_seasons_first_years = []
    for season in seasons_list:
        total_seasons_first_years.append(int(season.rsplit('/')[0]))

    # Max consecutive seasons
    max_consecutive_seasons = longest_consecutive_seasons(total_seasons_first_years)

    # Number of current consecutive seasons
    df[DATE_COL] = pd.to_datetime(df[DATE_COL])
    current_year = df[DATE_COL].dt.year.max()
    consecutive_seasons = 0
    while current_year - 1 in total_seasons_first_years:
        current_year -= 1
        consecutive_seasons += 1
    
    # Last match
    last_match = team_matches.iloc[-1]
    
    # Best / worst match
    team_matches['goal_diff'] = np.where(team_matches[HOME_COL]==team,
                                        team_matches[HOME_GOALS]-team_matches[AWAY_GOALS],
                                        team_matches[AWAY_GOALS]-team_matches[HOME_GOALS])
    best_match = team_matches.loc[team_matches['goal_diff'].idxmax()]
    worst_match = team_matches.loc[team_matches['goal_diff'].idxmin()]
    
    # Opponent points
    team_matches['points'] = team_matches.apply(
        lambda row: 3 if (row[HOME_COL]==team and row[FINAL_RESULT]=='home') or 
                         (row[AWAY_COL]==team and row[FINAL_RESULT]=='away')
                    else (1 if row[FINAL_RESULT]=='draw' else 0),
        axis=1
    )
    opponent_stats = {}
    opponents = pd.unique(team_matches[[HOME_COL, AWAY_COL]].values.ravel())
    for op in opponents:
        if op==team: 
            continue
        op_matches = team_matches[(team_matches[HOME_COL]==op) | (team_matches[AWAY_COL]==op)]
        if len(op_matches)>=5:
            avg_pts = op_matches['points'].mean()
            opponent_stats[op] = avg_pts
    favorite_opponent = max(opponent_stats, key=opponent_stats.get) if opponent_stats else None
    nemesis = min(opponent_stats, key=opponent_stats.get) if opponent_stats else None
    
    # Evolution per season
    evolution = team_matches.groupby('season')['points'].sum().cumsum().reset_index()
    
    return {
        'total_seasons': total_seasons,
        'consecutive_seasons': consecutive_seasons,
        'max_consecutive_seasons': max_consecutive_seasons,
        'last_match': last_match,
        'best_match': best_match,
        'worst_match': worst_match,
        'favorite_opponent': favorite_opponent,
        'nemesis': nemesis,
        'evolution': evolution
    }, team_matches


def compute_season_kpis(df_season, team, DATE_COL, HOME_COL, AWAY_COL, HOME_GOALS, AWAY_GOALS, FINAL_RESULT):
    """Computes KPIs for a selected season"""
    season_matches = df_season[(df_season[HOME_COL]==team) | (df_season[AWAY_COL]==team)].copy()
    season_matches.sort_values(DATE_COL, inplace=True)
    
    # Last match
    last_match = season_matches.iloc[-1] if not season_matches.empty else None
    
    # Points over last 5 matches
    last5 = season_matches.tail(5)
    last5_points = last5.apply(
        lambda row: 3 if (row[HOME_COL]==team and row[FINAL_RESULT]=='home') or
                          (row[AWAY_COL]==team and row[FINAL_RESULT]=='away')
                    else (1 if row[FINAL_RESULT]=='draw' else 0),
        axis=1
    ).sum() if not last5.empty else 0
    
    # Best / worst match
    season_matches['goal_diff'] = np.where(season_matches[HOME_COL]==team,
                                         season_matches[HOME_GOALS]-season_matches[AWAY_GOALS],
                                         season_matches[AWAY_GOALS]-season_matches[HOME_GOALS])
    best_match = season_matches.loc[season_matches['goal_diff'].idxmax()] if not season_matches.empty else None
    worst_match = season_matches.loc[season_matches['goal_diff'].idxmin()] if not season_matches.empty else None
    
    return {
        'last_match': last_match,
        'last5_points': last5_points,
        'best_match': best_match,
        'worst_match': worst_match
    }, season_matches