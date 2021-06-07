import logging

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

logger = logging.getLogger(__name__)


def evaluate_model(df, model, features=None):

    logger.info("Started evaluating the model")

    if features is None:
        features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
                                  'loudness', 'speechiness', 'tempo', 'valence']

    inertia = model.inertia_
    silhouette = silhouette_score(df[features], model.labels_)

    logger.info('inertia: %f' % inertia)
    logger.info('silhouette: %f' % silhouette)

    metrics = {'inertia': inertia, 'silhouette score': silhouette}

    logger.info("Finished evaluating the model")

    return metrics

def build_model(df, features=None, numClusters = 8, seed = 10):

    logger.info("Started building the model")

    if features is None:
        features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
                                  'loudness', 'speechiness', 'tempo', 'valence']

    model = KMeans(n_clusters=numClusters, random_state=seed).fit(df[features])
    logger.info("Finished developping the model")

    return model


def model(df, config):

    final_model = build_model(df, **config['build_model'])

    metrics = evaluate_model(df, final_model, **config['evaluate_model'])

    return final_model, metrics