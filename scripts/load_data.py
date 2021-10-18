import argparse
from json import load
import json_lines
import time
from collections import defaultdict
from scipy import sparse
from scipy.io import savemat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='name of json lined file in data directory')
    parser.add_argument('-m', '--mode', choices=['friends'], help='type of data that is being loaded')
    args = parser.parse_args()
    if args.mode == 'friends':
        load_friends(args.filename)


def load_friends(filename):
    # logging
    print('Loading friends')
    start_time = time.time()
    # data
    friend_map = defaultdict(set)
    unique_uids = set()
    idx_to_uid = {}
    uid_to_idx = {}
    idx = 0
    # add user id to above data
    def add_uid(uid, idx):
        if uid in unique_uids: return idx
        unique_uids.add(uid)
        idx_to_uid[idx] = uid
        uid_to_idx[uid] = idx
        return idx + 1
    # iterate over dataset
    with open(f'./data/{filename}.jl', 'rb') as f:
        for item in json_lines.reader(f):
            uid = str_to_uid(item['steamid'])
            idx = add_uid(uid, idx)
            uidx = uid_to_idx[uid]
            for fuid in map(str_to_uid, item['ids']):
                idx = add_uid(fuid, idx)
                fidx = uid_to_idx[fuid]
                friend_map[uidx].add(fidx)
                friend_map[fidx].add(uidx)
    # store as matrix
    N = idx
    friends = sparse.lil_matrix((N, N))
    for i in range(N):
        for j in friend_map[i]:
            friends[i, j] = 1
    savemat(f'./data/{filename}.mat', mdict={'friends': friends})
    # logging
    end_time = time.time()
    print(f'Loaded friends for {len(unique_uids)} users in {int(end_time - start_time)} seconds')


def str_to_uid(string):
    # strip 'profiles/' and convert to integer
    return int(string[9:])


if __name__ == '__main__':
    main()
