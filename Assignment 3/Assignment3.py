# CSCI 323/700
# Summer 2022
# Assignment 3 - Empirical Performance of Matrix Multiplication
# Changli Zeng

import numpy as np
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

assn_num = 3


def random_matrix(mn, mx, rows, cols):
    return [[random.randint(mn, mx) for col in range(0, cols)] for row in range(0, rows)]


def print_matrix(matrix):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])for row in matrix]) + "\n")


def native_mult(m1, m2):
    return np.dot(m1, m2)


def simple_mult(m1, m2):
    rows = len(m1)
    cols = len(m2[0])
    m3 = [[0 for x in range(cols)]for y in range(rows)]
    for i in range(rows):
        for j in range(cols):
            m3[i][j] = 0
            for x in range(cols):
                m3[i][j] += m1[i][x] * m2[x][j]
    return m3


def strassen_mult(m1, m2):
    return native_mult(m1, m2)


def plot_time(dict_algs, sizes, algs, trials):
    alg_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for alg in algs:
        alg_num += 1
        d = dict_algs[algs.__name__]
        x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=algs.__name__)
    plt.legend()
    plt.title("Run time of Algorithms")
    plt.xlabel("Size of data")
    plt.ylabel("Time for " + str(trials) + "trials (ms)")
    plt.savefig("Assignment3" + str(assn_num) + ".png")
    plt.show()


def main():
    sizes = [10 * i for i in range(1, 11)]
    trials = 1
    algs = [native_mult, simple_mult, strassen_mult]
    dict_algs= {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            m1 = random_matrix(-1, 1, size, size)
            m2 = random_matrix(-1, 1, size, size)
            print_matrix(m1)
            print_matrix(m2)
            for alg in algs:
                start_time = time.time()
                m3 = alg(m1, m2)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
                print_matrix(m3)
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_algs).T
    print(df)
    plot_time(dict_algs, sizes, algs, trials)


if __name__ == "__main__":
    main()

