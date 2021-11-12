from scipy.io import loadmat, savemat

MATRIX_PATH_FMT = './data/matrices/%s.mat'


def str_to_uid(string):
    # strip "profiles/" and convert to integer
    return int(string[16:])


def save_matrix(filename, key, matrix):
    path = MATRIX_PATH_FMT % filename
    savemat(path, mdict={key: matrix})


def load_matrix(filename, key):
    path = MATRIX_PATH_FMT % filename
    return loadmat(path)[key]
