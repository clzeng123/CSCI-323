import math
import random


def pseudo_random_list(n):
    data = [0]
    for i in range(1, n):
        data.append(data[i-1]+random.randint(1, 10))
    random.shuffle(data)
    return data


def build_chaining_hash(data):
    pass


def build_quad_hash(data):
    hash_table = [0] * 7

    for i in range(L):
        hash_table[i] = -1

    for i in range(N):

        # Computing the hash value
        hv = arr[i] % tsize

        # Insert in the table if there
        # is no collision
        if (table[hv] == -1):
            table[hv] = arr[i]

        else:

            # If there is a collision
            # iterating through all
            # possible quadratic values
            for j in range(tsize):

                # Computing the new hash value
                t = (hv + j * j) % tsize

                if (table[t] == -1):
                    # Break the loop after
                    # inserting the value
                    # in the table
                    table[t] = arr[i]
                    break


def build_double_hash(data):
    pass


def build_cuckoo_hash(data):
    pass

def main():
    sizes = [10 * i for i in range(1, 11)]
    data = pseudo_random_list(sizes)
    #pseudo_random_list
    print(pseudo_random_list(data))


if __name__ == "__main__":
    main()
