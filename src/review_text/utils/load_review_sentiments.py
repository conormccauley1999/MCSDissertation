# imports
from csv import reader as csv_reader
from time import time
import pandas as pd

from utils.review_constants import *


def load_review_sentiments(filename, verbose=True):
    # logging
    if verbose: print(f"Loading review sentiments from '{filename}'")
    t = time()
    # stored data
    data = {
        'text': [],
        'polarity': []
    }
    # iterate over csv rows
    with open(PATH_REVIEW_SENTS % filename, 'r', encoding='utf-8') as f:
        reader = csv_reader(f, delimiter=',')
        for review in reader:
            text = review[0]
            polarity = int(review[1])
            data['text'].append(text)
            data['polarity'].append(polarity)
    # logging
    if verbose: print(f'Loaded review sentiments in {int(time() - t)} seconds')
    # convert and randomise data
    return pd.DataFrame.from_dict(data).sample(frac=1).reset_index(drop=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='name of review sentiments file')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    load_review_sentiments(
        filename=args.filename,
        verbose=args.verbose
    )
