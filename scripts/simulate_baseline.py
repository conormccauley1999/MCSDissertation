import numpy as np
from math import ceil
from matplotlib import pyplot as plt
from random import shuffle
from numpy.core.numeric import load
from scipy.io import loadmat
from time import time

from utils import load_matrix, save_matrix


def convert_results(results, step=0.05):
    num_bins = int(ceil(1 / step)) + 1
    bins = []
    for _ in range(num_bins): bins.append([])
    for x, y, _ in results:
        i = min(int(round(x / step)), num_bins)
        bins[i].append(y)
    for i in range(num_bins):
        if not len(bins[i]):
            bins[i] = [0.01]
    x = np.array([
        round(i * step, 2)
        for i in range(num_bins)
    ])
    y = np.array([*map(np.mean, bins)])
    e = np.array([*map(np.var, bins)])
    return x, y, e


def display_results(results):
    x, y, e = convert_results(results)
    plt.bar(x, y, width=0.04, yerr=e)
    plt.xlabel('Percent positive ratings')
    plt.ylabel('Percent audience reached')
    plt.xticks(x[::2])
    plt.xlim([-0.05, 1.05])
    plt.ylim([0, 1.05])
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


def simulate_baseline(matrix, runs, start_size, growth_factor, min_proportion, verbose):
    game_count = matrix.shape[1]
    # data storing
    results = []
    # generate list of games to run simulations for
    indices = list(range(game_count))
    if runs != 0:
        shuffle(indices)
        indices = indices[:runs]
    # logging
    print(f'Running {len(indices)} simulations from {game_count} games')
    t = time()
    i = 0
    # run simulations
    for column_index in indices:
        column = matrix.getcol(column_index)
        # get a list of ratings for the game
        indices = column.nonzero()[0]
        ratings = []
        for row_index in indices:
            ratings.append(column[row_index, 0])
        # store some stats
        rating_count = len(ratings)
        percent_positive = ratings.count(1) / rating_count
        # simulate the potential audience reached
        percent_reached = simulate_baseline_for_game(ratings, start_size, growth_factor, min_proportion)
        results.append((percent_positive, percent_reached, rating_count))
        # verbose logging
        i += 1
        if verbose and not i % 500:
            print(f'{i} simulations completed')
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
    matrix = load_matrix(args.filename, 'R')
    results = simulate_baseline(matrix, args.runs, args.start_size, args.growth_factor, args.min_proportion, args.verbose)
    display_results(results)
