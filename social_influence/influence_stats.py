import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict
from csv import reader as csv_reader
from time import time

PATH_REVIEWS = './data/prepared/social_influence/reviews.csv'
PATH_FRIENDS = './data/prepared/social_influence/friends.csv'
SECONDS_PER_DAY = 60 * 60 * 24


def hist_num_influenced(max_amount=100, num_bins=100, verbose=True):
    friend_graph = load_friend_graph(verbose=verbose)
    review_data = load_review_data(verbose=verbose)
    inf_counts, time_counts, inf_type_counts = load_influenced_reviews(
        friend_graph,
        review_data,
        verbose=verbose
    )
    values = []
    total = excluded = 0
    for amount, count in inf_counts.items():
        total += count
        if amount > max_amount:
            excluded += count
            continue
        values.extend([amount] * count)
    df = pd.DataFrame(values)
    df.plot.hist(bins=num_bins, legend=None)
    plt.xlabel('Number of influenced reviews')
    plt.ylabel('Number of users')
    plt.show()
    print(f'Proportion excluded = {excluded / total}')
    # time diff histogram
    values = []
    total = excluded = 0
    for amount, count in time_counts.items():
        total += count
        if amount > 3000:
            excluded += count
            continue
        values.extend([amount] * count)
    df = pd.DataFrame(values)
    df.plot.hist(bins=140, legend=None)
    plt.xlabel('Number of days between reviews')
    plt.ylabel('Number of reviews')
    plt.show()
    print(f'Proportion excluded = {excluded / total}')


def load_influenced_reviews(friend_graph, review_data, verbose=True):
    if verbose: print('Loading influence data')
    t = time()
    influenced_counts = {}
    influence_type_counts = [[0, 0], [0, 0]]
    time_counts = defaultdict(int)
    # for each user
    for uid, friend_uids in friend_graph.items():
        if uid not in influenced_counts:
            influenced_counts[uid] = 0
        user_data = review_data[uid]
        # for each game user reviewed
        for gid in user_data['gids']:
            # for each user friend
            for friend_uid in friend_uids:
                friend_data = review_data[friend_uid]
                # if friend also reviewed game
                if gid in friend_data['gids']:
                    user_ts, user_pol = user_data['revs'][gid]
                    friend_ts, friend_pol = friend_data['revs'][gid]
                    # if user reviewed before friend
                    if user_ts < friend_ts:
                        influenced_counts[uid] += 1
                        influence_type_counts[user_pol][friend_pol] += 1
                        time_counts[(friend_ts - user_ts) // SECONDS_PER_DAY] += 1
    counts = defaultdict(int)
    for amount in influenced_counts.values():
        counts[amount] += 1
    if verbose: print(f'Loaded influence data in {int(time() - t)} seconds')
    return counts, time_counts, influence_type_counts


def load_friend_graph(verbose=True):
    if verbose: print('Loading friend graph')
    t = time()
    friend_graph = defaultdict(set)
    with open(PATH_FRIENDS, 'r', newline='') as f:
        reader = csv_reader(f, delimiter=',')
        for row in reader:
            uids = list(map(int, row))
            root_uid = uids[0]
            for friend_uid in uids[1:]:
                friend_graph[root_uid].add(friend_uid)
                friend_graph[friend_uid].add(root_uid)
    if verbose: print(f'Loaded friend graph in {int(time() - t)} seconds')
    return friend_graph


def load_review_data(verbose=True):
    if verbose: print('Loading review data')
    t = time()
    review_data = {}
    with open(PATH_REVIEWS, 'r', newline='') as f:
        reader = csv_reader(f, delimiter=',')
        for row in reader:
            uid = int(row[0])
            gid = int(row[1])
            polarity = int(row[2])
            timestamp = int(row[3])
            if uid not in review_data:
                review_data[uid] = { 'gids': set(), 'revs': {} }
            review_data[uid]['gids'].add(gid)
            review_data[uid]['revs'][gid] = (timestamp, polarity)
    if verbose: print(f'Loaded review data in {int(time() - t)} seconds')
    return review_data


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    hist_num_influenced(
        max_amount=50,
        num_bins=50,
        verbose=args.verbose
    )
