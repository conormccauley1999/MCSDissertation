from scipy.io import loadmat, savemat

MATRIX_PATH_FMT = './data/matrices/%s.mat'


def str_to_uid(string):
    # strip "profiles/" and convert to integer
    return int(string[16:])


def save_matrix(filename, matrix):
    path = MATRIX_PATH_FMT % filename
    savemat(path, mdict={'default': matrix})


def load_matrix(filename):
    path = MATRIX_PATH_FMT % filename
    return loadmat(path)['default']
