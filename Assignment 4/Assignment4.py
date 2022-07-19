# CSCI 323/700
# Summer 2022
# Assignment 4 - Empirical Performance of Search Structures"
# Changli Zeng


import math
import random
import time
import pandas as pd
import matplotlib.pyplot as plt


assn_num = 4


def random_list(range_max, size, unique):
    numbers = []
    i = 0
    while i < size:
        rnd = random.randint(1, range_max)
        if unique and rnd in numbers:
            continue
        else:
            numbers.append(rnd)
            i += 1

    return numbers


def plot_time(dict_algs, sizes, algs, trials):
    alg_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for algs in algs:
        alg_num += 1
        d = dict_algs[algs.__name__]
        x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=algs.__name__)
    plt.legend()
    plt.title("Run time for Search Structures")
    plt.xlabel("Size of data")
    plt.ylabel("Time for " + str(trials) + "trials (ms)")
    plt.savefig("Assignment" + str(assn_num) + ".png")
    plt.show()

    def main():
        sizes = [100 * i for i in range(1, 11)]
        search_size = 100
        trials = 1
        dict_structures = []
        dict_structures= {}
        for alg in algs:
            dict_algs[alg.__name__] = {}
        for size in sizes:
            for alg in algs:
                dict_algs[alg.__name__][size] = 0
            for trial in range(1, trials + 1):
                m1 = all_ones_matrix(-1, 1, size, size)
                m2 = all_ones_matrix(-1, 1, size, size)
                # m1 = random_matrix(-1, 1, size, size)
                # m2 = random_matrix(-1, 1, size, size)
                for alg in algs:
                    start_time = time.time()
                    m3 = alg(m1, m2)
                    end_time = time.time()
                    net_time = end_time - start_time
                    dict_algs[alg.__name__][size] += 1000 * net_time
        pd.set_option("display.max_rows", 500)
        pd.set_option("display.max_columns", 500)
        pd.set_option("display.width", 1000)
        df = pd.DataFrame.from_dict(dict_searches).T
        print(df)
        plot_time(dict_algs, sizes, algs, trials)


if __name__ == "__main__":
    main()