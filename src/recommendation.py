import logging

import numpy as np
import pandas as pd

from sklearn.metrics import pairwise_distances

logger = logging.getLogger(__name__)

def recommendation(df, model, column_names=None, k=10):

    if column_names is None:
        column_names = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
                'loudness', 'speechiness', 'tempo', 'valence']

    df_scale = df[column_names]

    # Assign cluster to each datapoint
    df_cluster = df_scale.copy().assign(cluster=model.predict(df_scale), name=df['name'], artist=df['artists'])

    # Generate the recommendation
    numClusters = len(df_cluster['cluster'].unique())
    rec_result = []

    for i in range(numClusters):
        logger.info("Started generating recommendations for cluster %d" % i)

        # filter to the corresponding cluster
        df_filter = df_cluster[df_cluster['cluster'] == i].reset_index(drop=True)

        # find the k points which are closet to a song
        dist_mat = pairwise_distances(df_filter[column_names])
        dist_mat[dist_mat == 0] = np.nan
        neighbors = np.argsort(dist_mat)[:, :k]

        name = df_filter['name'].to_dict()
        closet_neighbors_info = np.vectorize(name.get)(neighbors)
        cluster_rec = pd.DataFrame(closet_neighbors_info, columns=[f'rec{i}' for i in range(1, k+1)])
        cluster_song = df_filter[['name', 'artist']].copy()
        cluster_final = pd.concat([cluster_song, cluster_rec], axis=1)

        rec_result.append(cluster_final)

        logger.info("Finished generating recommendations for cluster %d" % i)

    # append the result of all clusters together
    df_rec = pd.concat(rec_result, axis=0).reset_index(drop=True)

    # Convert the dataframe from wide to long to include more information for each recommended song
    df_long = df_rec.melt(id_vars=['name', 'artist'], var_name="Rank", value_name="Recommended Song")
    df_long['Rank'] = df_long.Rank.str.replace('rec', '').astype(int)
    df_long = df_long.sort_values(['name', 'artist', 'Rank'], ignore_index=True)
    df_long.rename(columns={'name': 'Song Title'}, inplace=True)

    # Add the artist and duration information to the recommended songs
    info = ['name', 'artists', 'duration_ms']
    df_final_rec = df_long.merge(df[info], how='inner', left_on='Recommended Song', right_on='name')
    df_final_rec = df_final_rec.drop('name', axis=1).groupby(['Song Title', 'artist', 'Rank']).first().reset_index()
    df_final_rec.columns = ['Song Title', 'Artist', 'Rank', 'Recommended Song', 'Recommended Song Artist',
                            'Duration_ms']

    logger.info("Finished generating the recommendations")

    return df_final_rec