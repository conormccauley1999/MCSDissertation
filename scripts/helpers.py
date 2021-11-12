import numpy as np


def str_to_uid(string):
    # strip "profiles/" and convert to integer
    return int(string[16:])


def list_to_npa(arr, i=-1, dtype=int):
    if i != -1:
        arr = [x[i] for x in arr]
    return np.array(list(map(dtype, arr)))
