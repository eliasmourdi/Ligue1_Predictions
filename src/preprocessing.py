import pandas as pd
from src.utils import nb_points, goals_scored, goals_conceded, goal_diff, ranking_table, ranking_club, attack_ranking_table, attack_ranking_club, defense_ranking_table, defense_ranking_club, home_ranking_table, home_ranking_club, away_ranking_table, away_ranking_club
        

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
        return goals_conceded(df, club, self.config['home_column'], self.config['away_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _goal_diff(self, df, club):
        return goal_diff(df, club, self.config['home_column'], self.config['away_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _ranking_table(self, df, club):
        return ranking_table(df, club, self.config['home_column'], self.config['away_column'], self.config['final_result_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _ranking_club(self, df, club):
        return ranking_club(df, club, self.config['home_column'], self.config['away_column'], self.config['final_result_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _attack_ranking_table(self, df, club):
        return attack_ranking_table(df, club, self.config['home_column'], self.config['away_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _attack_ranking_club(self, df, club):
        return attack_ranking_club(df, club, self.config['home_column'], self.config['away_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _defense_ranking_table(self, df, club):
        return defense_ranking_table(df, club, self.config['home_column'], self.config['away_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _defense_ranking_club(self, df, club):
        return defense_ranking_club(df, club, self.config['home_column'], self.config['away_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _home_ranking_table(self, df, club):
        return home_ranking_table(df, club, self.config['home_column'], self.config['away_column'], self.config['final_result_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _home_ranking_club(self, df, club):
        return home_ranking_club(df, club, self.config['home_column'], self.config['away_column'], self.config['final_result_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _away_ranking_table(self, df, club):
        return away_ranking_table(df, club, self.config['home_column'], self.config['away_column'], self.config['final_result_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])


    def _away_ranking_club(self, df, club):
        return away_ranking_club(df, club, self.config['home_column'], self.config['away_column'], self.config['final_result_column'], self.config['nb_goals_home_column'], self.config['nb_goals_away_column'])
        
    
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
        - attack ranking so far
        - defense ranking so far
        - number of goals conceded so far
        - goal difference so far
        - number of points taken at home by home team so far, number of points taken away by away team so far
        - home ranking for home team so far, away ranking for away team so far
        - number of goals scored at home by home team so far, number of goals scored away by away team so far
        - number of goals conceded at home by home team so far, number of goals conceded away by away team so far
        """
        df = self.df.copy()
        df = df.sort_values(by=self.config['date_column']).reset_index(drop=True)

        # Initialization
        indicators = [self.config['nb_points_home_team'],
                      self.config['nb_points_away_team'],
                      self.config['general_ranking_home_team'],
                      self.config['general_ranking_away_team'],
                      self.config['nb_goals_scored_home_team'],
                      self.config['nb_goals_scored_away_team'],
                      self.config['nb_goals_conceded_home_team'],
                      self.config['nb_goals_conceded_away_team'],
                      self.config['goal_difference_home_team'],
                      self.config['goal_difference_away_team'],
                      self.config['attack_ranking_home_team'],
                      self.config['attack_ranking_away_team'],
                      self.config['defense_ranking_home_team'],
                      self.config['defense_ranking_away_team'],
                      self.config['nb_points_home_team_at_home'],
                      self.config['nb_points_away_team_away'],
                      self.config['home_team_ranking_at_home'],
                      self.config['away_team_ranking_away'],
                      self.config['nb_goals_scored_home_team_at_home'],
                      self.config['nb_goals_scored_away_team_away'],
                      self.config['nb_goals_conceded_home_team_at_home'],
                      self.config['nb_goals_conceded_away_team_away']]
        
        for col in indicators:
            df[col] = None

        # Season loop
        for season, season_df in df.groupby(self.config['season_column'], sort=False):
            
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
                home_rank = self._ranking_club(past_matches, home)
                away_rank = self._ranking_club(past_matches, away)

                home_rank_at_home = self._home_ranking_club(past_matches, home)
                away_rank_away = self._away_ranking_club(past_matches, away)

                home_attack_rank = self._attack_ranking_club(past_matches, home)
                home_defense_rank = self._defense_ranking_club(past_matches, home)

                away_attack_rank = self._attack_ranking_club(past_matches, away)
                away_defense_rank = self._defense_ranking_club(past_matches, away)


                # Home / Away specific indicators
                past_matches_home = past_matches[past_matches[self.config['home_column']] == home]
                past_matches_away = past_matches[past_matches[self.config['away_column']] == away]

                home_points_at_home = self._nb_points(past_matches_home, home)
                away_points_away = self._nb_points(past_matches_away, away)

                home_goals_at_home = self._goals_scored(past_matches_home, home)
                away_goals_away = self._goals_scored(past_matches_away, away)
                
                home_goals_conceded_at_home = self._goals_conceded(past_matches_home, home)
                away_goals_conceded_away = self._goals_conceded(past_matches_away, away)
                
                # Assignment
                df.at[i, self.config['nb_points_home_team']] = home_points
                df.at[i, self.config['nb_points_away_team']] = away_points
                df.at[i, self.config['general_ranking_home_team']] = home_rank
                df.at[i, self.config['general_ranking_away_team']] = away_rank
                df.at[i, self.config['nb_goals_scored_home_team']] = home_goals_for
                df.at[i, self.config['nb_goals_scored_away_team']] = away_goals_for
                df.at[i, self.config['nb_goals_conceded_home_team']] = home_goals_against
                df.at[i, self.config['nb_goals_conceded_away_team']] = away_goals_against
                df.at[i, self.config['goal_difference_home_team']] = home_diff
                df.at[i, self.config['goal_difference_away_team']] = away_diff
                df.at[i, self.config['attack_ranking_home_team']] = home_attack_rank
                df.at[i, self.config['attack_ranking_away_team']] = away_attack_rank
                df.at[i, self.config['defense_ranking_home_team']] = home_defense_rank
                df.at[i, self.config['defense_ranking_away_team']] = away_defense_rank
                df.at[i, self.config['nb_points_home_team_at_home']] = home_points_at_home
                df.at[i, self.config['nb_points_away_team_away']] = away_points_away
                df.at[i, self.config['home_team_ranking_at_home']] = home_rank_at_home
                df.at[i, self.config['away_team_ranking_away']] = away_rank_away
                df.at[i, self.config['nb_goals_scored_home_team_at_home']] = home_goals_at_home
                df.at[i, self.config['nb_goals_scored_away_team_away']] = away_goals_away
                df.at[i, self.config['nb_goals_conceded_home_team_at_home']] = home_goals_conceded_at_home
                df.at[i, self.config['nb_goals_conceded_away_team_away']] = away_goals_conceded_away
        
        return df

    
    def computes_absolute_recent_form_indicators(self, max_matches: int=None):
        """
        Absolute: regardless of the teams played against 
        Recent form: last matches on a same season
        Absolute recent form indicators are therefore indicators related to the max_matches last matches
            
        Absolute recent form indicators computed by this method are the following:
        - points averaged by match
        - goals scored averaged by match
        - goals conceded averaged by match
        - goal difference on last matches
        - ranking based on last matches
        """
        df = self.df.copy()
        df = df.sort_values(by=self.config['date_column']).reset_index(drop=True)

        if max_matches is None:
            max_matches = self.config['abs_max_matches']

        # Initialization
        indicators = [self.config['abs_recent_nb_points_by_match_home_team'],
                      self.config['abs_recent_nb_points_by_match_away_team'],
                      self.config['abs_recent_nb_goals_scored_by_match_home_team'],
                      self.config['abs_recent_nb_goals_scored_by_match_away_team'],
                      self.config['abs_recent_nb_goals_conceded_by_match_home_team'],
                      self.config['abs_recent_nb_goals_conceded_by_match_away_team'],
                      self.config['abs_recent_goal_difference_home_team'],
                      self.config['abs_recent_goal_difference_away_team'],
                      self.config['abs_recent_ranking_home_team'],
                      self.config['abs_recent_ranking_away_team']]

        for col in indicators:
            df[col] = None

        # Season loop
        for season, season_df in df.groupby(self.config['season_column'], sort=False):
            
            for i, row in season_df.iterrows():
                current_date = row[self.config['date_column']]
                home_team = row[self.config['home_column']]
                away_team = row[self.config['away_column']]
                
                # Filtrating on the last matches of home and away teams
                past_home_matches = season_df[(season_df[self.config['date_column']] < current_date) &
                                              ((season_df[self.config['home_column']] == home_team) | (season_df[self.config['away_column']] == home_team))]
                past_home_matches = past_home_matches.tail(max_matches)
                
                past_away_matches = season_df[(season_df[self.config['date_column']] < current_date) &
                                              ((season_df[self.config['home_column']] == away_team) | (season_df[self.config['away_column']] == away_team))]
                past_away_matches = past_away_matches.tail(max_matches)
                
                # Number of points
                avg_home_points = self._nb_points(past_home_matches, home_team) / len(past_home_matches) if len(past_home_matches) != 0 else -1
                avg_away_points = self._nb_points(past_away_matches, away_team) / len(past_away_matches) if len(past_away_matches) != 0 else -1
                
                # Number of goals scored
                avg_home_goals_scored = self._goals_scored(past_home_matches, home_team) / len(past_home_matches) if len(past_home_matches) != 0 else -1
                avg_away_goals_scored = self._goals_scored(past_away_matches, away_team) / len(past_away_matches) if len(past_away_matches) != 0 else -1

                # Number of goals conceded
                avg_home_goals_conceded = self._goals_conceded(past_home_matches, home_team) / len(past_home_matches) if len(past_home_matches) != 0 else -1
                avg_away_goals_conceded = self._goals_conceded(past_away_matches, away_team) / len(past_away_matches) if len(past_away_matches) != 0 else -1
                
                # Goal difference
                home_goal_diff = self._goal_diff(past_home_matches, home_team)
                away_goal_diff = self._goal_diff(past_away_matches, away_team)
                
                # Ranking
                teams = pd.concat([season_df[self.config['home_column']], season_df[self.config['away_column']]]).unique()
                ranking_table_df = pd.DataFrame({
                    'team': teams,
                    'points': [self._nb_points(season_df[(season_df[self.config['date_column']] < current_date) &
                                                         ((season_df[self.config['home_column']] == t) | (season_df[self.config['away_column']] == t))].tail(max_matches), t) for t in teams],
                    'goal_diff': [self._goal_diff(season_df[(season_df[self.config['date_column']] < current_date) &
                                                            ((season_df[self.config['home_column']] == t) | (season_df[self.config['away_column']] == t))].tail(max_matches), t) for t in teams]
                })
                ranking_table_df = ranking_table_df.sort_values(by=['points', 'goal_diff'], ascending=False).reset_index(drop=True)

                home_rank = ranking_table_df[ranking_table_df['team'] == home_team].index[0] + 1
                away_rank = ranking_table_df[ranking_table_df['team'] == away_team].index[0] + 1
                
                # Assignment
                df.at[i, self.config['abs_recent_nb_points_by_match_home_team']] = avg_home_points
                df.at[i, self.config['abs_recent_nb_points_by_match_away_team']] = avg_away_points
                df.at[i, self.config['abs_recent_nb_goals_scored_by_match_home_team']] = avg_home_goals_scored
                df.at[i, self.config['abs_recent_nb_goals_scored_by_match_away_team']] = avg_away_goals_scored
                df.at[i, self.config['abs_recent_nb_goals_conceded_by_match_home_team']] = avg_home_goals_conceded
                df.at[i, self.config['abs_recent_nb_goals_conceded_by_match_away_team']] = avg_away_goals_conceded
                df.at[i, self.config['abs_recent_goal_difference_home_team']] = home_goal_diff
                df.at[i, self.config['abs_recent_goal_difference_away_team']] = away_goal_diff
                df.at[i, self.config['abs_recent_ranking_home_team']] = home_rank
                df.at[i, self.config['abs_recent_ranking_away_team']] = away_rank

        return df


    def computes_absolute_historical_form_indicators(self):
        """
        Absolute: regardless of the teams played against 
        Historical form: all previous seasons
        Absolute historical form indicators are therefore indicators related to the previous seasons
            
        Absolute historical form indicators computed by this method are the following:
        - points averaged by season
        - goals scored averaged by season
        - goals conceded averaged by season
        - ranking averaged by season
        """
        df = self.df.copy()
        df = df.sort_values(by=self.config['date_column']).reset_index(drop=True)
        
        # Initialization
        indicators = [self.config['abs_hist_nb_points_by_season_home_team'],
                      self.config['abs_hist_nb_points_by_season_away_team'],
                      self.config['abs_hist_nb_goals_scored_by_season_home_team'],
                      self.config['abs_hist_nb_goals_scored_by_season_away_team'],
                      self.config['abs_hist_nb_goals_conceded_by_season_home_team'],
                      self.config['abs_hist_nb_goals_conceded_by_season_away_team'],
                      self.config['abs_hist_ranking_by_season_home_team'],
                      self.config['abs_hist_ranking_by_season_away_team']]

        for col in indicators:
            df[col] = None

        # Season loop
        for i, row in df.iterrows():
            current_season = row[self.config['season_column']]
            current_date = row[self.config['date_column']]
            home_team = row[self.config['home_column']]
            away_team = row[self.config['away_column']]

            # All previous seasons
            past_seasons = df[(df[self.config['date_column']] < current_date) & (df[self.config['season_column']] != current_season)]

            if past_seasons.empty:
                df.at[i, self.config['abs_hist_nb_points_by_season_home_team']] = -1
                df.at[i, self.config['abs_hist_nb_points_by_season_away_team']] = -1
                df.at[i, self.config['abs_hist_nb_goals_scored_by_season_home_team']] = -1
                df.at[i, self.config['abs_hist_nb_goals_scored_by_season_away_team']] = -1
                df.at[i, self.config['abs_hist_nb_goals_conceded_by_season_home_team']] = -1
                df.at[i, self.config['abs_hist_nb_goals_conceded_by_season_away_team']] = -1
                df.at[i, self.config['abs_hist_ranking_by_season_home_team']] = -1
                df.at[i, self.config['abs_hist_ranking_by_season_away_team']] = -1
                continue

            # Indicators computation
            home_points_avg = past_seasons.groupby(self.config['season_column']).apply(lambda x: self._nb_points(x, home_team)).mean()
            away_points_avg = past_seasons.groupby(self.config['season_column']).apply(lambda x: self._nb_points(x, away_team)).mean()

            home_goals_avg = past_seasons.groupby(self.config['season_column']).apply(lambda x: self._goals_scored(x, home_team)).mean()
            away_goals_avg = past_seasons.groupby(self.config['season_column']).apply(lambda x: self._goals_scored(x, away_team)).mean()

            home_conceded_avg = past_seasons.groupby(self.config['season_column']).apply(lambda x: self._goals_conceded(x, home_team)).mean()
            away_conceded_avg = past_seasons.groupby(self.config['season_column']).apply(lambda x: self._goals_conceded(x, away_team)).mean()

            home_rank_avg = past_seasons.groupby(self.config['season_column']).apply(lambda x: self._ranking_club(x, home_team)).mean()
            away_rank_avg = past_seasons.groupby(self.config['season_column']).apply(lambda x: self._ranking_club(x, away_team)).mean()

            # Assignment
            df.at[i, self.config['abs_hist_nb_points_by_season_home_team']] = home_points_avg
            df.at[i, self.config['abs_hist_nb_points_by_season_away_team']] = away_points_avg
            df.at[i, self.config['abs_hist_nb_goals_scored_by_season_home_team']] = home_goals_avg
            df.at[i, self.config['abs_hist_nb_goals_scored_by_season_away_team']] = away_goals_avg
            df.at[i, self.config['abs_hist_nb_goals_conceded_by_season_home_team']] = home_conceded_avg
            df.at[i, self.config['abs_hist_nb_goals_conceded_by_season_away_team']] = away_conceded_avg
            df.at[i, self.config['abs_hist_ranking_by_season_home_team']] = home_rank_avg
            df.at[i, self.config['abs_hist_ranking_by_season_away_team']] = away_rank_avg
            
        return df


    def computes_relative_recent_form_indicators(self, max_matches: int=None):
        """
        Relative: matches with teams playing each other
        Recent form: last matches on a same season
        Relative recent form indicators are therefore indicators related to the max_matches last matches confronting the two same teams
            
        Relative recent form indicators computed by this method are the following:
        - points averaged by match
        - goals scored averaged by match
        - goals conceded averaged by match
        - goal difference on last matches
        - % of win
        """
        df = self.df.copy()
        df = df.sort_values(by=self.config['date_column']).reset_index(drop=True)

        if max_matches is None:
            max_matches = self.config['rel_max_matches']

        # Initialization
        indicators = [self.config['rel_recent_nb_points_by_match_home_team'],
                      self.config['rel_recent_nb_points_by_match_away_team'],
                      self.config['rel_recent_nb_goals_scored_by_match_home_team'],
                      self.config['rel_recent_nb_goals_scored_by_match_away_team'],
                      self.config['rel_recent_nb_goals_conceded_by_match_home_team'],
                      self.config['rel_recent_nb_goals_conceded_by_match_away_team'],
                      self.config['rel_recent_goal_difference_home_team'],
                      self.config['rel_recent_goal_difference_away_team'],
                      self.config['rel_percentage_victory_home_team'],
                      self.config['rel_percentage_victory_away_team']]

        for col in indicators:
            df[col] = -1.0

    
        # Creation of a pair key column for each teams pair in chronological order (home away order not important here)
        df['pair_key'] = df.apply(lambda x: tuple(sorted([x[self.config['home_column']], x[self.config['away_column']]])), axis=1)
        grouped = df.groupby('pair_key', group_keys=False)

        # Indicators computation
        results = []

        for pair, sub in grouped:
            sub = sub.sort_values(by=self.config['date_column']).reset_index()
            n = len(sub)
            if n == 0:
                continue

            for i in range(n):
                prev = sub.iloc[max(0, i - max_matches):i] # last matches between the two teams
                if prev.empty:
                    continue

                row = sub.loc[i]
                home = row[self.config['home_column']]
                away = row[self.config['away_column']]
                n_matches = len(prev)

                # Number of points by match
                home_pts_by_match = self._nb_points(prev, home) / n_matches if n_matches > 0 else - 1
                away_pts_by_match = self._nb_points(prev, away) / n_matches if n_matches > 0 else -1

                # Goals scored
                home_goals_scored_by_match = self._goals_scored(prev, home) / n_matches if n_matches > 0 else -1
                away_goals_scored_by_match = self._goals_scored(prev, away) / n_matches if n_matches > 0 else -1

                # Goals conceded
                home_goals_conceded_by_match = self._goals_conceded(prev, home) / n_matches if n_matches > 0 else -1
                away_goals_conceded_by_match = self._goals_conceded(prev, away) / n_matches if n_matches > 0 else -1

                # Goal difference
                home_goal_diff = self._goal_diff(prev, home)
                away_goal_diff = self._goal_diff(prev, away)

                # Win percentage
                home_perc_wins = len(prev[
                                     ((prev[self.config['home_column']] == home) & (prev[self.config['final_result_column']] == 'home')) |
                                     ((prev[self.config['away_column']] == home) & (prev[self.config['final_result_column']] == 'away'))
                                     ]) / n_matches if n_matches > 0 else -1
                away_perc_wins = len(prev[
                                     ((prev[self.config['home_column']] == away) & (prev[self.config['final_result_column']] == 'home')) |
                                     ((prev[self.config['away_column']] == away) & (prev[self.config['final_result_column']] == 'away'))
                                     ]) / n_matches if n_matches > 0 else -1

                # Assignment
                results.append((
                    row['index'],
                    home_pts_by_match,
                    away_pts_by_match,
                    home_goals_scored_by_match,
                    away_goals_scored_by_match,
                    home_goals_conceded_by_match,
                    away_goals_conceded_by_match,
                    home_goal_diff,
                    away_goal_diff,
                    100 * home_perc_wins,
                    100 * away_perc_wins
                ))

        # df update
        if results:
            res_df = pd.DataFrame(results, columns=['index']+indicators).set_index('index')
            df.update(res_df)

        # Deleting the temporary pair key
        df.drop(columns=['pair_key'], inplace=True)

        return df


    def computes_strict_relative_recent_form_indicators(self, max_matches: int=None):
        """
        Strict: order home / away taken into consideration (e.g. TeamA vs TeamB different than TeamB vs TeamA)
        Relative: matches with teams playing each other
        Recent form: last matches on a same season
        Relative recent form indicators are therefore indicators related to the max_matches last matches confronting the two same teams in the home away order
            
        Relative recent form indicators computed by this method are the following:
        - points averaged by match
        - goals scored averaged by match
        - goals conceded averaged by match
        - goal difference on last matches
        - % of win
        """
        df = self.df.copy()
        df = df.sort_values(by=self.config['date_column']).reset_index(drop=True)

        if max_matches is None:
            max_matches = self.config['strict_rel_max_matches']

        # Initialization
        indicators = [self.config['strict_rel_recent_nb_points_by_match_home_team'],
                      self.config['strict_rel_recent_nb_points_by_match_away_team'],
                      self.config['strict_rel_recent_nb_goals_scored_by_match_home_team'],
                      self.config['strict_rel_recent_nb_goals_scored_by_match_away_team'],
                      self.config['strict_rel_recent_nb_goals_conceded_by_match_home_team'],
                      self.config['strict_rel_recent_nb_goals_conceded_by_match_away_team'],
                      self.config['strict_rel_recent_goal_difference_home_team'],
                      self.config['strict_rel_recent_goal_difference_away_team'],
                      self.config['strict_rel_percentage_victory_home_team'],
                      self.config['strict_rel_percentage_victory_away_team']]

        for col in indicators:
            df[col] = -1.0

    
        # Creation of a pair key column for each teams pair in chronological order (home away order important here)
        df['pair_key'] = df.apply(lambda x: (x[self.config['home_column']], x[self.config['away_column']]), axis=1)
        grouped = df.groupby('pair_key', group_keys=False)

        # Indicators computation
        results = []

        for pair, sub in grouped:
            sub = sub.sort_values(by=self.config['date_column']).reset_index()
            n = len(sub)
            if n == 0:
                continue

            for i in range(n):
                prev = sub.iloc[max(0, i - max_matches):i] # last matches between the two teams
                if prev.empty:
                    continue

                row = sub.loc[i]
                home = row[self.config['home_column']]
                away = row[self.config['away_column']]
                n_matches = len(prev)

                # Number of points by match
                home_pts_by_match = self._nb_points(prev, home) / n_matches if n_matches > 0 else - 1
                away_pts_by_match = self._nb_points(prev, away) / n_matches if n_matches > 0 else -1

                # Goals scored
                home_goals_scored_by_match = self._goals_scored(prev, home) / n_matches if n_matches > 0 else -1
                away_goals_scored_by_match = self._goals_scored(prev, away) / n_matches if n_matches > 0 else -1

                # Goals conceded
                home_goals_conceded_by_match = self._goals_conceded(prev, home) / n_matches if n_matches > 0 else -1
                away_goals_conceded_by_match = self._goals_conceded(prev, away) / n_matches if n_matches > 0 else -1

                # Goal difference
                home_goal_diff = self._goal_diff(prev, home)
                away_goal_diff = self._goal_diff(prev, away)

                # Win percentage
                home_perc_wins = len(prev[
                                     ((prev[self.config['home_column']] == home) & (prev[self.config['final_result_column']] == 'home')) |
                                     ((prev[self.config['away_column']] == home) & (prev[self.config['final_result_column']] == 'away'))
                                     ]) / n_matches if n_matches > 0 else -1
                away_perc_wins = len(prev[
                                     ((prev[self.config['home_column']] == away) & (prev[self.config['final_result_column']] == 'home')) |
                                     ((prev[self.config['away_column']] == away) & (prev[self.config['final_result_column']] == 'away'))
                                     ]) / n_matches if n_matches > 0 else -1

                # Assignment
                results.append((
                    row['index'],
                    home_pts_by_match,
                    away_pts_by_match,
                    home_goals_scored_by_match,
                    away_goals_scored_by_match,
                    home_goals_conceded_by_match,
                    away_goals_conceded_by_match,
                    home_goal_diff,
                    away_goal_diff,
                    100 * home_perc_wins,
                    100 * away_perc_wins
                ))

        # df update
        if results:
            res_df = pd.DataFrame(results, columns=['index']+indicators).set_index('index')
            df.update(res_df)

        # Deleting the temporary pair key
        df.drop(columns=['pair_key'], inplace=True)

        return df
        

        
        

        




