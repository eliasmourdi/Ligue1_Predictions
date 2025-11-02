import pandas as pd
import numpy as np
import re


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