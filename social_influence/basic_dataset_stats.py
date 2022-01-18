import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict
from csv import reader as csv_reader

PATH_REVIEWS = './data/prepared/social_influence/reviews.csv'
PATH_FRIENDS = './data/prepared/social_influence/friends.csv'


def hist_num_friends(max_amount=100, num_bins=100):
    friend_counts = load_friend_counts()
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
    print(f'Proportion excluded = {excluded / total}')


def load_friend_counts():
    graph = defaultdict(set)
    with open(PATH_FRIENDS, 'r', newline='') as f:
        reader = csv_reader(f, delimiter=',')
        for row in reader:
            uids = list(map(int, row))
            root_uid = uids[0]
            for friend_uid in uids[1:]:
                graph[root_uid].add(friend_uid)
                graph[friend_uid].add(root_uid)
    counts = defaultdict(int)
    for friend_list in graph.values():
        counts[len(friend_list)] += 1
    return counts


def hist_num_reviews(max_amount=100, num_bins=100):
    review_counts = load_review_counts()
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
    print(f'Proportion excluded = {excluded / total}')


def load_review_counts():
    user_counts = defaultdict(int)
    with open(PATH_REVIEWS, 'r', newline='') as f:
        reader = csv_reader(f, delimiter=',')
        for row in reader:
            uid = int(row[0])
            user_counts[uid] += 1
    counts = defaultdict(int)
    for user_count in user_counts.values():
        counts[user_count] += 1
    return counts


if __name__ == '__main__':
    hist_num_friends(max_amount=200, num_bins=200)
    hist_num_reviews(max_amount=50, num_bins=50)
