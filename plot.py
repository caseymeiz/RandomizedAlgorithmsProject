import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = "25-200"

avg_edges = pd.read_csv(f"data/{data}/avg_m.txt", names=["m"])
avg_time = pd.read_csv(f"data/{data}/avg_t.txt", names=["time"])
nodes = pd.read_csv(f"data/{data}/nodes.txt", names=["nodes"])
trials = pd.read_csv(f"data/{data}/trials.txt", names=["trials"])

df = pd.concat([avg_edges, avg_time, nodes], axis=1)

fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        'First m edges in graph with component n/2',
        'Seconds to find first m edges in graph with component n/2',
        "Edges per nodes",
        "Seconds per node",
    )
)

fig.add_trace(
    go.Scatter(
        x=df.nodes,
        y=df.m,
    ), row=1, col=1
)
fig.add_trace(
    go.Scatter(x=df.nodes, y=df.time),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(x=df.nodes, y=df.m / df.nodes),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(x=df.nodes, y=df.time / df.nodes),
    row=2, col=2
)

fig.update_xaxes(title_text="Nodes per graph", row=1, col=1)
fig.update_xaxes(title_text="Nodes per graph", row=1, col=2)
fig.update_xaxes(title_text="Nodes per graph",  row=2, col=1)
fig.update_xaxes(title_text="Nodes per graph", row=2, col=2)

fig.update_yaxes(title_text="Edges per graph", row=1, col=1)
fig.update_yaxes(title_text="Seconds per graph", row=1, col=2)
fig.update_yaxes(title_text="Ratio of edges to nodes", row=2, col=1)
fig.update_yaxes(title_text="Seconds per node", row=2, col=2)

fig.update_layout(title_text=f'trials: {trials.iloc[0].values.item()}')

fig.show()
