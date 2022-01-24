import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict
from csv import reader as csv_reader, writer as csv_writer
from time import time

PATH_REVIEWS = './data/prepared/social_influence/reviews.csv'
PATH_FRIENDS = './data/prepared/social_influence/friends.csv'
PATH_INFLUENCE = './data/prepared/social_influence/influence.csv'
SECONDS_PER_DAY = 60 * 60 * 24


def basic_influence_stats(export_influence_data=False, verbose=True):
    friend_graph = load_friend_graph(verbose=verbose)
    review_data = load_review_data(verbose=verbose)
    influence_counts, time_counts, influence_types, pp_pir_counts, extra_data = load_influenced_reviews(
        friend_graph,
        review_data,
        export_influence_data=export_influence_data,
        verbose=verbose
    )
    hist_num_influenced(influence_counts, extra_data['general'], max_amount=50, num_bins=50)
    hist_influence_time(time_counts, extra_data['time'], max_amount=3000, num_bins=140)
    hist_perc_positive_pirs(pp_pir_counts, max_amount=100, num_bins=100)
    table_influence_types(influence_types)


def hist_num_influenced(influence_counts, extra_data, max_amount=100, num_bins=100):
    values = []
    total = excluded = 0
    for amount, count in influence_counts.items():
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
    print('Influenced reviews:')
    print(f'- proportion_excluded = {excluded / total}')
    for label, value in extra_data.items():
        print(f'- {label} = {value}')


def hist_influence_time(time_counts, extra_data, max_amount=100, num_bins=100):
    values = []
    total = excluded = 0
    for amount, count in time_counts.items():
        total += count
        if amount > max_amount:
            excluded += count
            continue
        values.extend([amount] * count)
    df = pd.DataFrame(values)
    df.plot.hist(bins=num_bins, legend=None)
    plt.xlabel('Number of days between reviews')
    plt.ylabel('Number of reviews')
    plt.show()
    print('Influenced review time diffs:')
    print(f'- proportion_excluded = {excluded / total}')
    for label, value in extra_data.items():
        print(f'- {label} = {value}')


def hist_perc_positive_pirs(pir_counts, max_amount=10, num_bins=100):
    values = []
    total = excluded = zero = 00
    for amount, count in pir_counts.items():
        count = int(count)
        total += count
        if amount == 0:
            zero += count
        if amount > max_amount:
            excluded += count
            continue
        values.extend([amount] * count)
    df = pd.DataFrame(values)
    df.plot.hist(bins=num_bins, legend=None)
    plt.xlabel('Percentage of PIRs that are positive')
    plt.ylabel('Number of users')
    plt.show()
    print('PIRs:')
    print(f'- proportion_excluded = {excluded / total}')
    print(f'- proportion_zero = {zero / total}')


def table_influence_types(influence_types):
    print('Influenced review polarities:')
    labels = { 0: 'negative', 1: 'positive' }
    for i in range(2):
        for j in range(2):
            print(f'- influencer={labels[i]}, user={labels[j]}: {influence_types[i][j]}')


def load_influenced_reviews(friend_graph, review_data, export_influence_data=False, verbose=True):
    if verbose: print('Loading influence data')
    t = time()
    influenced_counts = {}
    influence_type_counts = [[0, 0], [0, 0]]
    time_counts = defaultdict(int)
    time_diff_counts = []
    influence_data = []
    pp_pir_counts = defaultdict(float)
    # for each user
    for uid, friend_uids in friend_graph.items():
        if uid not in influenced_counts:
            influenced_counts[uid] = 0
        user_pos = user_neg = 0
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
                        time_diff = (friend_ts - user_ts) // SECONDS_PER_DAY
                        time_counts[(friend_ts - user_ts) // SECONDS_PER_DAY] += 1
                        time_diff_counts.append(time_diff)
                        user_pos += 1
                        if export_influence_data:
                            influence_data.append((uid, friend_uid, gid, user_pol, friend_pol, user_ts, friend_ts))
                else:
                    user_neg += 1
        if user_pos != 0 or user_neg != 0:
            user_perc = round(100 * user_pos / (user_pos + user_neg), 2)
            pp_pir_counts[user_perc] += 1
    influence_counts = []
    counts = defaultdict(int)
    for amount in influenced_counts.values():
        influence_counts.append(amount)
        counts[amount] += 1
    num_influenced = len(influence_data)
    influence_counts = np.array(influence_counts)
    time_diff_counts = np.array(time_diff_counts)
    extra_data = {
        'general': {
            'num_influenced': num_influenced,
            'median_influenced': np.median(influence_counts),
            'mean_influenced': influence_counts.mean(),
            'dev_influenced': influence_counts.std()
        },
        'time': {
            'median_time': np.median(time_diff_counts),
            'mean_time': time_diff_counts.mean(),
            'dev_time': time_diff_counts.std()
        }
    }
    if verbose: print(f'Loaded influence data in {int(time() - t)} seconds')
    if export_influence_data:
        if verbose: print(f'Exporting influence data')
        t = time()
        with open(PATH_INFLUENCE, 'w+', newline='') as f:
            writer = csv_writer(f, delimiter=',')
            writer.writerows(influence_data)
        if verbose: print(f'Exported influence data in {int(time() - t)} seconds')
    return counts, time_counts, influence_type_counts, pp_pir_counts, extra_data


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
    parser.add_argument('-e', '--export_influence_data', action='store_true', help='export data on influenced reviews')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    basic_influence_stats(
        export_influence_data=args.export_influence_data,
        verbose=args.verbose
    )
