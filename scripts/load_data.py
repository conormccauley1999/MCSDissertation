import json_lines
import time
from collections import defaultdict
from scipy import sparse
from scipy.io import savemat

FRIENDS_PATH = './data/friends_1000.jl'


def str_to_uid(string):
    # strip 'profiles/' and convert to integer
    return int(string[9:])


def load_friends():
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
    with open(FRIENDS_PATH, 'rb') as f:
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
    savemat('friends.mat', mdict={'friends': friends})
    # logging
    end_time = time.time()
    print(f'Loaded friends for {len(unique_uids)} users in {int(end_time - start_time)} seconds')


if __name__ == '__main__':
    load_friends()
