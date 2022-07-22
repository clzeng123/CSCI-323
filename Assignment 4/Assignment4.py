# CSCI 323/700
# Summer 2022
# Assignment 4 - Empirical Performance of Search Structures
# Changli Zeng


import copy
import numpy as np
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

assn_num = 3


def build_chaining_hash(data):
    pass


def build_quad_hash(data):
    pass


def build_double_hash(data):
    pass


def build_cuckoo_hash(data):
    pass


def search_chaining_hash(data):
    pass


def search_quad_hash(data):
    pass


def search_double_hash(data):
    pass


def search_cuckoo_hash(data):
    pass


def pseudo_random_list(n):
    data = [0]
    for i in range(1, n):
        data.append(data[i-1]+random.randint(1, 10))
    random.shuffle(data)
    return data


# get random subset of size items from data list
def get_random_sublist(data, size):
    return [data[random.randint(0, len(data)-1)] for i in range(size)]


def plot_time(dict_algos, sizes, algos, trials):
    alg_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for alg in algos:
        alg_num += 1
        d = dict_algos[alg.__name__]
        x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.1, alpha=0.75, label=alg.__name__)
    plt.legend()
    plt.title("Run time of Algorithms")
    plt.xlabel("Size of data")
    plt.ylabel("Time for " + str(trials) + " trials (ms)")
    plt.savefig("Assignment" + str(assn_num) + "_output.png")
    plt.show()


def main():
    hash_chaining = None
    hash_quadratic = None
    hash_double = None
    hash_cuckoo = None

    sizes = [100 * i for i in range(1, 11)]
    trials = 1
    build_functions = [build_chaining_hash, build_quad_hash, build_double_hash, build_cuckoo_hash]
    search_functions = [search_chaining_hash, search_quad_hash, search_double_hash, search_cuckoo_hash]
    dict_build = {}
    dict_search = {}
    for build in build_functions:
        dict_build[build.__name__] = {}
    for search in search_functions:
        dict_search[search.__name__] = {}
    for size in sizes:
        for build in build_functions:
            dict_build[build.__name__][size] = 0
        for search in search_functions:
            dict_search[search.__name__][size] = 0
        for trial in range(1, trials + 1):
            data = pseudo_random_list(size)
            sublist = get_random_sublist(data, 100)
            hash_tables = []
            for build in build_functions:
                start_time = time.time()
                hash_tables.append(build(data))
                end_time = time.time()
                net_time = end_time - start_time
                dict_build[build.__name__][size] += 1000 * net_time

            for i in len(search_functions):
                search = search_functions[i]
                table = hash_tables[i]
                start_time = time.time()
                for item in sublist:
                    search(table, item)
                end_time = time.time()
                net_time = end_time - start_time
                dict_search[search.__name__][size] += 1000 * net_time

    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_build).T
    print(df)
    plot_time(dict_build, sizes, build_functions, trials)

    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_search).T
    print(df)
    plot_time(dict_search, sizes, search_functions, trials)


if __name__ == "__main__":
    main()

