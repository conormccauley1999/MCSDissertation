from json_lines import reader as jl_reader
from collections import defaultdict
from scipy import sparse
from time import time

from utils import save_matrix, str_to_uid


def load_friends(filename, verbose):
    # load friends from file into map of sets
    print('Loading friends...')
    t = time()
    friend_map = defaultdict(set)
    line_num = 0
    with open(f'./data/jl/{filename}.jl', 'rb') as f:
        for item in jl_reader(f):
            line_num += 1
            if verbose and not line_num % 10000: print(f'{line_num} lines parsed, {len(friend_map)} users found')
            root_uid = str_to_uid(item['steamid'])
            for friend_uid in map(str_to_uid, item['ids']):
                friend_map[root_uid].add(friend_uid)
    print(f'Loaded friends in {int(time() - t)} seconds')
    # convert map into sparse matrix and save to file
    print(f'Generating matrix...')
    t = time()
    n = len(friend_map)
    friend_mat = sparse.lil_matrix((n, n))
    for i in range(n):
        for j in friend_map[i]:
            friend_mat[i, j] = 1
            friend_mat[j, i] = 1
    save_matrix(filename, friend_mat)
    print(f'Generated matrix in {int(time() - t)} seconds')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='name of json lined file in data directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    load_friends(args.filename, args.verbose)
