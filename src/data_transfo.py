import pandas as pd
from typing import Sequence


def creation_betting_odd_variable(df: pd.DataFrame,
                                  cols_home_odds: Sequence[str],
                                  cols_away_odds: Sequence[str],
                                  cols_draw_odds: Sequence[str],
                                  home_odd_var_name: str = 'home_odd',
                                  away_odd_var_name: str = 'away_odd',
                                  draw_odd_var_name: str = 'draw_odd') -> pd.DataFrame:
    """
    Creates a betting odd variable by averaging all the betting odds given by the columns in input
    A new variable is created per possible issue (one for the home team victory, one for the away team victory, one for the draw)

    Args:
        df: dataframe to transform
        cols_home_odds: list of columns giving the odds of the home team victory
        cols_away_odds: list of columns giving the odds of the away team victory
        cols_draw_odds: list of columns giving the odds of the draw
        home_odd_var_name: name of the created variable with the odd of the home team victory
        away_odd_var_name: name of the created variable with the odd of the away team victory
        draw_odd_var_name: name of the created variable with the odd of the draw
        

    Returns:
        The dataframe without the odds columns but with three new variables (one per issue) which are the average of the different odds
    """

    df_odd = df.copy()

    avg_home_odd = df_odd[cols_home_odds].mean(axis = 1)
    avg_away_odd = df_odd[cols_away_odds].mean(axis = 1)
    avg_draw_odd = df_odd[cols_draw_odds].mean(axis = 1)

    # Creation of the new variables
    df_odd[home_odd_var_name] = avg_home_odd
    df_odd[away_odd_var_name] = avg_away_odd
    df_odd[draw_odd_var_name] = avg_draw_odd

    # Removing of the odd columns
    df_odd.drop(columns = cols_home_odds + cols_away_odds + cols_draw_odds, inplace = True)

    return df_odd