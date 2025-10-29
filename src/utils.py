import pandas as pd
import datetime


def season(date: datetime.date) -> str:
    """
    Returns the season of the match from its date, under the format 'year1/year2'
    For instance, if a match was played at September 2012, the corresponding season is '2012/2013'

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


def gen_ranking(df: pd.DataFrame, club: str) -> int:
    """
    Computes the ranking of a team from matches present in a dataframe
    The ranking is computed with the number of points of each team. In case of equality, the goal difference is taken into consideration
    
    Args:
        df: dataframe to consider to compute the ranking
        club: club to compute the ranking
        
    Returns:
        The ranking of the team
    """
    
    if df.empty:
        return -1
    
    home_points = df.groupby(col_home_team)[col_final_result].apply(lambda x: (x == final_result_home).sum() * 3 + (x == final_result_draw).sum()).reset_index(name = 'points')
    away_points = df.groupby(col_away_team)[col_final_result].apply(lambda x: (x == final_result_away).sum() * 3 + (x == final_result_draw).sum()).reset_index(name = 'points')
    total_points = pd.merge(home_points, away_points, left_on = col_home_team, right_on = col_away_team, how='outer', suffixes = ('_home', '_away')).fillna(0)
 
    total_points['total_points'] = total_points['points_home'] + total_points['points_away']
    
    total_points['team'] = total_points[col_home_team].fillna(total_points[col_away_team])
    total_points['goal_diff'] = total_points['team'].apply(lambda x: goal_diff(df, x))
    
    total_points = total_points.sort_values(by=['total_points', 'goal_diff'], ascending=False).reset_index(drop=True)
    
    if (total_points['team'] == club).any():
        ranking = total_points[total_points['team'] == club].index[0] + 1
    else:
        ranking = -1
        
    return ranking