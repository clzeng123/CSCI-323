# CSCI 323/700
# Summer 2022
# Assignment 5 - Palindromic Substrings and Subsequences
# Changli Zeng


import re
import texttable
import time


# From https://www.geeksforgeeks.org/longest-palindrome-substring-set-1/
def lpsst(s):
    n = len(s)
    table = [[0 for x in range(n)] for y in range(n)]
    max_length = 1
    i = 0
    while i < n:
        table[i][i] = True
        i = i + 1
    start = 0
    i = 0
    while i < n - 1:
        if s[i] == s[i + 1]:
            table[i][i + 1] = True
            start = i
            max_length = 2
        i = i + 1
    k = 3
    while k <= n:
        i = 0
        while i < (n - k + 1):
            j = i + k - 1
            if table[i + 1][j - 1] and s[i] == s[j]:
                table[i][j] = True
                if k > max_length:
                    start = i
                    max_length = k
            i = i + 1
        k = k + 1
    return s[start: start + max_length]


# From https://www.geeksforgeeks.org/print-longest-palindromic-subsequence/
# From https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/
def lcs(x, y):
    m = len(x)
    n = len(y)
    k = [[0] * (n + 1) for i in range(m + 1)]
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                k[i][j] = 0
            elif x[i-1] == y[j-1]:
                k[i][j] = k[i-1][j-1]+1
            else:
                k[i][j] = max(k[i-1][j], k[i][j-1])
    index = k[m][n]
    lcs2 = [""] * (index + 1)
    i, j = m, n
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            lcs2[index - 1] = x[i - 1]
            i -= 1
            j -= 1
            index -= 1
        elif k[i - 1][j] > k[i][j - 1]:
            i -= 1
        else:
            j -= 1
        ans = ""
    for x in range(len(lcs2)):
        ans += lcs2[x]
    return ans


# From https://www.geeksforgeeks.org/print-longest-palindromic-subsequence/
def lpssq(s):
        rev = s[:: -1]
        return lcs(s, rev)


def process_file(file_name):
    results = []
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            line = line.upper() # convert to upper case
            line = re.sub(r'[^A-Z]', '', line) # remove all non-alphabet chars
            start_time = time.time()
            st = lpsst(line)
            end_time = time.time()
            time_st = end_time - start_time
            start_time = time.time()
            sq = lpssq(line)
            end_time = time.time()
            time_sq = end_time - start_time
            results.append([line, len(line), st, len(st), time_st, sq, len(sq), time_sq])
    # return results
    headers = ["String", "Length", "LPSST", "Length", "Time", "LPSSQ", "Length", "Time"]
    tt = texttable.Texttable(500)
    tt.set_cols_align(["l", "r", "l", "r", "r", "l", "r", "r"])
    tt.set_cols_dtype(["t", "i", "t", "i", "f", "t", "i", "f"])
    tt.add_rows(results)
    tt.header(headers)
    print(tt.draw())


def main():
    process_file("palindromes.txt")
    process_file("sentences.txt")


if __name__ == "__main__":
    main()


# def test_lpsst_and_lpssq(s):
#     st = lpsst(s)
#     sq = lpssq(s)
#     print("The test string is ", s, "with length", len(s))
#     print("Its Longest Palindromic Substring is", st, "with length", len(st))
#     print("Its Longest Palindromic Subsequence is", sq, "with length", len(sq))



