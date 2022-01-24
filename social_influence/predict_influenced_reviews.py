import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from csv import reader as csv_reader
from random import shuffle
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import PolynomialFeatures
from time import time

warnings.filterwarnings('ignore')

PATH_FEATURES = './data/prepared/social_influence/influence_features.csv'


def predict_influenced_reviews(num_samples=10000, verbose=True):
    X, Y = load_influence_features(num_samples=num_samples, verbose=verbose)
    # most frequent baseline
    bl_freq = DummyClassifier(strategy='most_frequent')
    bl_freq_scores = cross_val_score(bl_freq, X, Y, cv=5, scoring='accuracy')
    bl_freq_mean, bl_freq_std = bl_freq_scores.mean(), bl_freq_scores.std()
    print('bl_freq >> mean = %.3f, std = %.3f' % (bl_freq_mean, bl_freq_std))
    # random baseline
    bl_rand = DummyClassifier(strategy='uniform')
    bl_rand_scores = cross_val_score(bl_rand, X, Y, cv=5, scoring='accuracy')
    bl_rand_mean, bl_rand_std = bl_rand_scores.mean(), bl_rand_scores.std()
    print('bl_rand >> mean = %.3f, std = %.3f' % (bl_rand_mean, bl_rand_std))
    # hyperparams
    degrees = [1, 2, 3]
    Cs = [0.00001, 0.001, 0.1, 10, 1000, 100000]
    means, stds = [], []
    for degree in degrees:
        X_poly = PolynomialFeatures(degree).fit_transform(X)
        print('\ndegree = %d:' % degree)
        means_, stds_ = [], []
        for C in Cs:
            model = LogisticRegression(C=C, penalty='l2', solver='lbfgs').fit(X_poly, Y)
            scores = cross_val_score(model, X_poly, Y, cv=5, scoring='accuracy')
            means_.append(scores.mean())
            stds_.append(scores.std())
            print('C = %.5f >> mean = %.3f, std = %.3f' % (C, scores.mean(), scores.std()))
        means.append(means_)
        stds.append(stds_)
    blf_means = [bl_freq_mean] * len(Cs)
    blf_stds = [bl_freq_std] * len(Cs)
    blr_means = [bl_rand_mean] * len(Cs)
    blr_stds = [bl_rand_std] * len(Cs)
    # plotting
    plt.errorbar(Cs, blf_means, yerr=blf_stds)
    plt.errorbar(Cs, blr_means, yerr=blr_stds)
    plt.errorbar(Cs, means[0], yerr=stds[0])
    plt.errorbar(Cs, means[1], yerr=stds[1])
    plt.errorbar(Cs, means[2], yerr=stds[2])
    plt.xlabel('C')
    plt.ylabel('Mean accuracy score')
    plt.xscale('log')
    plt.ylim(0, 1)
    plt.legend(['Baseline (freq)', 'Baseline (random)', 'Degree = 1', 'Degree = 2', 'Degree = 3'])
    plt.show()


def load_influence_features(num_samples=10000, verbose=True):
    if verbose: print('Loading influence features')
    t = time()
    data_pos = []
    data_neg = []
    with open(PATH_FEATURES, 'r', newline='') as f:
        reader = csv_reader(f, delimiter=',')
        for row in reader:
            vals = list(map(int, row))
            if vals[-1] == 0: vals[-1] = -1 # replace 0 with -1
            if vals[-1] == 1: data_pos.append(vals)
            else: data_neg.append(vals)
    if verbose: print(f'Loaded influence features in {int(time() - t)} seconds')
    if verbose: print('Sampling influence features')
    t = time()
    shuffle(data_pos)
    shuffle(data_neg)
    data_pos = data_pos[:num_samples]
    data_neg = data_neg[:num_samples]
    data = np.array(data_pos + data_neg)
    X, Y = data[:,:-1], data[:,-1:].flatten()
    if verbose: print(f'Sampled influence features in {int(time() - t)} seconds')
    return X, Y


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_samples', type=int, default=10000, help='number of positive and negative samples to select')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    predict_influenced_reviews(
        num_samples=args.num_samples,
        verbose=args.verbose
    )
