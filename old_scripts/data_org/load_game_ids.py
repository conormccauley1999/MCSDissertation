# imports
from csv import reader as csv_reader, writer as csv_writer
from time import time

from review_constants import *


def load_game_ids(verbose=True):
    # logging
    if verbose: print(f"Loading game IDs")
    t = time()
    # stored data
    data = {}
    # iterate over review pages
    for page_num in range(1, NUM_REDIST_REVIEW_PAGES + 1):
        with open(PATH_REVIEW_REDIST % page_num, 'r', encoding='utf-8') as f:
            reader = csv_reader(f, delimiter=',')
            for review in reader:
                # extract data
                game_id = int(review[ReviewCols.GID])
                polarity = int(review[ReviewCols.POLARITY])
                # store data
                if game_id not in data:
                    data[game_id] = [0, 0]
                data[game_id][polarity] += 1
        # logging
        if verbose:
            print(f'Loaded game IDs from page {page_num}')
    # reformat data
    new_data = []
    for game_id, (pos, neg) in data.items():
        new_data.append([game_id, pos, neg])
    new_data.sort()
    # save loaded data
    with open(PATH_GAME_DATA % 'game_ids', 'w+', newline='', encoding='utf-8') as f:
        writer = csv_writer(f, delimiter=',')
        writer.writerows(new_data)
    # logging
    if verbose: print(f'Loaded and saved game IDs in {int(time() - t)} seconds')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    load_game_ids(
        verbose=args.verbose
    )
