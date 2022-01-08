# imports
from csv import reader as csv_reader, writer as csv_writer
from spacy_langdetect import LanguageDetector
from time import time
import spacy

from utils.review_constants import *

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe(LanguageDetector(), name='ld', last=True)


def review_text_valid(text):
    if text == REVIEW_HIDDEN:
        return False
    if not len(text):
        return False
    lang = nlp(text)._.language
    if lang['language'] != 'en':
        return False
    return True


def prepare_review_sentiments(filename, num_samples=5000, start_page=1, end_page=NUM_REVIEW_PAGES, verbose=True):
    # logging
    if verbose:
        print(f'Loading {num_samples} review sentiments from pages {start_page}-{end_page}')
    t = time()
    # stored data
    data = []
    num_pos = 0
    num_neg = 0
    # iterate over review pages
    for page_num in range(start_page, end_page + 1):
        with open(PATH_REVIEW_COMB % page_num, 'r', encoding='utf-8') as f:
            reader = csv_reader(f, delimiter=',')
            for review in reader:
                # break if all samples have been found
                if num_pos == num_samples and num_neg == num_samples: break
                # extract data
                polarity = int(review[ReviewCols.POLARITY])
                text = review[ReviewCols.TEXT]
                # skip if we don't need more samples for this polarity
                if polarity == 1 and num_pos >= num_samples:
                    continue
                if polarity == 0 and num_neg >= num_samples:
                    continue
                # skip if the review text is invalid (empty/hidden/non-english/etc.)
                if not review_text_valid(text):
                    continue
                # update count and add to data
                if polarity == 1: num_pos += 1
                else: num_neg += 1
                data.append([text, polarity])
        # logging
        if verbose:
            print(f'Loaded review sentiments from page {page_num} ({num_pos}, {num_neg})')
        # break if all samples have been found
        if num_pos == num_samples and num_neg == num_samples: break
    # save loaded data
    with open(PATH_REVIEW_SENTS % filename, 'w+', newline='', encoding='utf-8') as f:
        writer = csv_writer(f, delimiter=',')
        writer.writerows(data)
    # logging
    if verbose: print(f'Loaded and prepared review sentiments in {int(time() - t)} seconds')
    return data


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='name of review sentiments file')
    parser.add_argument('-s', '--start_page', type=int, default=1, help='review page to start at')
    parser.add_argument('-e', '--end_page', type=int, default=NUM_REVIEW_PAGES, help='review page to end at (inclusive)')
    parser.add_argument('-n', '--num_samples', type=int, default=5000, help='number of samples each for pos/neg reviews')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    prepare_review_sentiments(
        args.filename,
        num_samples=args.num_samples,
        start_page=args.start_page,
        end_page=args.end_page,
        verbose=args.verbose
    )
