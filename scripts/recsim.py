import numpy as np
from math import ceil
from matplotlib import pyplot as plt
from random import shuffle

from utils import load_matrix


class RecSim:
    def __init__(self, M_ratings, M_clusters=None, n_clusters=5, n_sims=0, P_min=0.7, A0=10, G=5):
        self.M_ratings = M_ratings
        self.M_clusters = M_clusters
        self.is_baseline = (M_clusters is None)
        self.n_clusters = n_clusters
        self.n_users, self.n_games = M_ratings.shape
        self.n_sims = n_sims if n_sims else self.n_games
        self.A0 = A0
        self.G = G
        self.P_min = P_min
        self.results = []
    
    def simulate(self):
        # generate a list of games to run simulations for
        column_indices = list(range(self.n_games))
        shuffle(column_indices)
        column_indices = column_indices[:self.n_sims]
        # run simulations
        x = 0
        for column_index in column_indices:
            column = self.M_ratings.getcol(column_index)
            # get a list of users' clusters and their ratings for the game
            row_indices = column.nonzero()[0]
            user_ratings = []
            for row_index in row_indices:
                rating = column[row_index, 0]
                cluster = self.__get_user_cluster(row_index)
                user_ratings.append([rating, cluster])
            # simulate and add to results
            n_ratings = len(user_ratings)
            n_positive = self.__get_n_positive(user_ratings)
            n_reached = self.__simulate_game(user_ratings)
            pc_positive = n_positive / n_ratings
            pc_reached = n_reached / n_positive
            self.results.append((pc_positive, pc_reached))
            x += 1
            if (x % 100) == 0: print(x, self.n_games)
    
    def __simulate_game(self, ratings):
        n_reached = 0
        A = self.A0
        pc_positive = None
        while ratings:
            A_actual = min(A, len(ratings))
            P, ratings, pc_positive = self.__simulate_game_iteration(ratings, pc_positive, A)
            n_reached += int(A_actual * P)
            if P < self.P_min:
                break
            A *= self.G
        return n_reached
    
    def __simulate_game_iteration(self, ratings, pc_positive, A):
        if self.is_baseline:
            return self.__simulate_game_iteration_bl(ratings, A)
        else:
            return self.__simulate_game_iteration_actual(ratings, pc_positive, A)
    
    def __simulate_game_iteration_bl(self, ratings, A):
        shuffle(ratings)
        ratings_cur, ratings_rem = ratings[:A], ratings[A:]
        n_positive = self.__get_n_positive(ratings_cur)
        P = n_positive / len(ratings_cur)
        return P, ratings_rem, None
    
    def __simulate_game_iteration_actual(self, ratings, pc_positive, A):
        ratings_cur, ratings_rem = [], []
        shuffle(ratings)
        if not pc_positive:
            ratings_cur, ratings_rem = ratings[:A], ratings[A:]
        else:
            # calculate how much of each cluster we need
            count_clusters = [0] * self.n_clusters
            for _, cluster in ratings:
                count_clusters[cluster] += 1
            need_total = A
            need_clusters = [0] * self.n_clusters
            for _, cluster in pc_positive:
                take_cluster = max(0, min(count_clusters[cluster], need_total))
                need_clusters[cluster] = take_cluster
                need_total -= take_cluster
            # take needed user ratings
            for rating in ratings:
                _, cluster = rating
                if need_clusters[cluster] > 0:
                    ratings_cur.append(rating)
                    need_clusters[cluster] -= 1
                else:
                    ratings_rem.append(rating)
        n_positive = self.__get_n_positive(ratings_cur)
        P = n_positive / len(ratings_cur)
        return P, ratings_rem, self.__get_pc_positive_per_cluster(ratings_cur)
    
    def __get_user_cluster(self, user):
        return 0 if self.is_baseline else self.M_clusters[user, 1]

    def __get_n_positive(self, ratings):
        return sum(1 if x[0] == 1 else 0 for x in ratings)
    
    def __get_pc_positive_per_cluster(self, ratings):
        n_positive = [0] * self.n_clusters
        n_negative = [0] * self.n_clusters
        for polarity, cluster in ratings:
            if polarity == 1: n_positive[cluster] += 1
            else: n_negative[cluster] += 1
        pc_positive = []
        for i in range(self.n_clusters):
            pc_positive.append([
                n_positive[i] / (n_positive[i] + n_negative[i] + 1),
                i
            ])
        return sorted(pc_positive, reverse=True)

    def display(self, step=0.05):
        x, y, e = self.__convert_results(step)
        plt.bar(
            x, y, width=(step * 0.8), yerr=e, color='tab:blue',
            error_kw={'capsize': 3, 'elinewidth': 1, 'ecolor': 'tab:red'}
        )
        plt.xlabel('Percent positive ratings')
        plt.ylabel('Percent audience reached')
        plt.xticks(x[::2])
        plt.xlim([-step, 1 + step])
        plt.ylim([0, 1 + step])
        plt.axvline(self.P_min, color='black', alpha=0.7, linewidth=1, linestyle='--')
        plt.show()

    def __convert_results(self, step):
        n_bins = int(ceil(1 / step)) + 1
        bins = []
        for _ in range(n_bins): bins.append([])
        for x, y in self.results:
            i = min(int(round(x / step)), n_bins)
            bins[i].append(y)
        for i in range(n_bins):
            if not len(bins[i]):
                bins[i] = [0.01]
        x = np.array([
            round(i * step, 2)
            for i in range(n_bins)
        ])
        y = np.array(list(map(np.mean, bins)))
        e = np.array(list(map(np.var, bins)))
        return x, y, e


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('ratings_file', help='name of ratings matrix file')
    parser.add_argument('-c', '--clusters_file', type=str, default=None, help='name of clusters matrix file')
    parser.add_argument('-n', '--n_sims', type=int, default=0, help='number of simulations to run (0 = all games)')
    parser.add_argument('-l', '--n_clusters', type=int, default=5, help='number of clusters users have been grouped into')
    parser.add_argument('-p', '--p_min', type=float, default=0.7, help='minimum proportion of audience needed to continue')
    args = parser.parse_args()
    M_ratings = load_matrix(args.ratings_file)
    M_clusters = None
    if args.clusters_file:
        M_clusters = load_matrix(args.clusters_file)
    rs = RecSim(
        M_ratings,
        M_clusters=M_clusters,
        n_clusters=args.n_clusters,
        n_sims=args.n_sims,
        P_min=args.p_min
    )
    rs.simulate()
    rs.display()
