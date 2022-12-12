from util import Node, union
from itertools import combinations
from random import shuffle, sample
from time import process_time
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import math
import numpy as np

# constants
MIN_NODES = 25
MAX_NODES = 1000
STEP_SIZE = 1
TRIALS = 100


def main():
    trials = TRIALS

    # number of nodes in graphs
    nodes = list(range(MIN_NODES, MAX_NODES, STEP_SIZE)) + [MAX_NODES]

    # collected metrics
    avg_m = [0 for _ in nodes]
    var_m = [0 for _ in nodes]
    upper_m = [0 for _ in nodes]
    lower_m = [0 for _ in nodes]
    execution_time = [0 for _ in nodes]

    # run the algorithm for each node size and collect metrics
    for i in range(len(nodes)):
        print(f'\rworking on {i}/{len(nodes)}', end='')
        start = process_time()

        # number of edges to get a connected set of n/2 nodes
        # one value per trial
        m_values = [algo2(nodes[i]) for _ in range(trials)]

        # average number of edges for this size of graph
        avg_m[i] = sum(m_values)/trials

        # variance of distribution of number of edges
        var_m[i] = np.var(m_values)

        # lower and upper bounds on confidence interval
        (lower_m[i], upper_m[i]) = confidence_interval(avg_m[i], var_m[i], trials)

        # execution time for this graph size
        execution_time[i] = (process_time() - start)/trials


    # graph collected metrics

    df = pd.DataFrame({
        'm': avg_m,
        'var': var_m,
        'time': execution_time,
        'n': nodes,
        'upper': upper_m,
        'lower': lower_m
    })

    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=(
            'X/t vs. n',
            'Confidence Interval Width vs. n',
            'Distribution of M',
            'Sample Variance of M vs. n',
            'Runtime vs. n',
            'Average Runtime per Trial vs. n',
            'Runtime / Number of Nodes vs. n'
        )
    )

    # X/t vs. n
    fig.add_trace(
        go.Scatter(x=df.n, y=df.m, name="X/t", mode="lines"),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.n, y=df.upper, name="X/t (Upper Bound)", mode="lines",  line = dict(color='rgba(0,0,0,0)')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.n, y=df.lower, name="X/t (Lower Bound)", mode="lines", fill="tonexty",  line = dict(color='rgba(0,0,0,0)')),
        row=1, col=1
    )

    # Confidence Interval Width vs. n
    fig.add_trace(
        go.Scatter(x=df.n, y=df.upper - df.lower, name="Confidence Interval Width", mode="lines"),
        row=1, col=2
    )

    # Distribution of M for n = 100 for 10000 trials
    ms = [0] * 10000
    for i in range(10000):
        ms[i] = algo2(100)

    fig.add_trace(
        go.Histogram(
            x=ms
        ), row=1, col=3,
    )

    # Sample variance of M vs. n
    fig.add_trace(
        go.Scatter(x=df.n, y=var_m, name="Sample Variance of M", mode="lines"),
        row=2, col=1
    )

    # Runtime vs. n
    fig.add_trace(
        go.Scatter(x=df.n, y=df.time, name="Runtime", mode="lines"),
        row=2, col=2
    )

    # Average Runtime per trial vs. n
    fig.add_trace(
        go.Scatter(x=df.n, y=df.time/trials, name="Runtime", mode="lines"),
        row=2, col=3
    )

    # Runtime per number of nodes vs. n
    fig.add_trace(
        go.Scatter(x=df.n, y=df.time/df.n, name="Runtime", mode="lines"),
        row=3, col=1
    )


    fig.update_xaxes(title_text="Nodes per graph", row=1, col=1)
    fig.update_xaxes(title_text="Nodes per graph", row=1, col=2)
    fig.update_xaxes(title_text="Nodes per graph", row=1, col=3)
    fig.update_xaxes(title_text="Nodes per graph", row=2, col=1)
    fig.update_xaxes(title_text="Nodes per graph", row=2, col=2)
    fig.update_xaxes(title_text="Nodes per graph", row=2, col=3)
    fig.update_xaxes(title_text="Nodes per graph", row=3, col=1)

    fig.update_yaxes(title_text="Average Number of Edges", row=1, col=1)
    fig.update_yaxes(title_text="Edges", row=1, col=2)
    fig.update_yaxes(title_text="Edges", row=1, col=3)
    fig.update_yaxes(title_text="Edges", row=2, col=1)
    fig.update_yaxes(title_text="Time (seconds)", row=2, col=2)
    fig.update_yaxes(title_text="Average Time (seconds)", row=2, col=3)
    fig.update_yaxes(title_text="Time (seconds)", row=3, col=1)


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
