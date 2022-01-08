#import tensorflow as tf
#import tensorflow_hub as hub
#from bert import run_classifier
#from bert import optimization
#from bert import tokenization
from sklearn.model_selection import train_test_split

from utils.load_review_sentiments import *
from utils.review_constants import *

# https://github.com/google-research/bert/blob/master/predicting_movie_reviews_with_bert_on_tf_hub.ipynb
def bert_review_sentiments(filename, verbose=True):
    data = load_review_sentiments(filename, verbose=verbose)
    train, test = train_test_split(data, test_size=0.5)
    return


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='name of review sentiments file')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    bert_review_sentiments(
        args.filename,
        verbose=args.verbose
    )
