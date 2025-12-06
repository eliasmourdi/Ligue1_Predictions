import pandas as pd


def load_data(TRAIN_PATH, TEST_PATH, DATE_COL):
    """
    Load and merge the train/test preprocessed datasets
    """
    train = pd.read_csv(TRAIN_PATH, parse_dates=[DATE_COL])
    test = pd.read_csv(TEST_PATH, parse_dates=[DATE_COL])
    df = pd.concat([train, test], ignore_index=True)
    return df.sort_values(DATE_COL)