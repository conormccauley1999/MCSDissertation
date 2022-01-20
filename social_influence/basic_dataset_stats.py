import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict
from csv import reader as csv_reader
from time import time

PATH_REVIEWS = './data/prepared/social_influence/reviews.csv'
PATH_FRIENDS = './data/prepared/social_influence/friends.csv'


def basic_dataset_stats(verbose=True):
    hist_num_friends(max_amount=200, num_bins=200, verbose=verbose)
    hist_num_reviews(max_amount=50, num_bins=50, verbose=verbose)


def hist_num_friends(max_amount=100, num_bins=100, verbose=True):
    friend_counts, extra_data = load_friend_counts(verbose=verbose)
    values = []
    total = excluded = 0
    for amount, count in friend_counts.items():
        total += count
        if amount > max_amount:
            excluded += count
            continue
        values.extend([amount] * count)
    df = pd.DataFrame(values)
    df.plot.hist(bins=num_bins, legend=None)
    plt.xlabel('Number of friends')
    plt.ylabel('Number of users')
    plt.show()
    print('Friends:')
    print(f'- proportion_excluded = {excluded / total}')
    for label, value in extra_data.items():
        print(f'- {label} = {value}')


def load_friend_counts(verbose=True):
    if verbose: print('Loading friend data')
    t = time()
    graph = defaultdict(set)
    with open(PATH_FRIENDS, 'r', newline='') as f:
        reader = csv_reader(f, delimiter=',')
        for row in reader:
            uids = list(map(int, row))
            root_uid = uids[0]
            for friend_uid in uids[1:]:
                graph[root_uid].add(friend_uid)
                graph[friend_uid].add(root_uid)
    num_users = 0
    num_friendships = 0
    friend_counts = []
    counts = defaultdict(int)
    for friend_list in graph.values():
        num_users += 1
        num_friendships += len(friend_list)
        friend_counts.append(len(friend_list))
        counts[len(friend_list)] += 1
    num_friendships //= 2
    friend_counts = np.array(friend_counts)
    extra_data = {
        'num_users': num_users,
        'num_friendships': num_friendships,
        'median_friends': np.median(friend_counts),
        'mean_friends': friend_counts.mean(),
        'dev_friends': friend_counts.std()
    }
    if verbose: print(f'Loaded friend data in {int(time() - t)} seconds')
    return counts, extra_data


def hist_num_reviews(max_amount=100, num_bins=100, verbose=True):
    review_counts, extra_data = load_review_counts(verbose=verbose)
    values = []
    total = excluded = 0
    for amount, count in review_counts.items():
        total += count
        if amount > max_amount:
            excluded += count
            continue
        values.extend([amount] * count)
    df = pd.DataFrame(values)
    df.plot.hist(bins=num_bins, legend=None)
    plt.xlabel('Number of reviews')
    plt.ylabel('Number of users')
    plt.show()
    print('Reviews:')
    print(f'- proportion_excluded = {excluded / total}')
    for label, value in extra_data.items():
        print(f'- {label} = {value}')


def load_review_counts(verbose=True):
    if verbose: print('Loading review data')
    t = time()
    num_reviews = 0
    review_counts = []
    user_counts = defaultdict(int)
    with open(PATH_REVIEWS, 'r', newline='') as f:
        reader = csv_reader(f, delimiter=',')
        for row in reader:
            num_reviews += 1        
            uid = int(row[0])
            user_counts[uid] += 1
    counts = defaultdict(int)
    for user_count in user_counts.values():
        review_counts.append(user_count)
        counts[user_count] += 1
    review_counts = np.array(review_counts)
    extra_data = {
        'num_reviews': num_reviews,
        'median_reviews': np.median(review_counts),
        'mean_reviews': review_counts.mean(),
        'dev_reviews': review_counts.std()
    }
    if verbose: print(f'Loaded review data in {int(time() - t)} seconds')
    return counts, extra_data


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    basic_dataset_stats(
        verbose=args.verbose
    )
