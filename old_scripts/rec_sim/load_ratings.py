from collections import defaultdict
from json_lines import reader as jl_reader
from scipy import sparse
from time import time

from utils import save_extras, save_matrix, str_to_uid


def load_ratings(start_page=1, end_page=524, threshold=1000, verbose=True):
    # logging
    print(f'Loading ratings for pages {start_page}-{end_page}')
    t = time()
    # data storing (for matrix generation)
    user_map = {} # map user id to index
    game_map = {} # map game id to index
    user_ratings = {} # game ratings for each user
    num_ratings = defaultdict(int) # number of ratings for each game
    user_count = 0 # user index counter
    game_count = 0 # game index counter
    # data storing (for extra info)
    extras_dict = {}
    game_map_inv = {} # map game index to id
    game_ratings = {}
    user_rating_data = {}
    # iterate over review pages
    for page in range(start_page, end_page + 1):
        with open(f'./data/jl/reviews/review_page{page}.jl', 'rb') as f:
            # for each user in this page
            for item in jl_reader(f):
                # get the user id and store the index
                user_id = str_to_uid(item['steamid'])
                user_map[user_id] = user_count
                user_idx = user_count
                user_count += 1
                # initialise sets for user ratings
                user_ratings[user_idx] = [set(), set()]
                # for each game the user rated
                for game in item['reviews']:
                    game_id = int(game['appid'])
                    rating = int(game['voted_up'])
                    # if the game is new then store the index
                    if game_id not in game_map:
                        game_map[game_id] = game_count
                        game_map_inv[game_count] = game_id
                        game_count += 1
                    game_idx = game_map[game_id]
                    # store the rating
                    user_ratings[user_idx][rating].add(game_idx)
                    num_ratings[game_idx] += 1
                    if game_idx not in game_ratings:
                        game_ratings[game_idx] = [0, 0]
                    game_ratings[game_idx][rating] += 1
                # verbose logging
                if verbose and not user_count % 100000:
                    print(f'{user_count} users parsed (page = {page}), {game_count} games found')
    # remove games without a certain number of reviews
    filt_game_map = {} # map original game index to filtered game index
    filt_game_map_inv = {} # map filtered game index to game id and other info
    filt_game_count = 0 # filtered game index counter
    for game_idx in range(game_count):
        if num_ratings[game_idx] >= threshold:
            n_neg, n_pos = game_ratings[game_idx]
            filt_game_map_inv[filt_game_count] = [game_map_inv[game_idx], n_neg, n_pos]
            filt_game_map[game_idx] = filt_game_count
            filt_game_count += 1
    print(f'Ignoring {game_count - filt_game_count} games')
    # remove users without any included reviews
    valid_user_idxs = set()
    for user_idx in range(user_count):
        any_valid = False
        for ratings in user_ratings[user_idx]:
            if any_valid: break
            for game_idx in ratings:
                if game_idx in filt_game_map:
                    any_valid = True
                    break
        if any_valid:
            valid_user_idxs.add(user_idx)
    filt_user_count = len(valid_user_idxs)
    # logging
    print(f'Ignoring {user_count - filt_user_count} users')
    print(f'Loaded games in {int(time() - t)} seconds')
    print(f'Generating matrix ({filt_user_count} x {filt_game_count})')
    t = time()
    # convert data into sparse matrix
    matrix = sparse.lil_matrix((filt_user_count, filt_game_count))
    filt_user_idx = 0
    for user_idx in valid_user_idxs:
        sum_abs_diff = 0
        sum_real_diff = 0
        sum_ratings = 0
        n_ratings = 0
        n_valid_ratings = 0
        for polarity, ratings in zip([-1, 1], user_ratings[user_idx]):
            for game_idx in ratings:
                # extra data
                n_neg, n_pos = game_ratings[game_idx]
                game_rating = n_pos / (n_pos + n_neg)
                user_rating = 0 if polarity < 0 else 1
                sum_abs_diff += abs(user_rating - game_rating)
                sum_real_diff += user_rating - game_rating
                sum_ratings += user_rating
                n_ratings += 1
                # add to matrix
                if game_idx in filt_game_map:
                    filt_game_idx = filt_game_map[game_idx]
                    matrix[filt_user_idx, filt_game_idx] = polarity
                    n_valid_ratings += 1
        user_rating_data[filt_user_idx] = [
            round(sum_abs_diff / n_ratings, 3),
            round(sum_real_diff / n_ratings, 3),
            round(sum_ratings / n_ratings, 3),
            n_ratings,
            n_valid_ratings
        ]
        filt_user_idx += 1
    # logging
    print(f'Generated matrix in {int(time() - t)} seconds')
    print(f'Preparing extra data')
    t = time()
    # extra data
    game_data = []
    for game_idx, other_fields in filt_game_map_inv.items():
        game_data.append((game_idx, *other_fields))
    extras_dict['game'] = game_data
    user_data = []
    for user_idx, other_fields in user_rating_data.items():
        user_data.append((user_idx, *other_fields))
    extras_dict['user'] = user_data
    # logging
    print(f'Prepared extra data in {int(time() - t)} seconds')
    return matrix, extras_dict


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('out_file', help='output matrix filename')
    parser.add_argument('-s', '--start_page', type=int, default=1, help='review page to start at')
    parser.add_argument('-e', '--end_page', type=int, default=524, help='review page to end at (inclusive)')
    parser.add_argument('-t', '--threshold', type=int, default=1000, help='minimum number of reviews for game to be included')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    matrix, extras = load_ratings(
        start_page=args.start_page,
        end_page=args.end_page,
        threshold=args.threshold,
        verbose=args.verbose
    )
    save_matrix(args.out_file, matrix)
    save_extras(args.out_file, extras)