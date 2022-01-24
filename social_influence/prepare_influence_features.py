from collections import defaultdict
from csv import reader as csv_reader, writer as csv_writer
from random import uniform
from time import time

PATH_FRIENDS = './data/prepared/social_influence/friends.csv'
PATH_REVIEWS = './data/prepared/social_influence/reviews.csv'
PATH_FEATURES = './data/prepared/social_influence/influence_features.csv'


def prepare_influence_features(percent_negative=0.05, verbose=True):
    friend_graph = load_friend_graph(verbose=verbose)
    review_data = load_review_data(verbose=verbose)
    influence_features = load_influence_features(
        friend_graph,
        review_data,
        verbose=verbose
    )
    return
    if verbose: print(f'Saving influence features')
    t = time()
    with open(PATH_FEATURES, 'w+', newline='') as f:
        writer = csv_writer(f, delimiter=',')
        writer.writerows(influence_features)
    if verbose: print(f'Saving influence features in {int(time() - t)} seconds')


def load_influence_features(friend_graph, review_data, percent_negative=0.05, verbose=True):
    if verbose: print('Loading influence features')
    t = time()
    data = []
    # for each user
    for uid, friend_uids in friend_graph.items():
        user_data = review_data[uid]
        feature_u_friends = len(friend_uids)
        feature_u_reviews = len(user_data['gids'])
        # for each game user reviewed
        for gid in user_data['gids']:
            feature_rating = user_data['revs'][gid][1]
            # for each user friend
            for friend_uid in friend_uids:
                friend_data = review_data[friend_uid]
                feature_v_friends = len(friend_graph[friend_uid])
                # if friend also reviewed game
                if gid in friend_data['gids']:
                    user_ts = user_data['revs'][gid][0]
                    friend_ts = friend_data['revs'][gid][0]
                    # if user reviewed before friend
                    if user_ts < friend_ts:
                        data.append((feature_rating, feature_u_friends, feature_v_friends, feature_u_reviews, 1))
                elif uniform(0, 1) < percent_negative:
                    data.append((feature_rating, feature_u_friends, feature_v_friends, feature_u_reviews, 0))
    if verbose: print(f'Loaded influence data in {int(time() - t)} seconds')
    return data


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
    parser.add_argument('-p', '--percent_negative', type=float, default=0.05, help='percentage of potential but negative reviews to include')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    prepare_influence_features(
        percent_negative=args.percent_negative,
        verbose=args.verbose
    )
