class Node:
    def __init__(self):
        self.parent = self
        self.size = 1


def find(x):
    if x.parent != x:
        x.parent = find(x.parent)
        return x.parent
    return x


def union(x, y):
    x = find(x)
    y = find(y)
    if x == y:
        return x
    if x.size < y.size:
        [x, y] = [y, x]
    y.parent = x
    x.size += y.size
    return x
