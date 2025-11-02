import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif, mutual_info_classif


def find_highly_correlated_cols(df, cols=None, threshold=0.95):
    """
    Args:
        df: dataframe to analyze
        cols: optional list of numeric columns to consider. By default, all numeric columns are considered
        threshold: absolute correlation threshold above which redundancy is assumed

    Returns:
        The list of columns to drop according to correlation rules
    """
    if cols is None:
        numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    else:
        numeric = cols

    if len(numeric) <= 1:
        return []

    corr = df[numeric].corr().abs()

    # We keep unique correlation pairs (strictly upper diagonale of the correlation matrix) 
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))

    # Pairs with corr > threshold
    to_drop = set()
    mean_abs_corr = corr.mean().sort_values(ascending=False)

    # iterates on pairs
    for col in upper.columns:
        high_corr_with = upper.index[upper[col] > threshold].tolist()
        for other in high_corr_with:
            if other in to_drop or col in to_drop:
                continue
            # column to drop = column with correlation mean higher
            if mean_abs_corr.loc[col] >= mean_abs_corr.loc[other]:
                to_drop.add(col)
            else:
                to_drop.add(other)

    return list(to_drop)


def remove_low_variance_features(df: pd.DataFrame, threshold: float=0.05) -> pd.DataFrame:
    """
    Returns features with low variance, less than threshold providen in input
    """
    numeric_df = df.select_dtypes(include=["number"])
    selector = VarianceThreshold(threshold)
    selector.fit(numeric_df)

    kept = numeric_df.columns[selector.get_support()]
    dropped = list(set(numeric_df.columns) - set(kept))

    return dropped


def select_top_features(X, y, k=20, method="anova"):
    """
    Returns top features according to the method providen in input
    """
    X = X.select_dtypes(include=["number"])
    if method == "anova":
        selector = SelectKBest(f_classif, k=k)
    else:
        selector = SelectKBest(mutual_info_classif, k=k)

    X_new = selector.fit_transform(X, y)
    kept = X.columns[selector.get_support()]
    return kept