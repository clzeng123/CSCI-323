import math
import random


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


def main():
    sizes = [100 * i for i in range(1, 11)]
    arr = random_list(100000, 10, unique=True)

    print(sizes)


if __name__ == "__main__":
    main()
