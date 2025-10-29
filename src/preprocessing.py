import pandas as pd
from typing import Sequence
import warnings


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
        col_final_result: name of the column mentionning the categorical final result (home for home team victory, away for away team victory, draw otherwise)

    Returns:
        The number of points won by the club during matches present in the dataframe
    """
    if club not in df['home'].unique():
        warnings.warn(f"{club} did not play home in the dataframe providen as input")
    if club not in df['away'].unique():
        warnings.warn(f"{club} did not play away in the dataframe providen as input")
    if (club not in df['home'].unique()) and (club not in df['away'].unique()):
        raise AttributeError(f"{club} did not play in the dataframe providen as input")
    
    points_home = df[(df[col_home_team] == club) & ((df[col_final_result] == 'home') | (df[col_final_result] == 'draw'))]
    n_pts_home = (points_home[col_final_result] == 'home').sum() * 3 + (points_home[col_final_result] == 'draw').sum()
    
    points_away = df[(df[col_away_team] == club) & ((df[col_final_result] == 'away') | (df[col_final_result] == 'draw'))]
    n_pts_away = (points_away[col_final_result] == 'away').sum() * 3 + (points_away[col_final_result] == 'draw').sum()
    
    n_pts = n_pts_home + n_pts_away
    
    return n_pts








class Preprocessing:
    """
    Class which manages the preprocessing of a cleaned dataframe

    NB: a cleaned dataframe is a dataframe whose columns are the following:
        - date of the match
        - season of the match (e.g. if a match was played on September 2012, season = '2012/2013')
        - home team
        - away team
        - number of goals scored by the home team
        - number of goals scored by the away team
        - final result (categorical variable with mentionned if home team won, away team won or draw)
        - betting odds for home team win
        - betting odds for away team win
        - betting odds for draw

    The preprocessing follows the steps detailed below:
    - creation of an aggregated variable with betting odds: one column for an aggregated betting odd variable for home tema victory, one column for away team victory, one column for draw
    - .......
    TODO FOR THE WHOLE DOCUMENTATION
    """

    def __init__(self, df, config):
        """
        Args:
            - df: cleaned dataframe respecting the previous conditions
            - config: dictionnary with the information specified in the config file
        """
        self.df = df

        # Columns identification
        self.date_column = config['date_column']
        self.season_column = config['season_column']
        self.home_column = config['home_column']
        self.away_column = config['away_column']
        self.nb_goals_home_column = config['nb_goals_home_column']
        self.nb_goals_away_column = config['nb_goals_away_column']
        self.final_result_column = config['final_result_column']

        # Other columns are betting odds columns
        columns_to_exclude = set([self.date_column, self.season_column, self.home_column, self.away_column, self.nb_goals_home_column, self.nb_goals_away_column, self.final_result_column])
        self.odds_columns = [c for c in self.df.columns if c not in columns_to_exclude]
        
        # Number of odds columns: multiple of 3 (one odd for home team, one odd for away team, one for draw)
        if len(self.odds_columns) % 3 != 0:
            raise ValueError(f"There must be a multiple of 3 odd columns, there are currently {len(self.odds_columns)} columns")

        # Home, away, draw odd columns
        self.home_odds_columns = [c for c in self.odds_columns if c.upper().endswith('H')]
        self.away_odds_columns = [c for c in self.odds_columns if c.upper().endswith('A')]
        self.draw_odds_columns = [c for c in self.odds_columns if c.upper().endswith('D')]

        # home, away and draw odds columns must have same length
        if not (len(self.home_odds_columns) == len(self.away_odds_columns) == len(self.draw_odds_columns)):
            raise ValueError(f"There must be the same number of home, away and draw odds columns. There are currently {len(self.home_odds_columns)} home odds columns, {len(self.away_odds_columns)} away odds columns and {len(self.draw_odds_columns)} draw odds columns")

    
    def creation_betting_odd_variable(self,
                                      home_odd_var_name: str='home_odd',
                                      away_odd_var_name: str='away_odd',
                                      draw_odd_var_name: str='draw_odd') -> pd.DataFrame:
        """
        Creates a betting odd variable by averaging all the betting odds given by the columns in input
        A new variable is created per possible issue (one for the home team victory, one for the away team victory, one for the draw)

        Args:
            home_odd_var_name: name of the created variable with the odd of the home team victory
            away_odd_var_name: name of the created variable with the odd of the away team victory
            draw_odd_var_name: name of the created variable with the odd of the draw

        Returns:
            The dataframe without the odds columns but with three new variables (one per issue) which are the average of the different odds
        """

        df_odd = self.df.copy()

        avg_home_odd = df_odd[self.home_odds_columns].mean(axis = 1)
        avg_away_odd = df_odd[self.away_odds_columns].mean(axis = 1)
        avg_draw_odd = df_odd[self.draw_odds_columns].mean(axis = 1)

        # Creation of the new variables
        df_odd[home_odd_var_name] = avg_home_odd
        df_odd[away_odd_var_name] = avg_away_odd
        df_odd[draw_odd_var_name] = avg_draw_odd

        # Removing of the odd columns
        df_odd.drop(columns=self.odds_columns, inplace=True)

        return df_odd




