import pandas as pd
import numpy as np
import joblib
import os
import sys

root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
root_path = os.path.abspath(os.path.join(root_path, ".."))
sys.path.append(root_path)

from src.modeling import load_model 


def build_preprocessed_input_row(preprocessed_df, home_team, away_team, season, odd_home, odd_draw, odd_away, config):
    """
    Builds input row ready for prediction
    WIP: absolute and relative recent and historical indicators
    """

    df = preprocessed_df.copy()

    def get_points(row, team):
        if row[config['final_result_column']] == "draw":
            return 1
        if row[config['home_column']] == team and row[config['final_result_column']] == "home":
            return 3
        if row[config['away_column']] == team and row[config['final_result_column']] == "away":
            return 3
        return 0

    # Final input row initialization
    input_row = {
        # --- BASIC ---
        config['season_column']: season,
        config['home_column']: home_team,
        config['away_column']: away_team,

        # --- ODDS ---
        config['odd_home_column']: odd_home,
        config['odd_draw_column']: odd_draw,
        config['odd_away_column']: odd_away,

        # ===================================================================
        #                          HOME TEAM FEATURES
        # ===================================================================

        # Current season basic
        config['nb_points_home_team']: -1,
        config['general_ranking_home_team']: -1,
        config['nb_goals_scored_home_team']: -1,
        config['nb_goals_conceded_home_team']: -1,
        config['goal_difference_home_team']: -1,

        # Current season home-only indicators
        config['nb_points_home_team_at_home']: -1,
        config['nb_goals_scored_home_team_at_home']: -1,
        config['nb_goals_conceded_home_team_at_home']: -1,
        config['home_team_ranking_at_home']: -1,

        # Attack / defense ranking
        config['attack_ranking_home_team']: -1,
        config['defense_ranking_home_team']: -1,

        # --- Absolute recent form ---
        config['abs_recent_nb_points_by_match_home_team']: -1,
        config['abs_recent_nb_goals_scored_by_match_home_team']: -1,
        config['abs_recent_nb_goals_conceded_by_match_home_team']: -1,
        config['abs_recent_goal_difference_home_team']: -1,
        config['abs_recent_ranking_home_team']: -1,
        
        # --- Absolute historical form ---
        config['abs_hist_nb_points_by_season_home_team']: -1,
        config['abs_hist_nb_goals_scored_by_season_home_team']: -1,
        config['abs_hist_nb_goals_conceded_by_season_home_team']: -1,
        config['abs_hist_ranking_by_season_home_team']: -1,
        config['hist_nb_seasons_l1_home_team']: -1,

        # --- Relative recent form ---
        config['rel_recent_nb_points_by_match_home_team']: -1,
        config['rel_recent_nb_goals_scored_by_match_home_team']: -1,
        config['rel_recent_nb_goals_conceded_by_match_home_team']: -1,
        config['rel_recent_goal_difference_home_team']: -1,
        config['rel_percentage_victory_home_team']: -1,

        # --- Strict relative recent form ---
        config['strict_rel_recent_nb_points_by_match_home_team']: -1,
        config['strict_rel_recent_nb_goals_scored_by_match_home_team']: -1,
        config['strict_rel_recent_nb_goals_conceded_by_match_home_team']: -1,
        config['strict_rel_recent_goal_difference_home_team']: -1,
        config['strict_rel_percentage_victory_home_team']: -1,

        # --- External ---
        config['promoted_home_team']: -1,

        # ===================================================================
        #                          AWAY TEAM FEATURES
        # ===================================================================
    
        # Current season basic
        config['nb_points_away_team']: -1,
        config['general_ranking_away_team']: -1,
        config['nb_goals_scored_away_team']: -1,
        config['nb_goals_conceded_away_team']: -1,
        config['goal_difference_away_team']: -1,
    
        # Current season away-only indicators
        config['nb_points_away_team_away']: -1,
        config['nb_goals_scored_away_team_away']: -1,
        config['nb_goals_conceded_away_team_away']: -1,
        config['away_team_ranking_away']: -1,
    
        # Attack / defense rankings
        config['attack_ranking_away_team']: -1,
        config['defense_ranking_away_team']: -1,
    
        # --- Absolute recent form ---
        config['abs_recent_nb_points_by_match_away_team']: -1,
        config['abs_recent_nb_goals_scored_by_match_away_team']: -1,
        config['abs_recent_nb_goals_conceded_by_match_away_team']: -1,
        config['abs_recent_goal_difference_away_team']: -1,
        config['abs_recent_ranking_away_team']: -1,
    
        # --- Absolute historical form ---
        config['abs_hist_nb_points_by_season_away_team']: -1,
        config['abs_hist_nb_goals_scored_by_season_away_team']: -1,
        config['abs_hist_nb_goals_conceded_by_season_away_team']: -1,
        config['abs_hist_ranking_by_season_away_team']: -1,
        config['hist_nb_seasons_l1_away_team']: -1,
    
        # --- Relative recent form ---
        config['rel_recent_nb_points_by_match_away_team']: -1,
        config['rel_recent_nb_goals_scored_by_match_away_team']: -1,
        config['rel_recent_nb_goals_conceded_by_match_away_team']: -1,
        config['rel_recent_goal_difference_away_team']: -1,
        config['rel_percentage_victory_away_team']: -1,
    
        # --- Strict relative recent form ---
        config['strict_rel_recent_nb_points_by_match_away_team']: -1,
        config['strict_rel_recent_nb_goals_scored_by_match_away_team']: -1,
        config['strict_rel_recent_nb_goals_conceded_by_match_away_team']: -1,
        config['strict_rel_recent_goal_difference_away_team']: -1,
        config['strict_rel_percentage_victory_away_team']: -1,
    
        # --- External ---
        config['promoted_away_team']: -1,
    }

    # =========================================================================
    #                              UPDATE HOME TEAM
    # =========================================================================
    
    # ---------------------------
    # Current season indicators
    # ---------------------------
    season_df = df[df[config['season_column']] == season].copy()
    
    home_season_df = season_df[
        (season_df[config['home_column']] == home_team) |
        (season_df[config['away_column']] == home_team)
    ]

    # If no match yet in this season → keep -1 for all
    if len(home_season_df) > 0:
    
        # -------------------------
        # Current season points
        # -------------------------
        home_points = home_season_df.apply(
            lambda row: get_points(row, home_team), axis=1
        ).sum()
        input_row[config['nb_points_home_team']] = int(home_points)
    
        # -------------------------
        # Goals scored / conceded
        # -------------------------
        goals_scored = (
            home_season_df.apply(
                lambda r: r[config['nb_goals_home_column']]
                if r[config['home_column']] == home_team
                else r[config['nb_goals_away_column']],
                axis=1
            )
        ).sum()
    
        goals_conceded = (
            home_season_df.apply(
                lambda r: r[config['nb_goals_away_column']]
                if r[config['home_column']] == home_team
                else r[config['nb_goals_home_column']],
                axis=1
            )
        ).sum()
    
        input_row[config['nb_goals_scored_home_team']] = int(goals_scored)
        input_row[config['nb_goals_conceded_home_team']] = int(goals_conceded)
        input_row[config['goal_difference_home_team']] = int(goals_scored - goals_conceded)
    
        # -------------------------
        # Ranking in season
        # -------------------------
        ranking_table = (
            season_df.copy()
            .assign(home_points=lambda x: x.apply(lambda r: get_points(r, r[config['home_column']]), axis=1))
            .assign(away_points=lambda x: x.apply(lambda r: get_points(r, r[config['away_column']]), axis=1))
        )
    
        # Compute points per club
        pts_per_club = (
            pd.concat([
                ranking_table.groupby(config['home_column'])['home_points'].sum(),
                ranking_table.groupby(config['away_column'])['away_points'].sum()
            ], axis=1).sum(axis=1)
        )
        pts_per_club
    
        # Order & get rank
        general_rank = pts_per_club.sort_values(ascending=False)
        rank_home = general_rank.index.tolist().index(home_team) + 1
        input_row[config['general_ranking_home_team']] = int(rank_home)
    
        # -------------------------
        # Attack ranking
        # -------------------------
        goals_scored_clubs = (
            season_df.groupby(config['home_column'])[config['nb_goals_home_column']].sum() +
            season_df.groupby(config['away_column'])[config['nb_goals_away_column']].sum()
        )
        attack_rank = goals_scored_clubs.sort_values(ascending=False)
        input_row[config['attack_ranking_home_team']] = attack_rank.index.tolist().index(home_team) + 1
    
        # -------------------------
        # Defense ranking
        # -------------------------
        goals_conceded_clubs = (
            season_df.groupby(config['home_column'])[config['nb_goals_away_column']].sum() +
            season_df.groupby(config['away_column'])[config['nb_goals_home_column']].sum()
        )
        defense_rank = goals_conceded_clubs.sort_values()
        input_row[config['defense_ranking_home_team']] = defense_rank.index.tolist().index(home_team) + 1
    
        # -------------------------
        # At-home only indicators
        # -------------------------
        home_home_df = season_df[season_df[config['home_column']] == home_team]
        home_home_df['home_points'] = home_home_df.apply(lambda row: get_points(row, row[config['home_column']]), axis=1)
        home_home_df['away_points'] = home_home_df.apply(lambda row: get_points(row, row[config['away_column']]), axis=1)
        
        input_row[config['nb_points_home_team_at_home']] = int(home_home_df['home_points'].sum())
        input_row[config['nb_goals_scored_home_team_at_home']] = int(home_home_df[config['nb_goals_home_column']].sum())
        input_row[config['nb_goals_conceded_home_team_at_home']] = int(home_home_df[config['nb_goals_away_column']].sum())
    
        # Ranking at home
        pts_at_home = ranking_table.groupby(config['home_column'])['home_points'].sum()
        rank_home_home = pts_at_home.sort_values(ascending=False).index.tolist().index(home_team) + 1
        input_row[config['home_team_ranking_at_home']] = int(rank_home_home)

        # -----------------------------------
        # Nb seasons in L1 and promoted team
        # -----------------------------------
        df_home = df[(df[config['home_column']] == home_team) |
                             (df[config['away_column']] == home_team)].sort_values(by=config['date_column'])
        seasons_list = list(df_home[config['season_column']].unique())
    
        if season in seasons_list:
            input_row[config['hist_nb_seasons_l1_home_team']] = len(seasons_list)
        else:
            input_row[config['hist_nb_seasons_l1_home_team']] = len(seasons_list) + 1

        first_years_seasons = [int(s.rsplit('/')[0]) for s in seasons_list]
        first_year_current_season = int(season.rsplit('/')[0])
        if first_year_current_season - 1 not in first_years_seasons:
            input_row[config['promoted_home_team']] = 1
        else:
            input_row[config['promoted_home_team']] = 0


    # =========================================================================
    #                              UPDATE AWAY TEAM
    # =========================================================================
    
    # ---------------------------
    # Current season indicators
    # ---------------------------
    season_df = df[df[config['season_column']] == season].copy()
    
    away_season_df = season_df[
        (season_df[config['home_column']] == away_team) |
        (season_df[config['away_column']] == away_team)
    ]

    # If no match yet in this season → keep -1 for all
    if len(away_season_df) > 0:
    
        # -------------------------
        # Current season points
        # -------------------------
        away_points = away_season_df.apply(
            lambda row: get_points(row, away_team), axis=1
        ).sum()
        input_row[config['nb_points_away_team']] = int(away_points)
    
        # -------------------------
        # Goals scored / conceded
        # -------------------------
        goals_scored = (
            away_season_df.apply(
                lambda r: r[config['nb_goals_away_column']]
                if r[config['away_column']] == away_team
                else r[config['nb_goals_home_column']],
                axis=1
            )
        ).sum()
    
        goals_conceded = (
            away_season_df.apply(
                lambda r: r[config['nb_goals_home_column']]
                if r[config['away_column']] == away_team
                else r[config['nb_goals_away_column']],
                axis=1
            )
        ).sum()
    
        input_row[config['nb_goals_scored_away_team']] = int(goals_scored)
        input_row[config['nb_goals_conceded_away_team']] = int(goals_conceded)
        input_row[config['goal_difference_away_team']] = int(goals_scored - goals_conceded)
    
        # -------------------------
        # Ranking in season
        # -------------------------
        ranking_table = (
            season_df.copy()
            .assign(home_points=lambda x: x.apply(lambda r: get_points(r, r[config['home_column']]), axis=1))
            .assign(away_points=lambda x: x.apply(lambda r: get_points(r, r[config['away_column']]), axis=1))
        )
    
        # Compute points per club
        pts_per_club = (
            pd.concat([
                ranking_table.groupby(config['home_column'])['home_points'].sum(),
                ranking_table.groupby(config['away_column'])['away_points'].sum(),
            ], axis=1).sum(axis=1)
        )
    
        # Order & get rank
        general_rank = pts_per_club.sort_values(ascending=False)
        rank_away = general_rank.index.tolist().index(away_team) + 1
        input_row[config['general_ranking_away_team']] = int(rank_away)
    
        # -------------------------
        # Attack ranking
        # -------------------------
        goals_scored_clubs = (
            season_df.groupby(config['home_column'])[config['nb_goals_home_column']].sum() +
            season_df.groupby(config['away_column'])[config['nb_goals_away_column']].sum()
        )
        attack_rank = goals_scored_clubs.sort_values(ascending=False)
        input_row[config['attack_ranking_away_team']] = attack_rank.index.tolist().index(away_team) + 1
    
        # -------------------------
        # Defense ranking
        # -------------------------
        goals_conceded_clubs = (
            season_df.groupby(config['home_column'])[config['nb_goals_away_column']].sum() +
            season_df.groupby(config['away_column'])[config['nb_goals_home_column']].sum()
        )
        defense_rank = goals_conceded_clubs.sort_values()
        input_row[config['defense_ranking_away_team']] = defense_rank.index.tolist().index(away_team) + 1
    
        # -------------------------
        # At-home only indicators
        # -------------------------
        away_away_df = season_df[season_df[config['away_column']] == away_team]
        away_away_df['home_points'] = away_away_df.apply(lambda row: get_points(row, row[config['home_column']]), axis=1)
        away_away_df['away_points'] = away_away_df.apply(lambda row: get_points(row, row[config['away_column']]), axis=1)
        
        input_row[config['nb_points_away_team_away']] = int(away_away_df['away_points'].sum())
        input_row[config['nb_goals_scored_away_team_away']] = int(away_away_df[config['nb_goals_away_column']].sum())
        input_row[config['nb_goals_conceded_away_team_away']] = int(away_away_df[config['nb_goals_home_column']].sum())
    
        # Ranking at home
        pts_at_home = ranking_table.groupby(config['away_column'])['away_points'].sum()
        rank_away_away = pts_at_home.sort_values(ascending=False).index.tolist().index(away_team) + 1
        input_row[config['away_team_ranking_away']] = int(rank_away_away)


        # -----------------------------------
        # Nb seasons in L1 and promoted team
        # -----------------------------------
        df_away = df[(df[config['home_column']] == away_team) |
                             (df[config['away_column']] == away_team)].sort_values(by=config['date_column'])
        seasons_list = list(df_away[config['season_column']].unique())
    
        if season in seasons_list:
            input_row[config['hist_nb_seasons_l1_away_team']] = len(seasons_list)
        else:
            input_row[config['hist_nb_seasons_l1_away_team']] = len(seasons_list) + 1

        first_years_seasons = [int(s.rsplit('/')[0]) for s in seasons_list]
        first_year_current_season = int(season.rsplit('/')[0])
        if first_year_current_season - 1 not in first_years_seasons:
            input_row[config['promoted_away_team']] = 1
        else:
            input_row[config['promoted_away_team']] = 0

    return input_row


