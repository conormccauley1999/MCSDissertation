# imports
from csv import reader as csv_reader, writer as csv_writer
from time import time

from review_constants import *


def write_review_buffer(review_buffer, cur_write_page, verbose=True):
    # write review buffer to file
    with open(PATH_REVIEW_REDIST % cur_write_page, 'w+', encoding='utf-8', newline='') as f:
        writer = csv_writer(f, delimiter=',')
        writer.writerows(review_buffer)
    # logging
    if verbose:
        print(f'Wrote {len(review_buffer)} reviews to page {cur_write_page}')


def redistribute_review_data(page_size=400000, verbose=True):
    # logging
    if verbose: print(f'Redistributing review data')
    t = time()
    # stored data
    review_buffer = []
    buffer_length = 0
    cur_write_page = 1
    # iterate over review pages
    for page_num in range(1, NUM_REVIEW_PAGES + 1):
        # load non-text review data
        with open(PATH_REVIEW_COMB % page_num, 'r', encoding='utf-8') as f:
            reader = csv_reader(f, delimiter=',')
            for review  in reader:
                # if buffer is full then write the buffer to a file
                if buffer_length == page_size:
                    write_review_buffer(review_buffer, cur_write_page, verbose=verbose)
                    review_buffer = []
                    buffer_length = 0
                    cur_write_page += 1
                review_buffer.append(review)
                buffer_length += 1
    # write the remaining buffer to a file
    if buffer_length > 0:
        write_review_buffer(review_buffer, cur_write_page, verbose=verbose)
    # logging
    if verbose: print(f'Redistributed review data in {int(time() - t)} seconds')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--page_size', type=int, default=400000, help='number of reviews on each new page')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    redistribute_review_data(
        page_size=args.page_size,
        verbose=args.verbose
    )
