import pandas as pd


def nb_points(df: pd.DataFrame,
              club: str,
              col_home_team='home',
              col_away_team='away',
              col_final_result='final_result') -> int:
    """
    Computes the number of points won by a club during matches present in the dataframe df
    A victory brings 3 points, a draw 1 point and a defeat 0 point

    Args:
        df: dataframe with the matches to consider
        club: team to compute the number of points
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        col_final_result: name of the column mentionning the categorical final result ('home' for home team victory, 'away' for away team victory, 'draw' otherwise)

    Returns:
        The number of points won by the club during matches present in the dataframe
    """
    if df.empty:
        return -1 # if no matches were played, arbitrary value
    
    points_home = df[(df[col_home_team] == club) & ((df[col_final_result] == 'home') | (df[col_final_result] == 'draw'))]
    n_pts_home = (points_home[col_final_result] == 'home').sum() * 3 + (points_home[col_final_result] == 'draw').sum()
    
    points_away = df[(df[col_away_team] == club) & ((df[col_final_result] == 'away') | (df[col_final_result] == 'draw'))]
    n_pts_away = (points_away[col_final_result] == 'away').sum() * 3 + (points_away[col_final_result] == 'draw').sum()
    
    n_pts = n_pts_home + n_pts_away
    
    return n_pts


def goals_scored(df: pd.DataFrame,
                 club: str,
                 col_home_team='home',
                 col_away_team='away',
                 nb_goals_home_column='nb_goals_home',
                 nb_goals_away_column='nb_goals_away') -> int:
    """
    Computes the number of goals scored by a club during the matches present in the dataframe df

    Args:
        df: dataframe with the matches to consider
        club: team to compute the goal difference
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The number of goals scored by the club during the matches present in the dataframe df
    """
    if df.empty:
        return -1 # if no matches were played, arbitrary value
        
    return df.loc[df[col_home_team] == club, nb_goals_home_column].sum() + df.loc[df[col_away_team] == club, nb_goals_away_column].sum()


def goals_conceded(df: pd.DataFrame,
                   club: str,
                   col_home_team='home',
                   col_away_team='away',
                   nb_goals_home_column='nb_goals_home',
                   nb_goals_away_column='nb_goals_away') -> int:
    """
    Computes the number of goals conceded by a club during the matches present in the dataframe df

    Args:
        df: dataframe with the matches to consider
        club: team to compute the goal difference
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The number of goals conceded by the club during the matches present in the dataframe df
    """
    if df.empty:
        return -1 # if no matches were played, arbitrary value
        
    return df.loc[df[col_home_team] == club, nb_goals_away_column].sum() + df.loc[df[col_away_team] == club, nb_goals_home_column].sum()


def goal_diff(df: pd.DataFrame,
              club: str,
              col_home_team='home',
              col_away_team='away',
              nb_goals_home_column='nb_goals_home',
              nb_goals_away_column='nb_goals_away') -> int:
    """
    Computes the goal difference of a club during matches present in the dataframe df

    Args:
        df: dataframe with the matches to consider
        club: team to compute the goal difference
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The goal difference of the club during the matches present in the dataframe df
    """
    if df.empty:
        return -1 # if no matches were played, arbitrary value
        
    scored = goals_scored(df, club, col_home_team, col_away_team, nb_goals_home_column, nb_goals_away_column)
    conceded = goals_conceded(df, club, col_home_team, col_away_team, nb_goals_home_column, nb_goals_away_column)

    return scored - conceded


def ranking_table(df: pd.DataFrame,
                  col_home_team='home',
                  col_away_team='away',
                  col_final_result='final_result',
                  nb_goals_home_column='nb_goals_home',
                  nb_goals_away_column='nb_goals_away') -> pd.DataFrame:
    """
    Args:
        df: dataframe with the matches to consider
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        col_final_result: name of the column mentionning the categorical final result ('home' for home team victory, 'away' for away team victory, 'draw' otherwise)
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The table with the rankings of all teams present in the dataframe providen as input. The ranking is computed according to the number of points. In case of equality, the goal difference is taken into consideration
    """
    if df.empty:
        return pd.DataFrame(columns=['team', 'points', 'goal_diff'])
        
    teams = pd.concat([df[col_home_team], df[col_away_team]]).unique()
    table = pd.DataFrame({
        'team': teams,
        'points': [nb_points(df, t, col_home_team, col_away_team, col_final_result) for t in teams],
        'goal_diff': [goal_diff(df, t, col_home_team, col_away_team, nb_goals_home_column, nb_goals_away_column) for t in teams]
    })
    return table.sort_values(by=['points', 'goal_diff'], ascending=False).reset_index(drop=True)


