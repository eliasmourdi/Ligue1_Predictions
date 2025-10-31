import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class ClubAnalysis:
    """
    This class allows to run a data analysis pipeline which focuses on one specific club, providen as input of the class
    """
    def __init__(self, df, club_name, config):
        self.df = df
        self.club = club_name
        self.config = config

        if (self.club not in self.df[self.config['home_column']]) or (self.club not in self.df[self.config['away_column']]):
            raise AttributeError(f"{self.club} not in the providen dataframe")

        if ('home_points' not in self.df.columns) and ('away_points' not in self.df.columns):
            self.df['home_points'] = self.df[config['final_result_column']].map({'home': 3, 'draw': 1, 'away': 0})
            self.df['away_points'] = self.df[config['final_result_column']].map({'home': 0, 'draw': 1, 'away': 3})
            
        self.all_seasons = sorted(df[self.config['season_column']].unique())
        self.club_matches = df[(df[self.config['home_column']] == club_name) | (df[self.config['away_column']] == club_name)].copy()
        self._prepare_points()
        self._prepare_ranks()
        self._prepare_goals()
    

    def _prepare_points(self):
        points_home = self.club_matches[self.club_matches[self.config['home_column']]==self.club].groupby(self.config['season_column'])['home_points'].sum()
        points_away = self.club_matches[self.club_matches[self.config['away_column']]==self.club].groupby(self.config['season_column'])['away_points'].sum()
        self.points_per_season = points_home.add(points_away, fill_value=0).reindex(self.all_seasons, fill_value=0)
        
    
    def _prepare_ranks(self):
        home_points_season = self.df.groupby([self.config['season_column'],self.config['home_column']])['home_points'].sum().reset_index().rename(columns={self.config['home_column']:'club','home_points':'points_home'})
        away_points_season = self.df.groupby([self.config['season_column'],self.config['away_column']])['away_points'].sum().reset_index().rename(columns={self.config['away_column']:'club','away_points':'points_away'})
        season_points = pd.merge(home_points_season, away_points_season, on=[self.config['season_column'],'club'])
        season_points['total_points'] = season_points['points_home'] + season_points['points_away']
        season_points['rank'] = season_points.groupby(self.config['season_column'])['total_points'].rank(method='min', ascending=False)
        self.rank_per_season = season_points[season_points['club']==self.club].set_index(self.config['season_column'])['rank'].reindex(self.all_seasons, fill_value=None)

        
    def _prepare_goals(self):
        scored_home = self.club_matches[self.club_matches[self.config['home_column']]==self.club].groupby(self.config['season_column'])[self.config['nb_goals_home_column']].sum()
        scored_away = self.club_matches[self.club_matches[self.config['away_column']]==self.club].groupby(self.config['season_column'])[self.config['nb_goals_away_column']].sum()
        self.goals_scored = scored_home.add(scored_away, fill_value=0).reindex(self.all_seasons, fill_value=0)
        
        conceded_home = self.club_matches[self.club_matches[self.config['home_column']]==self.club].groupby(self.config['season_column'])[self.config['nb_goals_away_column']].sum()
        conceded_away = self.club_matches[self.club_matches[self.config['away_column']]==self.club].groupby(self.config['season_column'])[self.config['nb_goals_home_column']].sum()
        self.goals_conceded = conceded_home.add(conceded_away, fill_value=0).reindex(self.all_seasons, fill_value=0)
    

    def plot_points_per_season(self):
        plt.figure(figsize=(12,5))
        sns.barplot(x=self.points_per_season.index, y=self.points_per_season.values, color="blue")
        plt.title(f"Number of points evolution per season - {self.club}")
        plt.xlabel("Season")
        plt.ylabel("Points")
        plt.xticks(rotation=45)
        plt.show()

    
    def plot_rank_per_season(self):
        plt.figure(figsize=(12,5))
        sns.barplot(x=self.rank_per_season.index, y=self.rank_per_season.values, color="red")
        plt.title(f"Ranking evolution per season - {self.club}")
        plt.xlabel("Season")
        plt.ylabel("Ranking")
        plt.xticks(rotation=45)
        plt.gca().invert_yaxis()
        plt.show()

    
    def plot_goals_scored_per_season(self):
        plt.figure(figsize=(12,5))
        sns.barplot(x=self.goals_scored.index, y=self.goals_scored.values, color="green")
        plt.title(f"Number of goals scored evolution per season - {self.club}")
        plt.xlabel("Season")
        plt.ylabel("Goals scored")
        plt.xticks(rotation=45)
        plt.show()

    
    def plot_goals_conceded_per_season(self):
        plt.figure(figsize=(12,5))
        sns.barplot(x=self.goals_conceded.index, y=self.goals_conceded.values, color="red")
        plt.title(f"Goals conceded evolution per season - {self.club}")
        plt.xlabel("Season")
        plt.ylabel("Goals conceded")
        plt.xticks(rotation=45)
        plt.show()


    def plot_best_opponents(self, min_matches=5):
        home_against = self.df[self.df[self.config['away_column']] == self.club].groupby(self.config['home_column'])['home_points'].mean()
        home_counts = self.df[self.df[self.config['away_column']] == self.club].groupby(self.config['home_column'])['home_points'].count()
        home_against = home_against[home_counts >= min_matches]
    
        away_against = self.df[self.df[self.config['home_column']] == self.club].groupby(self.config['away_column'])['away_points'].mean()
        away_counts = self.df[self.df[self.config['home_column']] == self.club].groupby(self.config['away_column'])['away_points'].count()
        away_against = away_against[away_counts >= min_matches]

        plt.figure(figsize=(10,5))
        home_against.sort_values(ascending=False).plot(kind='bar', color='green')
        plt.title(f"Clubs performing well against {self.club} at home (min {min_matches} matches)")
        plt.ylabel("Average points")
        plt.show()

        plt.figure(figsize=(10,5))
        away_against.sort_values(ascending=False).plot(kind='bar', color='blue')
        plt.title(f"Clubs performing well against {self.club} away (min {min_matches} matches)")
        plt.ylabel("Average points")
        plt.show()


    def plot_worst_opponents(self, min_matches=5):
        home_against = self.df[self.df[self.config['away_column']] == self.club].groupby(self.config['home_column'])['home_points'].mean()
        home_counts = self.df[self.df[self.config['away_column']] == self.club].groupby(self.config['home_column'])['home_points'].count()
        home_against = home_against[home_counts >= min_matches]
    
        away_against = self.df[self.df[self.config['home_column']] == self.club].groupby(self.config['away_column'])['away_points'].mean()
        away_counts = self.df[self.df[self.config['home_column']] == self.club].groupby(self.config['away_column'])['away_points'].count()
        away_against = away_against[away_counts >= min_matches]

        plt.figure(figsize=(10,5))
        home_against.sort_values().plot(kind='bar', color='red')
        plt.title(f"Clubs struggling against {self.club} at home (min {min_matches} matches)")
        plt.ylabel("Average points")
        plt.show()

        plt.figure(figsize=(10,5))
        away_against.sort_values().plot(kind='bar', color='orange')
        plt.title(f"Clubs struggling against {self.club} away (min {min_matches} matches)")
        plt.ylabel("Average points")
        plt.show()

    
    def plot_all(self):
        self.plot_points_per_season()
        self.plot_rank_per_season()
        self.plot_goals_scored_per_season()
        self.plot_goals_conceded_per_season()
        self.plot_best_opponents()
        self.plot_worst_opponents()