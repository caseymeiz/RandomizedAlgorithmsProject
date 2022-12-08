from util import Node, union
from itertools import combinations
from random import shuffle, sample
from time import process_time
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def main():
    n = 1000
    avg_m = [0 for _ in range(n)]
    execution_time = [0 for _ in range(n)]
    nodes = [i for i in range(2, n+2)]
    for i in range(n):
        print(f'\rworking on {i}/{n}', end='')
        start = process_time()
        avg_m[i] = sum(algo2(nodes[i]) for _ in range(5))/5
        execution_time[i] = process_time() - start

    df = pd.DataFrame({
        'm': avg_m,
        'time': execution_time,
        'n': nodes
    })

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('n vs First m', 'n vs Time', "m / n", "time / n")
    )

    fig.add_trace(
        go.Scatter(x=df.n, y=df.m),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df.n, y=df.time),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=df.n, y=df.m/df.n),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=df.n, y=df.time/df.n),
        row=2, col=2
    )
    fig.show()


def algo(n):
    nodes = [Node() for _ in range(n)]
    sample_space = list(combinations(nodes, 2))
    shuffle(sample_space)
    for i, (u, v) in enumerate(sample_space, 1):
        x = union(u, v)
        if x.size >= len(nodes)/2:
            return i


def rand_combo(nodes, seen):
    s = frozenset(sample(nodes, 2))
    while s in seen:
        s = frozenset(sample(nodes, 2))
    seen.add(s)
    return s


# faster algo but harder to prove time complexity
def algo2(n):
    nodes = [Node() for _ in range(n)]
    seen = set()
    for i in range(1, len(nodes)**2):
        (u, v) = rand_combo(nodes, seen)
        x = union(u, v)
        if x.size >= len(nodes)/2:
            return i


if __name__ == '__main__':
    main()
