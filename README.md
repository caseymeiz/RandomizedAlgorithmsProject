# RandomizedAlgorithmsProject

## Install
```
Conda

python=3.11.0
plotly
pandas
numpy
```

## Run

```shell
python main.py
```

This generates a html file that contains our plots.
In the file you can specify the range of graph sizes
and the number of trials to do 


## Run the fast version

```shell
sh compile.sh
sh run.sh
```

This uses cpp implementation, it produces 4 files containing metrics like
average number of edges for each graph size, average time to process a graph.