import numpy as np
from matplotlib import pyplot as plt
from random import shuffle
from scipy.io import loadmat
from time import time

from helpers import list_to_npa


def sb_display(results):
    # bins:
    # (0.00-0.05,0.05-0.10,...,0.95-1.00)
    x = list_to_npa(results, i=0, dtype=float)
    y = list_to_npa(results, i=1, dtype=float)
    s = list_to_npa(results, i=2, dtype=float)
    s *= 150 / s.max()
    plt.scatter(x, y, s=s)
    plt.xlabel('Percent positive ratings')
    plt.ylabel('Percent audience reached')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.show()


def simulate_iteration(ratings, size):
    shuffle(ratings)
    audience, remaining = ratings[:size], ratings[size:]
    proportion = audience.count(1) / len(audience)
    return proportion, remaining


def simulate_baseline_for_game(ratings, start_size, growth_factor, min_proportion):
    potential_users = ratings.count(1)
    users_reached = 0
    size = start_size
    while ratings:
        real_size = min(size, len(ratings))
        proportion, ratings = simulate_iteration(ratings, size)
        users_reached += int(real_size * proportion)
        if proportion < min_proportion:
            break
        size *= growth_factor
    return users_reached / potential_users


def simulate_baseline(filename, runs, start_size, growth_factor, min_proportion, verbose):
    # read in matrix
    matrix = loadmat(f'./data/matrices/{filename}.mat')['R']
    user_count, game_count = matrix.shape
    # logging
    print(f'Running simulations for {game_count} games')
    t = time()
    # data storing
    results = []
    # generate list of games to run simulations for
    indices = list(range(game_count))
    if runs != 0:
        shuffle(indices)
        indices = indices[:runs]
    # run simulations
    for i in indices:
        column = matrix.getcol(i)
        # get a list of ratings for the game
        indices = column.nonzero()[0]
        ratings = []
        for index in indices:
            ratings.append(column[index, 0])
        # store some stats
        rating_count = len(ratings)
        percent_positive = ratings.count(1) / rating_count
        # simulate the potential audience reached
        percent_reached = simulate_baseline_for_game(ratings, start_size, growth_factor, min_proportion)
        results.append((percent_positive, percent_reached, rating_count))
        # verbose logging
        if verbose and not (i + 1) % 500:
            print(f'{i + 1} simulations completed')
    # logging
    print(f'Ran simulations in {int(time() - t)} seconds')
    return results


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='name of ratings matrix file')
    parser.add_argument('-r', '--runs', type=int, default=0, help='number of simulations to run (0 = all games)')
    parser.add_argument('-s', '--start_size', type=int, default=10, help='starting size of audience')
    parser.add_argument('-g', '--growth_factor', type=int, default=5, help='growth factor of audience')
    parser.add_argument('-p', '--min_proportion', type=float, default=0.7, help='minimum proportion of audience needed to continue')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    results = simulate_baseline(args.filename, args.runs, args.start_size, args.growth_factor, args.min_proportion, args.verbose)
    sb_display(results)
