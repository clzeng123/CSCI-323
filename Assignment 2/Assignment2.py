# CSCI 323/700
# Summer 2022
# Assignment 2 - Sorting Algorithms
# Changli Zeng


import copy
import math
import random
import time
import pandas as pd
import matplotlib.pyplot as plt


def random_list(range_max, size):
    numbers = []
    i = 0
    while i < size:
        rnd = random.randint(1, range_max)
        numbers.append(rnd)
        i += 1
    return numbers


def native_sort(arr):
    arr.sort()
    return arr


# From https://www.geeksforgeeks.org/bubble-sort/
def bubble_sort(arr):
    n = len(arr)
# Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# From https://www.geeksforgeeks.org/selection-sort/
def selection_sort(arr):
    # Traverse through all array elements
    for i in range(len(arr)):

        # Find the minimum element in remaining
        # unsorted array
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j

        # Swap the found minimum element with
        # the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# From https://www.geeksforgeeks.org/insertion-sort/
def insertion_sort(arr):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# From https://www.geeksforgeeks.org/cocktail-sort/
def cocktail_sort(a):
    n = len(a)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        # reset the swapped flag on entering the loop,
        # because it might be true from a previous
        # iteration.
        swapped = False

        # loop from left to right same as the bubble
        # sort
        for i in range(start, end):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True

        # if nothing moved, then array is sorted.
        if not swapped:
            break
        # otherwise, reset the swapped flag so that it
        # can be used in the next stage
        swapped = False

        # move the end point back by one, because
        # item at the end is in its rightful spot
        end = end - 1

        # from right to left, doing the same
        # comparison as in the previous stage
        for i in range(end - 1, start - 1, -1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True

        # increase the starting point, because
        # the last stage would have moved the next
        # smallest number to its rightful spot.
        start = start + 1
    return a


# From https://www.geeksforgeeks.org/shellsort/
def shell_sort(arr):
    # code here
    n = len(arr)
    gap = n // 2

    while gap > 0:
        j = gap
        # Check the array in from left to right
        # Till the last possible index of j
        while j < n:
            i = j - gap  # This will keep help in maintain gap value

            while i >= 0:
                # If value on right side is already greater than left side value
                # We don't do swap else we swap
                if arr[i + gap] > arr[i]:

                    break
                else:
                    arr[i + gap], arr[i] = arr[i], arr[i + gap]

                i = i - gap  # To check left side also
                # If the element present is greater than current element
            j += 1
        gap = gap // 2
    return arr


# From https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-search-and-sorting-exercise-8.php
def merge_sort(nlist):
    if len(nlist) > 1:
        mid = len(nlist) // 2
        lefthalf = nlist[:mid]
        righthalf = nlist[mid:]

        merge_sort(lefthalf)
        merge_sort(righthalf)
        i = j = k = 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                nlist[k] = lefthalf[i]
                i = i + 1
            else:
                nlist[k] = righthalf[j]
                j = j + 1
            k = k + 1

        while i < len(lefthalf):
            nlist[k] = lefthalf[i]
            i = i + 1
            k = k + 1

        while j < len(righthalf):
            nlist[k] = righthalf[j]
            j = j + 1
            k = k + 1

    return nlist


# From https://programmer.ink/think/622220809497d.html
def quick_sort(nums):
    n = len(nums)
    return quick(nums, 0, n - 1)


def quick(nums, left, right):
    if left >= right:
        return nums
    pivot = left
    i = left
    j = right
    while i < j:
        while i < j and nums[j] > nums[pivot]:
            j -= 1
        while i < j and nums[i] <= nums[pivot]:
            i += 1
        nums[i], nums[j] = nums[j], nums[i]
    nums[pivot], nums[j] = nums[j], nums[pivot]
    quick(nums, left, j - 1)
    quick(nums, j + 1, right)
    return nums


# From https://www.geeksforgeeks.org/heap-sort/
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is
    # greater than root
    if l < n and arr[largest] < arr[l]:
        largest = l

    # See if right child of root exists and is
    # greater than root
    if r < n and arr[largest] < arr[r]:
        largest = r

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap

        # Heapify the root.
        heapify(arr, n, largest)


# The main function to sort an array of given size
def heap_sort(arr):
    n = len(arr)

    # Build a maxheap.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)

    return arr


# From https://codezup.com/implementation-of-counting-sort-algorithm-in-python/
def counting_sort(myList):
    maxValue = 0
    for i in range(len(myList)):
        if myList[i] > maxValue:
            maxValue = myList[i]

    buckets = [0] * (maxValue + 1)

    for i in myList:
        buckets[i] += 1

    i = 0
    for j in range(maxValue + 1):
        for a in range(buckets[j]):
             myList[i] = j
             i += 1

    return myList


# From https://pythonwife.com/sorting-algorithms-in-python/
# From https://www.geeksforgeeks.org/python-program-for-insertion-sort/
def insertionSort(b):
    for i in range(1, len(b)):
        up = b[i]
        j = i - 1
        while j >= 0 and b[j] > up:
            b[j + 1] = b[j]
            j -= 1
        b[j + 1] = up
    return b


def bucket_sort(tempList):
    numberofBuckets = round(math.sqrt(len(tempList)))
    maxVal = max(tempList)
    arr = []

    for i in range(numberofBuckets):
        arr.append([])
    for j in tempList:
        index_b = math.ceil(j*numberofBuckets/maxVal)
        arr[index_b-1].append(j)

    for i in range(numberofBuckets):
        arr[i] = insertionSort(arr[i])

    k = 0
    for i in range(numberofBuckets):
        for j in range(len(arr[i])):
            tempList[k] = arr[i][j]
            k += 1
    return tempList


# From https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-search-and-sorting-exercise-19.php
def radix_sort(nums):
    RADIX = 10
    placement = 1
    max_digit = max(nums)

    while placement < max_digit:
      buckets = [list() for _ in range( RADIX )]
      for i in nums:
        tmp = int((i / placement) % RADIX)
        buckets[tmp].append(i)
      a = 0
      for b in range( RADIX ):
        buck = buckets[b]
        for i in buck:
          nums[a] = i
          a += 1
      placement *= RADIX
    return nums

# From https://rosettacode.org/wiki/Sorting_algorithms/Comb_sort#Python
def comb_sort(arr):
    gap = len(arr)
    swaps = True
    while gap > 1 or swaps:
        gap = max(1, int(gap / 1.25))  # minimum gap is 1
        swaps = False
        for i in range(len(arr) - gap):
            j = i+gap
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
                swaps = True

    return arr


def plot_time(dict_searches, sizes, searches):
    search_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for search in searches:
        search_num += 1
        d = dict_searches[search.__name__]
        x_axis = [j + 0.05 * search_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=search.__name__)
    plt.legend()
    plt.title("Run time of Sort Algorithms")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time for ten trials (ms)")
    plt.savefig("Assignment2.png")
    plt.show()


def main():
    sizes = [10, 100, 1000, 10000]
    trials = 10
    sorts = [native_sort,  bubble_sort, selection_sort, insertion_sort, cocktail_sort, shell_sort,
             merge_sort, quick_sort, heap_sort, counting_sort, bucket_sort, radix_sort, comb_sort]
    dict_sorts = {}
    for sort in sorts:
        dict_sorts[sort.__name__] = {}
    for size in sizes:
        for sort in sorts:
            dict_sorts[sort.__name__][size] = 0
        for trial in range(1, trials + 1):
            arr = random_list(100000, size)
            for sort in sorts:
                arr1 = copy.copy(arr)
                arr2 = copy.copy(arr)
                start_time = time.time()
                implement_sort = sort(arr1)
                end_time = time.time()
                build_in_sort = native_sort(arr2)
                if build_in_sort != implement_sort:
                    print("We have found an error in", sort.__name__, "please fix it")
                net_time = end_time - start_time
                dict_sorts[sort.__name__][size] += 1000 * net_time
        dict_sorts[sort.__name__][size] /= trials
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_sorts).T
    print(df)
    plot_time(dict_sorts, sizes, sorts)


if __name__ == "__main__":
    main()
