from util import Node, union
from itertools import combinations
from random import shuffle, sample
from time import process_time
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import math
import numpy as np


def main():
    nodes = list(range(25, 200, 1)) + [200]
    trials = 1000
    avg_m = [0 for _ in nodes]
    std_m = [0 for _ in nodes]
    execution_time = [0 for _ in nodes]
    for i in range(len(nodes)):
        print(f'\rworking on {i}/{len(nodes)}', end='')
        start = process_time()
        m_values = [algo2(nodes[i]) for _ in range(trials)]
        avg_m[i] = sum(m_values)/trials
        std_m[i] = np.std(m_values)
        execution_time[i] = (process_time() - start)/trials

    df = pd.DataFrame({
        'm': avg_m,
        'time': execution_time,
        'n': nodes,
        'std_m': std_m
    })

    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'First m edges in graph with component n/2',
            'Seconds to find first m edges in graph with component n/2',
            "Ratio of edges to nodes",
            "Ratio of seconds per node",
        )
    )

    fig.add_trace(
        go.Scatter(x=df.n, y=df.m),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.n, y=df.m+df.std_m),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.n, y=df.m-df.std_m),
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





    fig.update_xaxes(title_text="Nodes per graph", row=1, col=1)
    fig.update_xaxes(title_text="Nodes per graph", row=1, col=2)
    fig.update_xaxes(title_text="Nodes per graph", row=2, col=1)
    fig.update_xaxes(title_text="Nodes per graph", row=2, col=2)

    fig.update_yaxes(title_text="Edges per graph", row=1, col=1)
    fig.update_yaxes(title_text="Seconds per graph", row=1, col=2)
    fig.update_yaxes(title_text="Ratio of edges to nodes", row=2, col=1)
    fig.update_yaxes(title_text="Seconds per node", row=2, col=2)

    fig.update_layout(title_text=f'trials: {trials}')

    fig.write_html(f'sample range: {nodes[0]}-{nodes[-1]} total samples:{len(nodes)} trials: {trials}.html')


def bad_algo(n):
    nodes = [Node() for _ in range(n)]
    sample_space = list(combinations(nodes, 2))
    shuffle(sample_space)
    for i, (u, v) in enumerate(sample_space, 1):
        x = union(u, v)
        if x.size >= len(nodes)/2:
            return i


def rand_combo(nodes, seen):
    s = tuple(sorted(sample(nodes, 2), key=id))
    while s in seen:
        s = tuple(sorted(sample(nodes, 2), key=id))
    seen.add(s)
    return s


# faster algo but harder to prove time complexity
def algo2(n):
    nodes = [Node() for _ in range(n)]
    seen = set()
    for i in range(1, len(nodes)**3):
        (u, v) = rand_combo(nodes, seen)
        x = union(u, v)
        if x.size >= len(nodes)/2:
            return i

# calculate upper and lower bound of 95% confidence interval
# returns a 2 element tuple (lower bound, upper bound)
# requires the sample mean, sample variance, and number of trials
def confidence_interval(sample_mean, sample_variance, trials):
    sigma = (math.sqrt(trials * sample_variance) * math.sqrt(20)) / trials

    return (sample_mean - sigma, sample_mean + sigma)


if __name__ == '__main__':
    main()
