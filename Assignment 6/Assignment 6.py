# CSCI 323/700
# Summer 2022
# Assignment 6 - Palindromic Substrings and Subsequences
# Changli Zeng


import random
import math
import time
import pandas as pda
import matplotlib.pyplot as plt
import copy
import numpy as np

assn_num = 6


def native_search(text, pattern, verbose=True):
    return text.find(pattern)


# from https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/
def brute_force(text, pattern, verbose=True):
    m = len(pattern)
    n = len(text)
    for i in range(n - m + 1):
        j = 0
        while j < m:
            if verbose:
                print('m', m, 'n', n, 'i', i, 'j', j)
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return i
    return -1


#from https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/
def rabin_karp(text, pattern, verbose=True):
    m = len(pattern)
    n = len(text)
    j = 0
    p = 0  # hash value for pattern
    t = 0  # hash value for txt
    h = 1
    q = 101  # modulo
    d = 256  # num of char
    # The value of h would be "pow(d, M-1)%q"
    for i in range(m - 1):
        h = (h * d) % q
    # Calculate the hash value of pattern and first window of text
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    # Slide the pattern over text one by one
    for i in range(n - m + 1):
        # Check the hash values of current window of text and pattern if the hash values match then only check
        # for characters one by one
        if p == t:
            if verbose:
                print('p', p, 't', t, 'i', i, 'j', j, 'm', m, 'n', n)
            # Check for characters one by one
            for j in range(m):
                if text[i + j] != pattern[j]:
                    break
                else:
                    j += 1
            # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
            if j == m:
                return i
        # Calculate hash value for next window of text: Remove leading digit, add trailing digit
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            # We might get negative values of t, converting it to positive
            if t < 0:
                t = t + q
    return -1




def plot_time(dict_algs, sizes, algs, trails):
    alg_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for algs in algs:
        alg_num += 1
        d = dict_algs[algs.__name__]
        x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=algs.__name__)
    plt.legend()
    plt.title("Run time of search algorithms")
    plt.xlabel("Size of Data")
    plt.ylabel("Time for " + str(trails) + "Trails" "(ms)")
    plt.savefig("Assignment" + str(assn_num) + ".png")
    plt.show()






def run_trials():
    sizes = [10 * i for i in range(1, 2)]
    trials = 1
    algs = [native_search, brute_force, rabin_karp]
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            for alg in algs:
                start_time = time.time()
                idx = alg(text='', pattern='', verbose=True)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    pda.set_option("display.max_rows", 500)
    pda.set_option("display.max_columns", 500)
    pda.set_option("display.width", 1000)
    df = pda.DataFrame.from_dict(dict_algs).T
    print(df)
    plot_time(dict_algs, sizes, algs, trials)


def main():
    # run_trials()
    text = 'loopsjdbeiwm'
    pattern = 'jdb'
    idx1 = native_search(text, pattern, True)
    idx2 = brute_force(text, pattern, True)
    idx3 = rabin_karp(text, pattern, True)
    print(idx1, idx2, idx3)


if __name__ == "__main__":
    main()