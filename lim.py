from main import algo2
import sys
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from time import time

n = int(sys.argv[1])
trials = int(sys.argv[2])

m = list()
time_spent = list()
for _ in range(trials):
    start = time()
    result = algo2(n)
    time_spent.append(time()-start)
    m.append(result)

df = pd.DataFrame({
    'trial': list(range(trials)),
    'm': m,
    'time': time_spent
})

fig = make_subplots(
    rows=2, cols=2, subplot_titles=(
        "Running Average",
        "First m Histogram",
        "Running m Standard Deviation",
        "Running average of time spent"
    )
)


fig.add_trace(
    go.Scatter(
        x=df.trial,
        y=df.m.expanding().mean()
    ), row=1, col=1,
)

fig.add_trace(
    go.Histogram(
        x=df.m,
    ), row=1, col=2,
)

fig.add_trace(
    go.Scatter(
        x=df.trial,
        y=df.m.expanding().std(),
    ), row=2, col=1,
)

fig.add_trace(
    go.Scatter(
        x=df.trial,
        y=df.time.expanding().mean(),
    ), row=2, col=2,
)

fig.update_xaxes(title_text="Trial", row=1, col=1)
fig.update_xaxes(title_text="Edges in graph", row=1, col=2)
fig.update_xaxes(title_text="Trial", row=2, col=1)
fig.update_xaxes(title_text="Trial", row=2, col=2)

fig.update_yaxes(title_text="Average m edges", row=1, col=1)
fig.update_yaxes(title_text="Count of graphs with m edges", row=1, col=2)
fig.update_yaxes(title_text="Standard Deviation of edges in graph", row=2, col=1)
fig.update_yaxes(title_text="Seconds", row=2, col=2)

fig.update_layout(
    title_text=f'G(n, m) n: {n} trials: {trials}')

fig.show()
fig.write_html(f"lim n:{n} trials{trials}.html")
