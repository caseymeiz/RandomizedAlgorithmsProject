import random

class UnionFind:
  def __init__(self, n):
    self.parent = list(range(n))
    self.size = [1] * n
    self.num_components = n

  def find(self, u):
    # Follow parent pointers until we reach the root
    root = u
    while root != self.parent[root]:
      root = self.parent[root]

    # Compress the path leading back to the root
    while u != root:
      next_ = self.parent[u]
      self.parent[u] = root
      u = next_

    return root

  def union(self, u, v):
    root1 = self.find(u)
    root2 = self.find(v)

    # Connect the two components if they are not already connected
    if root1 != root2:
      # Merge smaller component into larger component
      if self.size[root1] < self.size[root2]:
        self.parent[root1] = root2
        self.size[root2] += self.size[root1]
      else:
        self.parent[root2] = root1
        self.size[root1] += self.size[root2]

      self.num_components -= 1

def monte_carlo_experiment(n, total_edges):
  # Initialize union-find data structure with n nodes
  uf = UnionFind(n)

  # Start with m = 0
  m = 0

  # Sample edges one by one, without replacement
  while m < total_edges:
    # Choose two random vertices
    v1 = random.randint(0, n-1)
    v2 = random.randint(0, n-1)

    # Make sure the vertices are different
    if v1 == v2:
      continue

    # Add edge between the two vertices
    uf.union(v1, v2)
    m += 1

    # Return m if the largest component size is at least n/2
    if uf.size[uf.find(v1)] >= n/2:
      return m

  # Return -1 if no connected component of size at least n/2 is found
  return -1

# Example usage:
n = 1000000
total_edges = n*n

m = monte_carlo_experiment(n, total_edges)

print(m)  # Output: the first value of m for which the graph has a connected component of size at least n/2
