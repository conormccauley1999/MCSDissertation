def take_n_lines(filename, n):
    lines = []
    with open(f'./data/{filename}.jl', 'rb') as f:
        for _ in range(n):
            lines.append(f.readline())
    with open(f'./data/{filename}_{n}.jl', 'wb+') as f:
        f.writelines(lines)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='name of json lined file in data directory')
    parser.add_argument('-n', '--num_lines', type=int, default=100, help='number of lines to take')
    args = parser.parse_args()
    take_n_lines(args.filename, args.num_lines)
