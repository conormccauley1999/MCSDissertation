import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import tensorflow_hub as hub
from bert import run_classifier
from bert import optimization
from bert import tokenization
from sklearn.model_selection import train_test_split

from utils.load_review_sentiments import *
from utils.review_constants import *


# https://github.com/google-research/bert/blob/master/predicting_movie_reviews_with_bert_on_tf_hub.ipynb
def bert_review_sentiments(filename, verbose=True):
    # load data and split into train/test sets
    data = load_review_sentiments(filename, verbose=verbose)
    train, test = train_test_split(data, test_size=0.5)
    # convert data to BERT input format
    to_input = lambda x: run_classifier.InputExample(
        guid=None, text_a=x['text'], text_b=None, label = x['polarity']
    )
    train_ies = train.apply(to_input, axis=1)
    test_ies = test.apply(to_input, axis=1)
    # create tokenizer and convert data to features
    tokenizer = create_tokenizer()
    max_seq_length = 128
    #train_features = run_classifier
    return


def create_tokenizer():
    with tf.Graph().as_default():
        module = hub.Module(MODEL_BERT_UNCASED)
        tokenization_info = module(signature='tokenization_info', as_dict=True)
        with tf.Session() as sess:
            vocab_file, do_lower_case = sess.run(
                tokenization_info['vocab_file'],
                tokenization_info['do_lower_case']
            )
    return
    return tokenization.FullTokenizer(
        vocab_file=vocab_file,
        do_lower_case=do_lower_case
    )


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
