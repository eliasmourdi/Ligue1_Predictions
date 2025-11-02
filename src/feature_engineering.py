import pandas as pd
import numpy as np
import re
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif, mutual_info_classif


def create_diff_features(df: pd.DataFrame, patterns: list[tuple[str, str]], drop_original: bool=True) -> pd.DataFrame:
    """
    Creates columns with the difference of same columns which highlight the same indicator for home and away teams. Columns are paired according to a specific pattern providen in input
    Ex: nb_goals_home and nb_goals_away -> one column diff_nb_goals
    Function used for the primary model, whose goal is to predict the final issue of a match

    Args:
        df: preprocessed dataframe with home and away columns
        patterns: [(home_pattern, away_pattern),...] used to identity columns to pair 
        drop_original: if True, deletes initial columns after computation of new columns

    Returns:
        pd.DataFrame: enriched dataframe with new columns
    """
    df_diff = df.copy()
    created = []
    paired_cols = set()

    for home_suffix, away_suffix in patterns:
        home_cols = [c for c in df.columns if c.endswith(home_suffix)]

        for home_col in home_cols:
            # Odds columns can be ignored
            if "odd" in home_col.lower():
                continue

            away_col = home_col.replace(home_suffix, away_suffix)
            if away_col in df.columns:
                base_name = home_col.replace(home_suffix, "")
                new_col = f"diff_{base_name}"
                df_diff[new_col] = df[home_col] - df[away_col]
                created.append(new_col)
                paired_cols.update([home_col, away_col])

    # Check if some columns have not been paired
    all_home_like = [c for c in df.columns if any(s in c for s, _ in patterns)]
    all_away_like = [c for c in df.columns if any(e in c for _, e in patterns)]
    unpaired = set(all_home_like + all_away_like) - paired_cols

    # Ignore odds
    unpaired = {u for u in unpaired if "odd" not in u.lower()}

    if len(unpaired) > 0:
        raise ValueError(f"These columns have not been paired: {sorted(unpaired)}")

    if drop_original:
        df_diff = df_diff.drop(columns=list(paired_cols), errors="ignore")

    return df_diff


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

    if len(dropped) > 0:
        print(f"{len(dropped)} removed features since they have low variance: {dropped}")
    else:
        print("No columns removed")

    return dropped


def select_top_features(X, y, k=20, method="anova"):
    """
    Returns top features according to the method providen in input
    """
    if method == "anova":
        selector = SelectKBest(f_classif, k=k)
    else:
        selector = SelectKBest(mutual_info_classif, k=k)

    X_new = selector.fit_transform(X, y)
    kept = X.columns[selector.get_support()]
    return kept