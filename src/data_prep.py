import pandas as pd
import os
from typing import Sequence, Mapping, Tuple
from datetime import datetime


def import_raw_aggregated_dataset(first_year: int,
                                  last_year: int,
                                  raw_data_file: str) -> pd.DataFrame:
    """
    Allows to save an aggregated dataset with all the Ligue 1 matchs from a season to another season
    All the files have a name like 'ligue1_firstYear_lastYear'
    
    Args:
        first_year: first year of the first season we want to save (e.g. 2012 for 2012/2013)
        last_year: last year of the last season we want to save (e.g. 2015 for 2014/2015)
        raw_data_file: folder with all the raw data to aggregate

    Returns:
        A Pandas dataframe with all the matchs from the first season to the last season
    """

    df_list = []

    for year in range(first_year, last_year):
        filename = f'ligue1_{year}_{year + 1}.csv'
        filepath = os.path.join('../' + raw_data_file, filename)

        if not os.path.exists(filepath):
            print(f"File not found: {filepath} (ignored)")
            continue

        data = pd.read_csv(filepath)
        data.dropna(how = 'all', inplace = True)
        df_list.append(data)

    if not df_list:
        raise ValueError("No data has been loaded")

    df = pd.concat(df_list, ignore_index=True)
    return df


def dataframe_cleaning(df: pd.DataFrame,
                       cols_to_delete: Sequence[str] | None,
                       cols_to_rename: Mapping[str, str] | None,
                       values_to_rename: Mapping[str, Tuple[str, str]] | None) -> pd.DataFrame:
    """
    Cleans a dataframe by dropping columns, renaming columns, and renaming values in specific columns

    Args:
        df: dataframe to clean
        cols_to_delete: list of columns to delete from the dataframe
        cols_to_rename: keys are old column names, values are new column names
        values_to_rename: keys are column names, values are tuples of (old_value, new_value) to replace in that column

    Returns:
        A dataframe cleaned according to these 3 rules
    """

    df_cleaned = df.copy()
    
    # Columns removing
    if cols_to_delete:
        df_cleaned.drop(columns=cols_to_delete, inplace=True)

    # Columns renaming
    if cols_to_rename:
        df_cleaned.rename(columns=cols_to_rename, inplace=True)

    # Values replacement in specific columns
    if values_to_rename:
        for col, (old_val, new_val) in values_to_rename.items():
            if col in df_cleaned.columns:
                df_cleaned[col] = df_cleaned[col].replace(old_val, new_val)

    return df_cleaned


def convert_dates_column(df: pd.DataFrame,
                         date_column: str) -> pd.DataFrame:
    """
    Converts a date column in a dataframe to datetime objects, handling multiple formats

    This function attempts to parse each value in the specified column using two common date formats:
    - '%d/%m/%y' (e.g., 12/08/23)
    - '%d/%m/%Y' (e.g., 12/08/2023)

    Args:
        df: The input dataframe containing a column with date strings
        date_column: Name of the column to convert

    Returns:
        The dataframe with the date column converted to datetime objects.
    """

    def parse_date(value: str):
        for fmt in ("%d/%m/%y", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt)
            except (ValueError, TypeError):
                continue
        raise ValueError(f"Unrecognized date format: {value}")

    df = df.copy()
    df[date_column] = df[date_column].apply(parse_date)

    return df