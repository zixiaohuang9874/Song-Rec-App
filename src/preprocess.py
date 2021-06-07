import logging

import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def clean(df, columns_to_clean=None):
    """Clean the specified column in the dataset. In this case, the artists column is being cleaned to remove
    the beginning [' and ending ']

    Args:
        df (pandas dataframe): dataframe to be cleaned
        columns_to_clean (list): columns of the dataframe to be cleaned

    Return:
        df (pandas dataframe): dataframe after cleaning

    """

    if columns_to_clean is None:
        columns_to_clean = ['artists']

    for c in columns_to_clean:
        df[c] = df[c].str.slice(2)
        df[c] = df[c].str[:-2]

    logger.info("Finished cleaning the data")

    return df


def standardize(df, columns_to_standardize=None):
    """Standardize the specified column in the dataset.

    Args:
        df (pandas dataframe): dataframe to be standardized
        columns_to_standardize (list): columns of the dataframe to be standardized

    Return:
        df(pandas dataframe): dataframe after standardizing

    """

    if columns_to_standardize is None:
        columns_to_standardize = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
                                  'loudness', 'speechiness', 'tempo', 'valence']

    scaler = StandardScaler()
    df[columns_to_standardize] = pd.DataFrame(scaler.fit_transform(df[columns_to_standardize]))

    logger.info("Finished standardizing the data")

    return df


def preprocess(df, config):
    """Call clean() and standardize() to preprocess the data

    Args:
        df (pandas dataframe): dataframe to be preprocessed
        config: configuration of the functions in this .py file

    Return:
        df (pandas dataframe): dataframe after preprocessing

    """

    if 'clean' in config:
        df = clean(df, **config['clean'])

    if 'standardize' in config:
        df = standardize(df, **config['standardize'])

    logger.info("Finished preprocessing the data")

    return df