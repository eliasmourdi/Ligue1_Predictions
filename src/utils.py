import pandas as pd
from config import load_config
from datetime import date


# Config file loading
config = load_config()

col_home_team = config['data']['cols_to_rename_base']['HomeTeam']
col_away_team = config['data']['cols_to_rename_base']['AwayTeam']

col_nb_goals_home_team = config['data']['cols_to_rename_base']['FTHG']
col_nb_goals_away_team = config['data']['cols_to_rename_base']['FTAG']

final_result_home = config['data']['values_to_rename_base']['final_result']['H']
final_result_away = config['data']['values_to_rename_base']['final_result']['A']
final_result_draw = config['data']['values_to_rename_base']['final_result']['D']
col_final_result = config['data']['cols_to_rename_base']['FTR']


def nb_points(df: pd.DataFrame,
              club: str
             ) -> int:
    """
    Computes the numer of points won by a club during matches present in the dataframe df
    A victory brings 3 points, a draw 1 point and a defeat 0 point

    Args:
        df: dataframe with the matches to consider
        club: team to compute the number of points

    Returns:
        The number of points won by the club during matches present in the dataframe
    """
    
    points_home = df[(df[col_home_team] == club) & ((df[col_final_result] == final_result_home) | (df[col_final_result] == final_result_draw))]
    n_pts_home = (points_home[col_final_result] == final_result_home).sum() * 3 + (points_home[col_final_result] == final_result_draw).sum()
    
    points_away = df[(df[col_away_team] == club) & ((df[col_final_result] == final_result_away) | (df[col_final_result] == final_result_draw))]
    n_pts_away = (points_away[col_final_result] == final_result_away).sum() * 3 + (points_away[col_final_result] == final_result_draw).sum()
    
    n_pts = n_pts_home + n_pts_away
    
    return n_pts


def goal_diff(df: pd.DataFrame,
              club: str
             ) -> int:
    """
    Computes the goal difference of a club during matches present in a dataframe

    Args:
        df: dataframe with the matches to consider
        club: team to compute the goal difference

    Returns:
        The goal difference of the club during the matches present in the dataframe df

    """
    
    matches_home = df[df[col_home_team] == club]
    matches_away = df[df[col_away_team] == club]

    goals_home_for = matches_home[col_nb_goals_home_team].sum()
    goals_home_against = matches_home[col_nb_goals_away_team].sum()

    goals_away_for = matches_away[col_nb_goals_away_team].sum()
    goals_away_against = matches_away[col_nb_goals_home_team].sum()

    goal_diff = goals_home_for + goals_away_for - goals_home_against - goals_away_against

    return goal_diff


def season(date: datetime.date) -> str:
    """
    Returns the season of the match from its date

    Args:
        date: date of the match

    Returns:
        The season of the match
    """
    
    month = date.month
    year = date.year
    season = ''

    if month <= 6: # a ligue 1 season ends in June max
        season = season + str(year - 1) + '/' + str(year)

    if month >= 8: # a ligue 1 season starts in August min
        season = season + str(year) + '/' + str(year + 1)

    return season


