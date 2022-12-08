from main import algo2
import sys


def f(n, trials):
    return sum(algo2(n) for _ in range(trials)) / trials / n


print(f(int(sys.argv[1]), int(sys.argv[2])))