def ranking_club(df: pd.DataFrame,
                 club: str,
                 col_home_team='home',
                 col_away_team='away',
                 col_final_result='final_result',
                 nb_goals_home_column='nb_goals_home',
                 nb_goals_away_column='nb_goals_away') -> int:
    """
    Args:
        df: dataframe with the matches to consider
        club: team to compute the goal difference
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        col_final_result: name of the column mentionning the categorical final result ('home' for home team victory, 'away' for away team victory, 'draw' otherwise)
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The ranking of the club providen as input. The ranking is computed according to the number of points. In case of equality, the goal difference is taken into consideration
    """
    table = ranking_table(df, col_home_team, col_away_team, col_final_result, nb_goals_home_column, nb_goals_away_column)
    row = table.loc[table['team'] == club]
    return int(row.index[0] + 1) if not row.empty else -1 # if no matches were played, arbitrary value


def home_ranking_table(df: pd.DataFrame,
                       col_home_team='home',
                       col_away_team='away',
                       col_final_result='final_result',
                       nb_goals_home_column='nb_goals_home',
                       nb_goals_away_column='nb_goals_away') -> pd.DataFrame:
    """
    Compute rankings for home games only
    """
    if df.empty:
        return pd.DataFrame(columns=['team', 'home_points', 'home_goal_diff'])
    
    teams = pd.concat([df[col_home_team], df[col_away_team]]).unique()
    
    table = pd.DataFrame({
        'team': teams,
        'home_points': [nb_points(df[df[col_home_team] == t], t, col_home_team, col_away_team, col_final_result) for t in teams],
        'home_goal_diff': [goal_diff(df[df[col_home_team] == t], t, col_home_team, col_away_team, nb_goals_home_column, nb_goals_away_column) for t in teams]
    })
    
    return table.sort_values(by=['home_points', 'home_goal_diff'], ascending=False).reset_index(drop=True)


def home_ranking_club(df: pd.DataFrame,
                      club: str,
                      col_home_team='home',
                      col_away_team='away',
                      col_final_result='final_result',
                      nb_goals_home_column='nb_goals_home',
                      nb_goals_away_column='nb_goals_away') -> int:
    """
    Args:
        df: dataframe with the matches to consider
        club: team to compute the goal difference
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        col_final_result: name of the column mentionning the categorical final result ('home' for home team victory, 'away' for away team victory, 'draw' otherwise)
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The home ranking of the club providen as input. The ranking is computed according to the number of points. In case of equality, the goal difference is taken into consideration
    """
    table = home_ranking_table(df, col_home_team, col_away_team, col_final_result, nb_goals_home_column, nb_goals_away_column)
    row = table.loc[table['team'] == club]
    return int(row.index[0] + 1) if not row.empty else -1 # if no matches were played, arbitrary value


def away_ranking_table(df: pd.DataFrame,
                       col_home_team='home',
                       col_away_team='away',
                       col_final_result='final_result',
                       nb_goals_home_column='nb_goals_home',
                       nb_goals_away_column='nb_goals_away') -> pd.DataFrame:
    """
    Compute rankings for away games only
    """
    if df.empty:
        return pd.DataFrame(columns=['team', 'away_points', 'away_goal_diff'])
    
    teams = pd.concat([df[col_home_team], df[col_away_team]]).unique()
    
    table = pd.DataFrame({
        'team': teams,
        'away_points': [nb_points(df[df[col_away_team] == t], t, col_home_team, col_away_team, col_final_result) for t in teams],
        'away_goal_diff': [goal_diff(df[df[col_away_team] == t], t, col_home_team, col_away_team, nb_goals_home_column, nb_goals_away_column) for t in teams]
    })
    
    return table.sort_values(by=['away_points', 'away_goal_diff'], ascending=False).reset_index(drop=True)


