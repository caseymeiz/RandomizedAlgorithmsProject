from util import Node, union
from itertools import combinations
from random import shuffle
import matplotlib.pyplot as plt


def main():
    avg_m = list()
    for i in range(2, 100):
        avg_m.append(sum(algo(i) for _ in range(20))/20)
    plt.scatter(x=range(len(avg_m)), y=avg_m)
    plt.show()


def algo(n):
    nodes = [Node() for _ in range(n)]
    thresh = len(nodes)/2
    sample_space = list(combinations(nodes, 2))
    shuffle(sample_space)
    for i, (u, v) in enumerate(sample_space, 1):
        x = union(u, v)
        if x.size >= thresh:
            return i


if __name__ == '__main__':
    main()
