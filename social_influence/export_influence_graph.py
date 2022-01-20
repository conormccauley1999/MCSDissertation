import networkx as nx
from collections import defaultdict
from csv import reader as csv_reader
from time import time

PATH_INFLUENCE = './data/prepared/social_influence/influence.csv'
PATH_GRAPHML = './data/prepared/social_influence/influence_graph.graphml'
PATH_GRAPHML_GID = './data/prepared/social_influence/influence_graph_%d.graphml'


def export_influence_graph(game_id=None, verbose=True):
    graph = load_influence_graph(game_id=game_id, verbose=verbose)
    if verbose: print('Exporting influence graph')
    t = time()
    path = PATH_GRAPHML
    if game_id is not None:
        path = PATH_GRAPHML_GID % game_id
    nx.write_graphml(graph, path)
    if verbose: print(f'Exported influence graph in {int(time() - t)} seconds')


def load_influence_graph(game_id=None, verbose=True):
    if verbose: print('Loading influence graph')
    t = time()
    graph = nx.MultiDiGraph()
    weights = defaultdict(lambda: defaultdict(int))
    with open(PATH_INFLUENCE, 'r', newline='') as f:
        reader = csv_reader(f, delimiter=',')
        for row in reader:
            u = int(row[0])
            v = int(row[1])
            w = int(row[2])
            if game_id is None:
                weights[u][v] += 1
            elif w == game_id:
                weights[u][v] = 1
    edge_id = 0
    for u, vs in weights.items():
        for v, w in vs.items():
            if game_id is None:
                graph.add_edge(u, v, weight=w, key=edge_id)
            else:
                graph.add_edge(u, v, key=edge_id)
            edge_id += 1
    if verbose: print(f'Loaded influence graph in {int(time() - t)} seconds')
    return graph


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--game_id', default=None, type=int, help='only include reviews for a specific game')
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress')
    args = parser.parse_args()
    export_influence_graph(
        game_id=args.game_id,
        verbose=args.verbose
    )
