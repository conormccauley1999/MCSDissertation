import numpy as np
from sklearn.cluster import KMeans
from time import time

from utils import save_matrix, load_matrix


def cluster_users(matrix, num_clusters, verbose):
    user_count = matrix.shape[0]
    # logging
    print(f'Running k-means clustering on {user_count} users')
    t = time()
    # cluster users
    km = KMeans(n_clusters=num_clusters).fit(matrix)
    # logging
    print(f'Clustered users in {int(time() - t)} seconds')
    return np.c_[np.arange(user_count), km.labels_]


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file', help='ratings matrix filename')
    parser.add_argument('out_file', help='output matrix filename')
    parser.add_argument('-n', '--num_clusters', type=int, default=5, help='number of clusters')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    matrix_ratings = load_matrix(args.in_file)
    matrix_clusters = cluster_users(matrix_ratings, args.num_clusters, args.verbose)
    save_matrix(args.out_file, matrix_clusters)