def predict_match(home_team, away_team, primary_model, secondary_model, config):
    """
    Predicts the final result and the score of the match knowing the involved teams and the chosen models
    """
    # Model loading
    if primary_model == 'LogisticRegression':
        primary = load_model(os.path.join('..', config['primary_models_dir'], 'logistic.joblib'))

    if primary_model == 'RandomForest':
        primary = load_model(os.path.join('..', config['primary_models_dir'], 'rf.joblib'))
        
    if primary_model == 'XGBoost':
        primary = load_model(os.path.join('..', config['primary_models_dir'], 'xgb.joblib'))
        
    if secondary_model == 'Poisson':
        home_secondary = load_model(os.path.join('..', config['secondary_models_dir'], 'home_poisson.joblib'))
        away_secondary = load_model(os.path.join('..', config['secondary_models_dir'], 'away_poisson.joblib'))
        
    if secondary_model == 'RandomForest':
        home_secondary = load_model(os.path.join('..', config['secondary_models_dir'], 'home_rf.joblib'))
        away_secondary = load_model(os.path.join('..', config['secondary_models_dir'], 'away_rf.joblib'))
        
    if secondary_model == 'XGBoost':
        home_secondary = load_model(os.path.join('..', config['secondary_models_dir'], 'home_xgb.joblib'))
        away_secondary = load_model(os.path.join('..', config['secondary_models_dir'], 'away_xgb.joblib'))

    









