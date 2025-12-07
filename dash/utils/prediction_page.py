import pandas as pd
import numpy as np
import joblib

root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
root_path = os.path.abspath(os.path.join(root_path, ".."))
sys.path.append(root_path)

from src.modeling import load_model 


def predict_match(home_team, away_team, primary_model, secondary_model, config):
    """
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