def away_ranking_club(df: pd.DataFrame,
                      club: str,
                      col_home_team='home',
                      col_away_team='away',
                      col_final_result='final_result',
                      nb_goals_home_column='nb_goals_home',
                      nb_goals_away_column='nb_goals_away') -> int:
    """
    Args:
        df: dataframe with the matches to consider
        club: team to compute the goal difference
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        col_final_result: name of the column mentionning the categorical final result ('home' for home team victory, 'away' for away team victory, 'draw' otherwise)
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The away ranking of the club providen as input. The ranking is computed according to the number of points. In case of equality, the goal difference is taken into consideration
    """
    table = away_ranking_table(df, col_home_team, col_away_team, col_final_result, nb_goals_home_column, nb_goals_away_column)
    row = table.loc[table['team'] == club]
    return int(row.index[0] + 1) if not row.empty else -1 # if no matches were played, arbitrary value


def attack_ranking_table(df: pd.DataFrame,
                         col_home_team='home',
                         col_away_team='away',
                         nb_goals_home_column='nb_goals_home',
                         nb_goals_away_column='nb_goals_away') -> pd.DataFrame:
    """
    Args:
        df: dataframe with the matches to consider
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The table with the rankings of all teams present in the dataframe providen as input, according to their number of goals scored
    """
    if df.empty:
        return pd.DataFrame(columns=['team', 'goals_scored'])
        
    teams = pd.concat([df[col_home_team], df[col_away_team]]).unique()
    table = pd.DataFrame({
        'team': teams,
        'goals_scored': [goals_scored(df, t, col_home_team, col_away_team, nb_goals_home_column, nb_goals_away_column) for t in teams]
    })
    return table.sort_values(by=['goals_scored'], ascending=False).reset_index(drop=True)


def attack_ranking_club(df: pd.DataFrame,
                        club: str,
                        col_home_team='home',
                        col_away_team='away',
                        nb_goals_home_column='nb_goals_home',
                        nb_goals_away_column='nb_goals_away') -> int:
    """
    Args:
        df: dataframe with the matches to consider
        club: team to compute the goal difference
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The attack ranking of the club providen as input
    """
    table = attack_ranking_table(df, col_home_team, col_away_team, nb_goals_home_column, nb_goals_away_column)
    row = table.loc[table['team'] == club]
    return int(row.index[0] + 1) if not row.empty else -1 # if no matches were played, arbitrary value


def defense_ranking_table(df: pd.DataFrame,
                          col_home_team='home',
                          col_away_team='away',
                          nb_goals_home_column='nb_goals_home',
                          nb_goals_away_column='nb_goals_away') -> pd.DataFrame:
    """
    Args:
        df: dataframe with the matches to consider
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The table with the rankings of all teams present in the dataframe providen as input, according to their number of goals conceded
    """
    if df.empty:
        return pd.DataFrame(columns=['team', 'goals_conceded'])
        
    teams = pd.concat([df[col_home_team], df[col_away_team]]).unique()
    table = pd.DataFrame({
        'team': teams,
        'goals_conceded': [goals_conceded(df, t, col_home_team, col_away_team, nb_goals_home_column, nb_goals_away_column) for t in teams]
    })
    return table.sort_values(by=['goals_conceded'], ascending=True).reset_index(drop=True)


def defense_ranking_club(df: pd.DataFrame,
                         club: str,
                         col_home_team='home',
                         col_away_team='away',
                         nb_goals_home_column='nb_goals_home',
                         nb_goals_away_column='nb_goals_away') -> int:
    """
    Args:
        df: dataframe with the matches to consider
        club: team to compute the goal difference
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        The defense ranking of the club providen as input
    """
    table = defense_ranking_table(df, col_home_team, col_away_team, nb_goals_home_column, nb_goals_away_column)
    row = table.loc[table['team'] == club]
    return int(row.index[0] + 1) if not row.empty else -1 # if no matches were played, arbitrary value