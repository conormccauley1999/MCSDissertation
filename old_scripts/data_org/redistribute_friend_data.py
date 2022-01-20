from csv import writer as csv_writer
from json_lines import reader as jl_reader
from time import time

IN_FILE = './data/raw/friends/friends.jl'
OUT_FILE = './data/raw/friends/redist/page_%d.csv'


def profile_to_uid(profile):
    return int(profile[16:])


def write_buffer(buffer, cur_write_page, verbose=True):
    with open(OUT_FILE % cur_write_page, 'w+', newline='') as f:
        writer = csv_writer(f, delimiter=',')
        writer.writerows(buffer)
    if verbose:
        print(f'Wrote {len(buffer)} items to page {cur_write_page}')


def redistribute_friend_data(page_size, verbose=True):
    if verbose: print(f'Redistributing friend data')
    t = time()
    buffer = []
    buffer_len = 0
    cur_write_page = 1
    with open(IN_FILE, 'rb') as f:
        for item in jl_reader(f):
            if buffer_len == page_size:
                write_buffer(buffer, cur_write_page)
                buffer = []
                buffer_len = 0
                cur_write_page += 1
            data = [profile_to_uid(item['steamid'])]
            for friend in item['ids']:
                data.append(profile_to_uid(friend))
            buffer.append(data)
            buffer_len += 1
    if buffer_len > 0:
        write_buffer(buffer, cur_write_page)
    if verbose: print(f'Redistributed friend data in {int(time() - t)} seconds')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--page_size', type=int, default=300000, help='number of reviews on each new page')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    redistribute_friend_data(
        page_size=args.page_size,
        verbose=args.verbose
    )
