import logging

import numpy as np
import pandas as pd

from sklearn.metrics import pairwise_distances

logger = logging.getLogger(__name__)

def find_closet(df, k):
    """This function finds the 10 closet points to the song in the cluster.
    Args:
        df (pandas dataframe): dataframe of a cluster
        k (int): number of neighbors to be found

    """
    dist_mat = pairwise_distances(df)
    dist_mat[dist_mat == 0] = np.nan  # drop the points with zero distance
    neighbors = np.argsort(dist_mat)[:, :k]  # sort based on the pairwise distance

    return neighbors

def recommendation(df, model, column_names=None, k=10):
    """The function generates the recommendation of each song based on the K-Means model passed in

    Args:
        df (pandas dataframe): dataframe to be used to generate the recommendations
        model (sklearn.cluster._kmeans.KMeans): K-Means model to be used to generate the recommendations
        column_names (list): list of features to be extracted from the dataframe
        k (int): number of recommendations

    Return:
        df_rec (pandas dataframe): dataframe with the recommendations

    """

    if column_names is None:
        column_names = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
                'loudness', 'speechiness', 'tempo', 'valence']

    df_scale = df[column_names]

    # Assign cluster to each datapoint
    df_cluster = df_scale.copy().assign(cluster=model.predict(df_scale), name=df['name'], artist=df['artists'])

    # Generate the recommendation
    numClusters = len(df_cluster['cluster'].unique())
    rec_result = []

    # Note that this for loop might take a long time to run
    logger.info("Started generating recommendations. This might take a while")
    logger.warning("If using docker and the process is killed, please increase the size of the memory")
    for i in range(numClusters):
        logger.debug("Started generating recommendations for cluster %d" % i)

        # filter to the corresponding cluster
        df_filter = df_cluster[df_cluster['cluster'] == i].reset_index(drop=True)

        # find the k points which are closet to a song
        neighbors = find_closet(df_filter[column_names], k)

        name = df_filter['name'].to_dict()
        closet_neighbors_info = np.vectorize(name.get)(neighbors)
        cluster_rec = pd.DataFrame(closet_neighbors_info, columns=[f'rec{i}' for i in range(1, k+1)])
        cluster_song = df_filter[['name', 'artist']].copy()
        cluster_final = pd.concat([cluster_song, cluster_rec], axis=1)

        rec_result.append(cluster_final)

        logger.debug("Finished generating recommendations for cluster %d" % i)

    # append the result of all clusters together
    df_rec = pd.concat(rec_result, axis=0).reset_index(drop=True)

    logger.info("Finished generating the recommendations")

    return df_rec