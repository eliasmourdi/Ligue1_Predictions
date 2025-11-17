import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedKFold, GridSearchCV, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import make_scorer, f1_score, accuracy_score, log_loss
import optuna
from optuna.samplers import TPESampler


# Utilities
def _make_cv(n_splits=5, random_state=42):
    return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)


def _save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"Model saved to {path}")


# GridSearch implementations
def run_grid_search(X, y, param_grid, preprocessing_pipeline, cv=None, n_jobs=-1, verbose=2):
    """Grid Search according to a param grid and a preprocessing pipeline."""
    if cv is None:
        cv = _make_cv()

    new_grid = {}
    for key, value in param_grid.items():
        if not key.startswith('clf'):
            new_grid[f"clf__{key}"] = value
        else:
            new_grid[key] = value

    gs = GridSearchCV(preprocessing_pipeline, new_grid, scoring='f1_macro', cv=cv, n_jobs=n_jobs, verbose=verbose)
    gs.fit(X, y)
    print("Best logistic params:", gs.best_params_, "best f1_macro:", gs.best_score_)
    return gs    


def run_primary_modeling(X, y, param_grid_lr, param_grid_rf, param_grid_xgb, preprocessing_pipeline_lr, preprocessing_pipeline_rf, preprocessing_pipeline_xgb, outdir, cv_splits=5, n_jobs=-1):
    cv = _make_cv(n_splits=cv_splits)
    results = {}
    # Logistic regression
    results['logistic'] = run_grid_search(X, y, param_grid_lr, preprocessing_pipeline_lr, cv=cv, n_jobs=n_jobs)
    _save_model(results['logistic'].best_estimator_, os.path.join('..', outdir, 'logistic.joblib'))

    # Random forest
    results['rf'] = run_grid_search(X, y, param_grid_rf, preprocessing_pipeline_rf, cv=cv, n_jobs=n_jobs)
    _save_model(results['rf'].best_estimator_, os.path.join('..', outdir, 'rf.joblib'))

    # XGBoost
    results['xgb'] = run_grid_search(X, y, param_grid_xgb, preprocessing_pipeline_xgb, cv=cv, n_jobs=n_jobs)
    _save_model(results['xgb'].best_estimator_, os.path.join('..', outdir, 'xgb.joblib'))

    return results


def run_secondary_modeling(X_home, y_home, X_away, y_away, param_grid_poisson, param_grid_rf, param_grid_xgb, preprocessing_pipeline_poisson, preprocessing_pipeline_rf, preprocessing_pipeline_xgb, outdir, cv_splits=5, n_jobs=-1):
    cv = _make_cv(n_splits=cv_splits)
    results = {}
    # Poisson regression
    # Home
    results['home_poisson'] = run_grid_search(X_home, y_home, param_grid_poisson, preprocessing_pipeline_poisson, cv=cv, n_jobs=n_jobs)
    _save_model(results['home_poisson'].best_estimator_, os.path.join('..', outdir, 'home_poisson.joblib'))

    # Away
    results['away_poisson'] = run_grid_search(X_home, y_home, param_grid_poisson, preprocessing_pipeline_poisson, cv=cv, n_jobs=n_jobs)
    _save_model(results['away_poisson'].best_estimator_, os.path.join('..', outdir, 'away_poisson.joblib'))
    
    # Random forest
    # Home
    results['home_rf'] = run_grid_search(X_home, y_home, param_grid_rf, preprocessing_pipeline_rf, cv=cv, n_jobs=n_jobs)
    _save_model(results['home_rf'].best_estimator_, os.path.join('..', outdir, 'home_rf.joblib'))

    # Away
    results['away_rf'] = run_grid_search(X_away, y_away, param_grid_rf, preprocessing_pipeline_rf, cv=cv, n_jobs=n_jobs)
    _save_model(results['away_rf'].best_estimator_, os.path.join('..', outdir, 'away_rf.joblib'))
    
    # XGBoost
    # Home
    results['home_xgb'] = run_grid_search(X_home, y_home, param_grid_xgb, preprocessing_pipeline_xgb, cv=cv, n_jobs=n_jobs)
    _save_model(results['home_xgb'].best_estimator_, os.path.join('..', outdir, 'home_xgb.joblib'))

    # Away
    results['away_xgb'] = run_grid_search(X_away, y_away, param_grid_xgb, preprocessing_pipeline_xgb, cv=cv, n_jobs=n_jobs)
    _save_model(results['away_xgb'].best_estimator_, os.path.join('..', outdir, 'away_xgb.joblib'))
    
    return results


def load_model(path):
    """
    Loads a joblib file
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")
    model = joblib.load(path)
    print(f"Model loaded from {path}")
    return model


def evaluate_model_metrics(model, X_test, y_test, plot_confusion=False):
    """
    Evaluates a model and returns main classification metrics
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_macro": f1_score(y_test, y_pred, average='macro'),
        "precision_macro": precision_score(y_test, y_pred, average='macro'),
        "recall_macro": recall_score(y_test, y_pred, average='macro')
    }
    
    print("Evaluation metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")
    
    if plot_confusion:
        cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
        plt.figure(figsize=(6,5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
        plt.xlabel("Predicted")
        plt.ylabel("True")
        plt.title("Confusion Matrix")
        plt.show()
    
    return metrics