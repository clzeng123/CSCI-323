# CSCI 323/700
# Summer 2022
# Assignment 6 - Sub-String Search Algorithms
# Changli Zeng


import re
import texttable
import time
import time
import pandas as pd
import matplotlib.pyplot as plt


assn_num = 6


def native_search(text, pattern):
    return text.find(pattern)


# from https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/
def brute_force_search(text, pattern):
    m = len(pattern)
    n = len(text)
    for i in range(n - m + 1):
        j = 0
        while j < m:
            # if verbose:
            #     print('m', m, 'n', n, 'i', i, 'j', j)
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return i
    return -1


#from https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/
def rabin_karp_search(text, pattern):
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


#from https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
def knuth_morris_pratt_search(text, pattern):
    m = len(pattern)
    n = len(text)
    # create lps[] that will hold the longest prefix suffix
    # values for pattern
    lps = [0] * m
    j = 0  # index for pat[]

    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pattern, m, lps)

    i = 0  # index for txt[]
    while (n - i) >= (m - j):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            # if verbose:
            #     print('m', m, 'n', n, 'i', i, 'j', j)
            return i-j
            j = lps[j - 1]

        # mismatch after j matches
        elif i < n and pattern[j] != text[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def computeLPSArray(pattern, m, lps):
    len = 0  # length of the previous longest prefix suffix

    lps[0]  # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i = 1 to M-1
    while i < m:
        if pattern[i] == pattern[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar
            # to search step.
            if len != 0:
                len = lps[len - 1]

            # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1


#from https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/
def badCharHeuristic(string, size):
    # '''
    # The preprocessing function for
    # Boyer Moore's bad character heuristic
    # '''
    NO_OF_CHARS = 256
    # Initialize all occurrence as -1
    badChar = [-1] * NO_OF_CHARS

    # Fill the actual value of last occurrence
    for i in range(size):
        badChar[ord(string[i])] = i
    # return initialized list
    return badChar


def boyer_moore_search(text, pattern):
    # '''
    # A pattern searching function that uses Bad Character
    # Heuristic of Boyer Moore Algorithm
    # '''
    m = len(pattern)
    n = len(text)

    # create the bad character list by calling
    # the preprocessing function badCharHeuristic()
    # for given pattern
    badChar = badCharHeuristic(pattern, m)

    # s is shift of the pattern with respect to text
    s = 0
    while s <= n - m:
        j = m - 1

        # Keep reducing index j of pattern while
        # characters of pattern and text are matching
        # at this shift s
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        # If the pattern is present at current shift,
        # then index j will become -1 after the above loop
        if j < 0:
            # '''
            #     Shift the pattern so that the next character in text
            #           aligns with the last occurrence of it in pattern.
            #     The condition s+m < n is necessary for the case when
            #        pattern occurs at the end of text
            #    '''
            return s
            s += (m - badChar[ord(text[s + m])] if s + m < n else 1)
        else:
            # '''
            #    Shift the pattern so that the bad character in text
            #    aligns with the last occurrence of it in pattern. The
            #    max function is used to make sure that we get a positive
            #    shift. We may get a negative shift if the last occurrence
            #    of bad character in pattern is on the right side of the
            #    current character.
            # '''
            s += max(1, j - badChar[ord(text[s + j])])
    return -1


def plot_time(dict_algs, algs, trails):
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
    algs = [native_search, brute_force_search, rabin_karp_search, knuth_morris_pratt_search, boyer_moore_search]
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            for alg in algs:
                start_time = time.time()
                idx = alg(text='', pattern='', verbose=True)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_algs).T
    print(df)
    plot_time(dict_algs, algs, trials)


def process_file(file_name_text, file_name_pattern):
    results = []
    with (
        open(file_name_text) as file_text,
        open(file_name_pattern) as file_pattern
    ):
        texts = file_text.readlines()
        patterns = file_pattern.readlines()
        for text in texts:
            text = text.upper()  # convert to upper case
            text = re.sub(r'[^A-Z]', '', text)  # remove all non-alphabet chars
            # print(text)
            if text == '':
                continue
            for pattern in patterns:
                pattern = pattern.upper()  # convert to upper case
                pattern = re.sub(r'[^A-Z]', '', pattern)  # remove all non-alphabet chars
                ns = native_search(text, pattern)

                bfs = brute_force_search(text, pattern)

                rks = rabin_karp_search(text, pattern)

                kmps = knuth_morris_pratt_search(text, pattern)

                bm = boyer_moore_search(text, pattern)

                results.append([text, pattern, len(text), ns, bfs, rks, kmps, bm])
    headers = ["String", "Pattern", "Length", "Native", "Brute Force", "Rabin Karp", "KMP", "Boyer Moore"]
    tt = texttable.Texttable(500)
    tt.set_cols_align(["l", "c", "c", "c", "c", "c", "c", "c"])
    tt.set_cols_dtype(["t", "t", "i", "i", "i", "i", "i", "i"])
    tt.add_row(results[0])
    tt.add_rows(results)
    tt.header(headers)
    print(tt.draw())
    return results


def main():
    process_file("Assignment6_Text1.txt", "Assignment6_Patterns.txt")
    process_file("Assignment6_Text2.txt", "Assignment6_Patterns.txt")
    # print(native_search("O'er the land of the free and the home of the brave!?", "brave"))
    # print(brute_force_search("O'er the land of the free and the home of the brave!", "brave"))
    # print(rabin_karp_search("O'er the land of the free and the home of the brave!", "brave"))
    # print(knuth_morris_pratt_search("O'er the land of the free and the home of the brave!", "brave"))
    # print(boyer_moore_search("O'er the land of the free and the home of the brave!", "brave"))


    # run_trials()
    # text = 'loopsjdbeiwm'
    # pattern = 'jdb'
    # idx1 = native_search(text, pattern, True)
    # idx2 = brute_force(text, pattern, True)
    # idx3 = rabin_karp(text, pattern, True)
    # idex4 = knuth_morris_pratt(text, pattern, True)
    # idex5 = boyer_moore(text, pattern, True)
    # print(idx1, idx2, idx3, idex4, idex5)


if __name__ == "__main__":
    main()