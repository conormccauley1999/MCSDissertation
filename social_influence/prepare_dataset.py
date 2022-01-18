from csv import reader as csv_reader, writer as csv_writer

PATH_REVIEWS_IN = './data/raw/reviews/redist/page_%d.csv'
PATH_FRIENDS_IN = './data/raw/friends/redist/page_%d.csv'
PAGE_COUNT_REVIEWS = 28
PAGE_COUNT_FRIENDS = 14
PATH_REVIEWS_OUT = './data/prepared/social_influence/reviews.csv'
PATH_FRIENDS_OUT = './data/prepared/social_influence/friends.csv'


def prepare_dataset(verbose=True):
    unique_user_ids, user_id_map = prepare_review_data(verbose=verbose)
    prepare_friend_data(unique_user_ids, user_id_map, verbose=verbose)


def prepare_review_data(verbose=True):
    if verbose: print('Loading review data')
    unique_user_ids = set()
    user_id_map = {}
    game_id_map = {}
    user_count = 0
    game_count = 0
    review_data = []
    for page_num in range(1, PAGE_COUNT_REVIEWS + 1):
        with open(PATH_REVIEWS_IN % page_num, 'r', newline='', encoding='utf-8') as f:
            reader = csv_reader(f, delimiter=',')
            for row in reader:
                user_id = int(row[0])
                game_id = int(row[1])
                polarity = int(row[2])
                timestamp = int(row[3])
                unique_user_ids.add(user_id)
                if user_id not in user_id_map:
                    user_id_map[user_id] = user_count
                    user_count += 1
                if game_id not in game_id_map:
                    game_id_map[game_id] = game_count
                    game_count += 1
                review_data.append([
                    user_id_map[user_id],
                    game_id,#game_id_map[game_id],
                    polarity,
                    timestamp
                ])
        if verbose:
            print(f'Loaded review page {page_num}: {len(unique_user_ids)} users found')
    if verbose: print('Saving review data')
    with open(PATH_REVIEWS_OUT, 'w+', newline='') as f:
        writer = csv_writer(f, delimiter=',')
        writer.writerows(review_data)
    return unique_user_ids, user_id_map


def prepare_friend_data(unique_user_ids, user_id_map, verbose=True):
    if verbose: print('Loading friend data')
    friend_data = []
    for page_num in range(1, PAGE_COUNT_FRIENDS + 1):
        with open(PATH_FRIENDS_IN % page_num, 'r', newline='') as f:
            reader = csv_reader(f, delimiter=',')
            for row in reader:
                user_ids = list(map(int, row))
                root_user_id = user_ids[0]
                if root_user_id not in unique_user_ids:
                    continue
                new_root_user_id = user_id_map[root_user_id]
                user_data = [new_root_user_id]
                for friend_user_id in user_ids[1:]:
                    if friend_user_id not in unique_user_ids:
                        continue
                    new_friend_user_id = user_id_map[friend_user_id]
                    user_data.append(new_friend_user_id)
                friend_data.append(user_data)
        if verbose:
            print(f'Loaded friend page {page_num}: {len(friend_data)} root users found')
    if verbose: print('Saving friend data')
    with open(PATH_FRIENDS_OUT, 'w+', newline='') as f:
        writer = csv_writer(f, delimiter=',')
        writer.writerows(friend_data)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    prepare_dataset(
        verbose=args.verbose
    )
