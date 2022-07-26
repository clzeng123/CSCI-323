import numpy as np
import random
import time
import pandas as pd
import matplotlib.pyplot as plt


def pseudo_random_list(n):
    data = [0]
    for i in range(1, n):
        data.append(data[i-1]+random.randint(1, 10))
    random.shuffle(data)
    return data


# From https://blog.chapagain.com.np/hash-table-implementation-in-python-data-structures-algorithms/
def build_chaining_hash(data):
    hash_table = [[] for _ in range(len(data))]
    for num in data:
        hash_key = num % len(data)
        hash_table[hash_key].append(num)
    return hash_table


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


def build_double_hash(data):
    hash_table = [[] for _ in range(len(data))]
    for i in range(len(data)):
        hash_key = data[i] % len(hash_table)
        if hash_table[hash_key] is None:
            hash_table[hash_key] = data[i]
        else:
            new_hashkey = hash_key
            while hash_table[new_hashkey] is not None:
                steps = double_hash_value - (data[i] % double_hash_value)
                new_hashkey = (new_hashkey + steps) % len(hash_table)  ## problem 1 is here
            hash_table[new_hashkey] = data[i]
        return hash_table


def build_cuckoo_hash(data):
    pass


def main():
    #sizes = [10 * i for i in range(1, 11)]
    #arr = [50, 700, 76,85, 92, 73, 101]
    #table = build_quad_hash(arr)
    #print(table)

    #data = pseudo_random_list(20)
    #print(data)
    #table = build_quad_hash(data)
    #print(table)
    #pseudo_random_list
    #print(pseudo_random_list(arr))
    #data = pseudo_random_list(5)
    #table = build_chaining_hash(data)
    #print(table)


if __name__ == "__main__":
    main()
