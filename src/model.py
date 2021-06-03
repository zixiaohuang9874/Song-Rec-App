import logging

import pandas as pd
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)

def model(df, features=None, numClusters = 8, seed = 10):
    if features is None:
        features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
                                  'loudness', 'speechiness', 'tempo', 'valence']

    model = KMeans(n_clusters=numClusters, random_state=seed).fit(df[features])
    logger.info("Finished developping the model")

    return model