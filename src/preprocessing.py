import pandas as pd
from utils import nb_points, goals_scored, goals_conceded, goal_diff, ranking_table, ranking_club
        

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
        self.config = config

        # Check columns
        required_cols = [config['date_column'], config['season_column'], config['home_column'], config['away_column'], config['nb_goals_home_column'], config['nb_goals_away_column'], config['final_result_column']]
        missing = [c for c in required_cols if c not in self.df.columns]
        if missing:
            raise ValueError(f"Following columns are missing: {missing}")

        # Other columns are betting odds columns
        columns_to_exclude = required_cols.copy()
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


    def _nb_points(self, df, club):
        return nb_points(df, club, self.config['home_column'], self.config['away_column'], self.config['final_result_column'])

    
    def _goals_scored(self, df, club):
        return goals_scored(df, club, self.config['home_column'], self.config['away_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _goals_conceded(self, df, club):    
        returns goals_conceded(df, club, self.config['home_column'], self.config['away_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _goal_diff(self, df, club):
        return goal_diff(df, club, self.config['home_column'], self.config['away_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _ranking_table(self, df, club):
        return ranking_table(df, club, self.config['home_column'], self.config['away_column'], self.config['final_result_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _ranking_club(self, df, club):
        return ranking_club(df, club, self.config['home_column'], self.config['away_column'], self.config['final_result_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])
        
    
    def creation_betting_odd_variable(self) -> pd.DataFrame:
        """
        Creates a betting odd variable by averaging all the betting odds given by the columns in input
        A new variable is created per possible issue (one for the home team victory, one for the away team victory, one for the draw)

        Returns:
            The dataframe without the odds columns but with three new variables (one per issue) which are the average of the different odds
        """
        df_odd = self.df.copy()

        avg_home_odd = df_odd[self.home_odds_columns].mean(axis = 1)
        avg_away_odd = df_odd[self.away_odds_columns].mean(axis = 1)
        avg_draw_odd = df_odd[self.draw_odds_columns].mean(axis = 1)

        # Creation of the new variables
        df_odd[self.config['odd_home_column']] = avg_home_odd
        df_odd[self.config['odd_away_column']] = avg_away_odd
        df_odd[self.config['odd_draw_column']] = avg_draw_odd

        # Removing of the odd columns
        df_odd.drop(columns=self.odds_columns, inplace=True)

        return df_odd


    def computes_current_season_indicators(self):
        """
        Current season: only matches played during a same Ligue 1 season (season column, '2012/2013' for example)
        
        Current season indicators computed by this method are the following:
        - number of points so far
        - general ranking so far
        - number of goals scored so far
        - number of goals conceded so far
        - goal difference so far
        ...
        """
        df = self.df.copy()
        df = df.sort_values(by=self.config['date_column']).reset_index(drop=True)

        indicators = [self.config['nb_points_home_column'],
                      self.config['nb_points_away_column'],
                      self.config['general_ranking_home_column'],
                      self.config['general_ranking_away_column'],
                      self.config['nb_goals_scored_home_column'],
                      self.config['nb_goals_scored_away_column'],
                      self.config['nb_goals_conceded_home_column'],
                      self.config['nb_goals_conceded_away_column'],
                      self.config['goal_difference_home_column'],
                      self.config['goal_difference_away_column'],
                      self.config['attack_ranking_home_column'],
                      self.config['attack_ranking_away_column'],
                      self.config['defense_ranking_home_column'],
                      self.config['defense_ranking_away_column'],
                      self.config['nb_points_home_matches_column'],
                      self.config['nb_points_away_matches_column'],
                      self.config['home_ranking_column'],
                      self.config['away_ranking_column'],
                      self.config['nb_goals_scored_at_home_column'],
                      self.config['nb_goals_scored_away_column'],
                      self.config['nb_goals_conceded_at_home_column'],
                      self.config['nb_goals_conceded_away_column']]

        for col in indicators:
            df[col] = None # initialization

        # Season loop
        for season, season_df in df.groupby(self.season_column, sort=False):
            
            for i, row in season_df.iterrows():
                past_matches = season_df.loc[season_df[self.config['date_column']] < row[self.config['date_column']]]

                # Clubs involving in the match
                home, away = row[self.config['home_column']], row[self.config['away_column']]
                
                # Points, goals, goal difference
                home_points = self._nb_points(past_matches, home)
                away_points = self._nb_points(past_matches, away)

                home_goals_for = self._goals_scored(past_matches, home)
                away_goals_for = self._goals_scored(past_matches, away)

                home_goals_against = self._goals_conceded(past_matches, home)
                away_goals_against = self._goals_conceded(past_matches, away)

                home_diff = self._goal_diff(past_matches, home)
                away_diff = self._goal_diff(past_matches, away)
            
                # Rankings
                table = self._ranking_table(past_matches)
                home_rank = self._ranking_club(past_matches, home)
                away_rank = self._ranking_club(past_matches, away)

                # Attribution
                df.at[i, self.config['nb_points_home_column']] = home_points
                df.at[i, self.config['nb_points_away_column']] = away_points
                df.at[i, self.config['general_ranking_home_column']] = home_rank
                df.at[i, self.config['general_ranking_away_column']] = away_rank
                df.at[i, self.config['nb_goals_scored_home_column']] = home_goals_for
                df.at[i, self.config['nb_goals_scored_away_column']] = away_goals_for
                df.at[i, self.config['nb_goals_conceded_home_column']] = home_goals_against
                df.at[i, self.config['nb_goals_conceded_away_column']] = away_goals_against
                df.at[i, self.config['goal_difference_home_column']] = home_diff
                df.at[i, self.config['goal_difference_away_column']] = away_diff

        return df


        

        
        

        




