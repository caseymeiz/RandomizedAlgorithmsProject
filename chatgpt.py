import random

def monte_carlo_experiment(n, total_edges):
  # Initialize empty graph with n vertices
  G = []
  for i in range(n):
    G.append([])

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
    G[v1].append(v2)
    G[v2].append(v1)

    m += 1

    # Check if G has a connected component of size at least n/2
    visited = [False] * n
    queue = []
    component_size = 0

    # Start BFS from a random vertex
    start_vertex = random.randint(0, n-1)
    visited[start_vertex] = True
    queue.append(start_vertex)
    component_size += 1

    while len(queue) > 0:
      v = queue.pop(0)
      for u in G[v]:
        if not visited[u]:
          visited[u] = True
          queue.append(u)
          component_size += 1

          # Return m if the component size is at least n/2
          if component_size >= n/2:
            return m

  # Return -1 if no connected component of size at least n/2 is found
  return -1

# Example usage:
n = 100
total_edges = 100

m = monte_carlo_experiment(n, total_edges)

print(m)  # Output: the first value of m for which the graph has a connected component of size at least n/2
