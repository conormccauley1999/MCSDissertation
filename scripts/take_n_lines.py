import argparse


def take_n_lines(in_path, out_path, n):
    lines = []
    with open(in_path, 'rb') as f:
        for _ in range(n):
            lines.append(f.readline())
    with open(out_path, 'wb+') as f:
        f.writelines(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_path', help='path to json lined file')
    parser.add_argument('out_path', help='path to output file')
    parser.add_argument('-n', '--num_lines', type=int, default=100, help='number of lines to take')
    args = parser.parse_args()
    take_n_lines(args.in_path, args.out_path, args.num_lines)
