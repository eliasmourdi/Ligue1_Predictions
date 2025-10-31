import pandas as pd


def compute_team_stats(df, 
                       col_home_team='home', 
                       col_away_team='away', 
                       col_final_result='final_result',
                       nb_goals_home_column='nb_goals_home', 
                       nb_goals_away_column='nb_goals_away') -> pd.DataFrame:
    """
    Computes statistics specific to clubs based on matches present in the dataframe df

    Args:
        df: dataframe with the matches to consider
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        col_final_result: name of the column mentionning the categorical final result ('home' for home team victory, 'away' for away team victory, 'draw' otherwise)
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        A dataframe with for each club the total of points won during the period, the number of goals scored and conceded, and the goal difference
    """
    if df.empty:
        return pd.DataFrame(columns=['team', 'points', 'goals_scored', 'goals_conceded', 'goal_diff'])
    
    # Points earned by home and away teams
    df = df.copy()
    df['home_points'] = df[col_final_result].map({'home': 3, 'draw': 1, 'away': 0})
    df['away_points'] = df[col_final_result].map({'home': 0, 'draw': 1, 'away': 3})

    # Home and away views
    home_stats = df[[col_home_team, 'home_points', nb_goals_home_column, nb_goals_away_column]].copy()
    home_stats.columns = ['team', 'points', 'goals_scored', 'goals_conceded']

    away_stats = df[[col_away_team, 'away_points', nb_goals_away_column, nb_goals_home_column]].copy()
    away_stats.columns = ['team', 'points', 'goals_scored', 'goals_conceded']

    # Combine and aggregate
    all_stats = pd.concat([home_stats, away_stats], ignore_index=True)
    agg_stats = all_stats.groupby('team', as_index=False).sum()
    agg_stats['goal_diff'] = agg_stats['goals_scored'] - agg_stats['goals_conceded']

    return agg_stats.sort_values(by=['points', 'goal_diff'], ascending=False).reset_index(drop=True)


def ranking_club(df,
                 club, 
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
    table = compute_team_stats(df, col_home_team, col_away_team, col_final_result, nb_goals_home_column, nb_goals_away_column)
    try:
        return table.index[table['team'] == club][0] + 1
    except IndexError:
        return -1


def compute_home_away_stats(df, 
                            home=True,
                            col_home_team='home',
                            col_away_team='away', 
                            col_final_result='final_result',
                            nb_goals_home_column='nb_goals_home', 
                            nb_goals_away_column='nb_goals_away') -> pd.DataFrame:
    """
    Computes statistics specific to clubs based on home or away matches present in the dataframe df, according to the home argument in the function input

    Args:
        df: dataframe with the matches to consider
        home: boolean indicating whether only home or away matches are considered
        col_home_team: name of the column mentionning the home team
        col_away_team: name of the column mentionning the away team
        col_final_result: name of the column mentionning the categorical final result ('home' for home team victory, 'away' for away team victory, 'draw' otherwise)
        nb_goals_home_column: name of the column providing the number of goals scored by home team
        nb_goals_away_column: name of the column providing the number of goals scored by away team

    Returns:
        A dataframe with for each club the total of points won during the period, the number of goals scored and conceded, and the goal difference
    """
    if df.empty:
        return pd.DataFrame(columns=['team', 'points', 'goals_scored', 'goals_conceded', 'goal_diff'])
    
    df = df.copy()
    if home:
        df['points'] = df[col_final_result].map({'home': 3, 'draw': 1, 'away': 0})
        df['goals_scored'] = df[nb_goals_home_column]
        df['goals_conceded'] = df[nb_goals_away_column]
        teams = df[col_home_team]
    else:
        df['points'] = df[col_final_result].map({'home': 0, 'draw': 1, 'away': 3})
        df['goals_scored'] = df[nb_goals_away_column]
        df['goals_conceded'] = df[nb_goals_home_column]
        teams = df[col_away_team]
    
    stats = pd.DataFrame({
        'team': teams,
        'points': df['points'],
        'goals_scored': df['goals_scored'],
        'goals_conceded': df['goals_conceded'],
        'goal_diff': df['goals_scored'] - df['goals_conceded']
    })
    agg_stats = stats.groupby('team', as_index=False).sum()
    return agg_stats.sort_values(by=['points', 'goal_diff'], ascending=False).reset_index(drop=True)


def home_ranking_club(df, 
                      club,
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
    table = compute_home_away_stats(df, True, col_home_team, col_away_team, col_final_result, nb_goals_home_column, nb_goals_away_column)
    try:
        return table.index[table['team'] == club][0] + 1
    except IndexError:
        return -1


def away_ranking_club(df, 
                      club,
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
    table = compute_home_away_stats(df, False, col_home_team, col_away_team, col_final_result, nb_goals_home_column, nb_goals_away_column)
    try:
        return table.index[table['team'] == club][0] + 1
    except IndexError:
        return -1


def attack_ranking_club(df: pd.DataFrame,
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
        The attack ranking of the club providen as input
    """
    table = compute_team_stats(df, col_home_team, col_away_team, col_final_result, nb_goals_home_column, nb_goals_away_column).sort_values(by=['goals_scored'], ascending=False).reset_index(drop=True)
    try:
        return table.index[table['team'] == club][0] + 1
    except IndexError:
        return -1


def defense_ranking_club(df: pd.DataFrame,
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
        The defense ranking of the club providen as input
    """
    table = compute_team_stats(df, col_home_team, col_away_team, col_final_result, nb_goals_home_column, nb_goals_away_column).sort_values(by=['goals_conceded'], ascending=True).reset_index(drop=True)
    try:
        return table.index[table['team'] == club][0] + 1
    except IndexError:
        return -1