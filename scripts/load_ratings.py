from json_lines import reader as jl_reader
from scipy import sparse
from scipy.io import savemat
from time import time

from helpers import str_to_uid

LOG_FREQUENCY = 100000
MIN_PAGE = 1
MAX_PAGE = 524


def load_ratings(start_page, end_page, threshold, verbose):
    # logging
    print(f'Loading ratings for pages {start_page}-{end_page}')
    t = time()
    # data storing
    user_map = {} # map user_id to user_index
    game_map = {} # map game_id to game_index
    user_ratings = {} # user game ratings
    user_count = 0 # user index counter
    game_count = 0 # game index counter
    # iterate over review pages
    for page in range(start_page, end_page + 1):
        with open(f'./data/reviews/review_page{page}.jl', 'rb') as f:
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
                        game_count += 1
                    game_idx = game_map[game_id]
                    # store the rating
                    user_ratings[user_idx][rating].add(game_idx)
                # verbose logging
                if verbose and not user_count % LOG_FREQUENCY:
                    print(f'{user_count} users parsed (page = {page}), {game_count} games found')
    # logging
    print(f'Loaded games in {int(time() - t)} seconds')
    print(f'Generating matrix ({user_count} x {game_count})')
    t = time()
    # convert data into sparse matrix and save
    matrix = sparse.lil_matrix((user_count, game_count))
    for user_idx in range(user_count):
        for game_idx in user_ratings[user_idx][0]:
            matrix[user_idx, game_idx] = -1
        for game_idx in user_ratings[user_idx][1]:
            matrix[user_idx, game_idx] = 1
    savemat(f'./data/matrices/ratings_{start_page}-{end_page}.mat', mdict={'R': matrix})
    # logging
    print(f'Generated matrix in {int(time() - t)} seconds')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_page', type=int, default=1, help='review page to start at')
    parser.add_argument('-e', '--end_page', type=int, default=524, help='review page to end at (inclusive)')
    parser.add_argument('-t', '--threshold', type=int, default=50, help='minimum number of reviews for game to be included')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    assert MIN_PAGE <= args.start_page <= args.end_page <= MAX_PAGE
    load_ratings(args.start_page, args.end_page, args.threshold, args.verbose)
