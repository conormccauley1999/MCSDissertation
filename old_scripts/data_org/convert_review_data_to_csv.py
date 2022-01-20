# imports
from csv import writer as csv_writer
from json_lines import reader as jl_reader
from time import time

from review_constants import *

# convert a Steam user ID to an integer
uid_to_int = lambda uid: int(uid[16:])


def convert_review_data_to_csv(start_page=1, end_page=NUM_REVIEW_PAGES, verbose=True):
    # logging
    if verbose: print(f'Converting review pages {start_page}-{end_page}')
    t = time()
    # iterate over review pages
    for page_num in range(start_page, end_page + 1):
        # stored review data
        review_data = []
        # load non-text review data
        with open(PATH_REVIEW_NTXT % page_num, 'rb') as f:
            for item in jl_reader(f):
                user_id = uid_to_int(item['steamid'])
                for review in item['reviews']:
                    review_data.append([
                        user_id,
                        int(review['appid']),
                        int(review['voted_up']),
                        int(review['tstamp_created']),
                        float(review['playtime_forever']),
                        int(review['votes_up']),
                        int(review['votes_funny']),
                        ''
                    ])
        # load review text
        with open(PATH_REVIEW_TXT % page_num, 'rb') as f:
            i = 0
            for item in jl_reader(f):
                user_id = uid_to_int(item['steamid'])
                for review in item['reviews']:
                    text = review['text']
                    review_data[i][-1] = text
                    i += 1
        # save review page data as csv
        with open(PATH_REVIEW_COMB % page_num, 'w+', encoding='utf-8', newline='') as f:
            writer = csv_writer(f, delimiter=',')
            writer.writerows(review_data)
        # logging
        if verbose: print(f'Converted page {page_num}')
    # logging
    if verbose: print(f'Converted review pages in {int(time() - t)} seconds')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_page', type=int, default=1, help='review page to start at')
    parser.add_argument('-e', '--end_page', type=int, default=NUM_REVIEW_PAGES, help='review page to end at (inclusive)')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    convert_review_data_to_csv(
        start_page=args.start_page,
        end_page=args.end_page,
        verbose=args.verbose
    )
