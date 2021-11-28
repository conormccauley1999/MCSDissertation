from csv import writer
from scipy.io import loadmat, savemat

MATRIX_PATH_FMT = './data/matrices/%s.mat'
EXTRAS_PATH_FMT = './data/csv/%s_%s.csv'


def str_to_uid(string):
    # strip "profiles/" and convert to integer
    return int(string[16:])


def save_matrix(filename, matrix):
    path = MATRIX_PATH_FMT % filename
    savemat(path, mdict={'default': matrix})


def load_matrix(filename):
    path = MATRIX_PATH_FMT % filename
    return loadmat(path)['default']


def save_extras(filename, extras):
    for key, data in extras.items():
        path = EXTRAS_PATH_FMT % (filename, key)
        with open(path, 'w+', newline='') as f:
            writer(f, delimiter=',').writerows(data)
