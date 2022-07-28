# CSCI 323/700
# Summer 2022
# Assignment 4 - Empirical Performance of Search Structures
# Changli Zeng


import numpy as np
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import math


assn_num = 4


def build_chaining_hash(data):
    hash_table = [[] for _ in range(len(data))]
    for num in data:
        hash_key = num % len(data)
        hash_table[hash_key].append(num)
    return hash_table


def search_chaining_hash(table, num):
    if table[num % len(table)].index(num) >= 0:
        return True
    else:
        return False


# From https://www.geeksforgeeks.org/quadratic-probing-in-hashing/
def build_quad_hash(data):
    # create table
    hash_table = [[] for _ in range(len(data))]

    # Initializing the hash table
    for i in range(len(data)):
        hash_table[i] = -1

    for i in range(len(data)):
        # Computing the hash value
        hash_key = data[i] % len(hash_table)

        # Insert in the table if there
        # is no collision
        if hash_table[hash_key] == -1:
            hash_table[hash_key] = data[i]

        else:

            # If there is a collision
            # iterating through all
            # possible quadratic values
            for j in range(len(data)):

                # Computing the new hash value
                t = (hash_key + j * j) % len(hash_table)

                if hash_table[t] == -1:
                    # Break the loop after
                    # inserting the value
                    # in the table
                    hash_table[t] = data[i]
                    break
    return hash_table


def search_quad_hash(table, num):
    size = len(table)
    for i in range(size):
        if table[num % size] == num:
            return True
        else:
            for j in range(size):
                t = (num % size + j * j) % size
                if table[t] == num:
                    return True
        return False


# https://www.geeksforgeeks.org/double-hashing/
def build_double_hash(datas):
    size = len(datas)*10
    hash_table = [None for i in range(size)]

    for num in datas:
        hash1 = num % size
        if not hash_table[hash1]:  # no collision
            hash_table[hash1] = num
        else:  # use double-hashing
            hash2 = prime(num) - num % prime(num)
            inserted = False
            i = 1  # no need to check for i = 0, since collision already occurred
            while not inserted:
                if i > size:
                    print("cant find place to insert")
                    break
                hash_combo = (hash1 + hash2 * i) % size
                if not hash_table[hash_combo]:
                    hash_table[hash_combo] = num
                    inserted = True
                else:
                    i += 1
    return hash_table


def search_double_hash(table, num):
    size = len(table)
    hash1 = num % size
    if table[hash1] == num:
        return True
    else:
        hash2 = prime(num) - num % prime(num)
        i = 1
        while i <= size:
            hash_combo = (hash1 + hash2 * i) % size
            if table[hash_combo] == num:
                return True
            else:
                i += 1
    return False


# https://www.geeksforgeeks.org/cuckoo-hashing/
def build_cuckoo_hash(datas):
    size = len(datas)
    table_size = size*10
    num_tables = 2

    # init table
    hash_table = [None] * num_tables
    hash_table[0] = [-1] * table_size
    hash_table[1] = [-1] * table_size
    pos = [None] * num_tables

    for i in range(size):
        cuckoo_insert(datas[i], 0, 0, table_size, pos, hash_table)

    return hash_table


def cuckoo_insert(key, table_num, cnt, table_size, pos, hash_table):
    if cnt == table_size:
        print("unpositioned:", key)
        print("Cycle present. REHASH.")
        return

    ver = len(hash_table)
    for i in range(ver):
        pos[i] = my_hash(i + 1, key, table_size)
        if hash_table[i][pos[i]] == key:
            return

    if hash_table[table_num][pos[table_num]] != -1:  # if some thingelse if there
        dis = hash_table[table_num][pos[table_num]]
        hash_table[table_num][pos[table_num]] = key
        cuckoo_insert(dis, (table_num+1) % ver, cnt+1, table_size, pos, hash_table)
    else:
        hash_table[table_num][pos[table_num]] = key


def search_cuckoo_hash(hash_table, key):
    ver = len(hash_table)
    for i in range(ver):
        pos = my_hash(i + 1, key, len(hash_table[0]))
        if hash_table[i][pos] == key:
            return i, pos


def my_hash(func_num, key, size):
    if func_num == 1:
        return key % size
    else:
        return int(key / size) % size


def prime(n):
    # All prime numbers are odd except two
    if n & 1:
        n -= 2
    else:
        n -= 1

    i, j = 0, 3

    for i in range(n, 2, -2):

        if i % 2 == 0:
            continue

        while j <= math.floor(math.sqrt(i)) + 1:
            if i % j == 0:
                break
            j += 2

        if j > math.floor(math.sqrt(i)):
            return i

    # It will only be executed when n is 3
    return 2


def pseudo_random_list(n):
    data = [0]
    for i in range(1, n):
        data.append(data[i-1]+random.randint(1, 10))
    random.shuffle(data)
    return data


# get random subset of size items from data list
def get_random_sublist(data, size):
    return [data[random.randint(0, len(data)-1)] for i in range(size)]


def plot_time(dict_algos, sizes, algos, trials, name):
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
    plt.savefig("Assignment" + str(name) + "_output.png")
    plt.show()


def main():
    hash_chaining = None
    hash_quadratic = None
    hash_double = None
    hash_cuckoo = None

    sizes = [1000 * i for i in range(1, 11)]
    trials = 10
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

            for i in range(len(search_functions)):
                search = search_functions[i]
                table = hash_tables[i]
                start_time = time.time()
                for item in sublist:
                    search(table, item)
                    net_time = end_time - start_time
                    dict_search[search.__name__][size] += 1000 * net_time

    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_build).T
    print(df)
    ds = pd.DataFrame.from_dict(dict_search).T
    print(ds)
    plot_time(dict_build, sizes, build_functions, trials, "4a")
    plot_time(dict_search, sizes, search_functions, trials, "4b")


if __name__ == "__main__":
    main()

