from main import algo2
import sys
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

n = int(sys.argv[1])
trials = int(sys.argv[2])


def f(n, trials):
    running_avg = list()
    running_var = list()
    m = list()
    for _ in range(trials):
        m.append(algo2(n))
        running_avg.append(sum(m)/len(m))
        sample_mean = running_avg[-1]
        if len(m) == 1:
            running_var.append(0)
        else:
            running_var.append(sum((mi - sample_mean)**2 for mi in m)/(len(m)-1))
    return running_avg, m, running_var


average_m, m_per, running_var = f(n, trials)

df = pd.DataFrame({
    'iter': list(range(len(average_m))),
    'avg_m': average_m,
    'running_var': running_var,
    'm': m_per
})

fig = make_subplots(
    rows=2, cols=2, subplot_titles=("Running average", "First m histogram", "Running variance")
)


fig.add_trace(
    go.Scatter(
        x=df.iter,
        y=df.avg_m
    ), row=1, col=1,
)

fig.add_trace(
    go.Histogram(
        x=df.m,
    ), row=1, col=2,
)

fig.add_trace(
    go.Scatter(
        x=df.iter,
        y=df.running_var,
    ), row=2, col=1,
)

fig.update_xaxes(title_text="Number of trials", row=1, col=1)
fig.update_xaxes(title_text="Edges in graph", row=1, col=2)
fig.update_xaxes(title_text="Number of trials", row=2, col=1)

fig.update_yaxes(title_text="Avg edges in graph", row=1, col=1)
fig.update_yaxes(title_text="Count of graphs with m edges", row=1, col=2)
fig.update_yaxes(title_text="Variance of edges in graph", row=2, col=1)

fig.update_layout(title_text=f'G(n, m) n: {n} trials: {trials}')

fig.show()
