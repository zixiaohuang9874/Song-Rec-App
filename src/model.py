import logging

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

logger = logging.getLogger(__name__)


def evaluate_model(df, model):
    """Evaluate the performance of the model

    Args:
        df (pandas dataframe): dataframe used in building the model and evaluating the model
        model (sklearn.cluster._kmeans.KMeans): model to be evaluated

    Returns:
        metrics (dict): dictionary to store the result (inertia and silhouette score)

    """

    logger.info("Started evaluating the model")

    # Calculate the inertia and silhouette score
    inertia = model.inertia_
    silhouette = silhouette_score(df, model.labels_)

    logger.info('inertia: %f' % inertia)
    logger.info('silhouette: %f' % silhouette)

    # Put the inertia and silhouette score into a dictionary
    metrics = {'inertia': inertia, 'silhouette score': silhouette}

    logger.info("Finished evaluating the model")

    return metrics


def build_model(df, numClusters=8, seed=10):
    """Build the K-Means clustering model

    Args:
        df (pandas dataframe): dataframe to be used to build the model
        numClusters (int): number of clusters in the KMeans model
        seed (int): random state number to ensure the reproducibility

    Return:
        model: K-Means clustering model
        metrics (dict): dictionary to store the result (inertia and silhouette score)

    """

    logger.info("Started building the model")

    model = KMeans(n_clusters=numClusters, random_state=seed).fit(df)
    logger.info("Finished developping the model")

    return model


def model(df, config, features=None):
    """Main function to build and evaluate the model

    Args:
        df (pandas dataframe): dataframe to be used to build and evaluate the model
        config: configuration for the function
        features (list): features to be extracted from the dataframe in order to build the model

    Returns:
        model (sklearn.cluster._kmeans.KMeans): K-Means clustering model
        metrics: (dict): dictionary to store the result (inertia and silhouette score)

    """

    if features is None:
        features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
                'loudness', 'speechiness', 'tempo', 'valence']

    df_new = df[features]

    if 'build_model' in config:
        final_model = build_model(df_new, **config['build_model'])
    else:
        final_model = build_model(df_new)

    metrics = evaluate_model(df_new, final_model)

    return final_model, metrics