import hestus as h
import networkx as nx

# Input shapes
square = (
    ((1, 1), (1, 2)),
    ((1, 2), (2, 2)),
    ((2, 2), (2, 1)),
    ((2, 1), (1, 1)))

hourglass=( ((1, 1), (1, 2)),
((1, 2), (2, 1)),
((2, 1), (2, 2)),
((2, 2), (1, 1)))

window= ( ((1, 1), (1, 2)),
((1, 2), (2, 2)),
((2, 2), (2, 1)),
((2, 1), (1, 1)),
((1.5, 1), (1.5, 2)),
((1, 1.5), (2, 1.5)))

# Shape to consider
shape=window

# Creates undirected graph from original shape and load edges
G = nx.Graph()
G.add_edges_from(shape)

# (1) Find new intersections between lines. This is essential to determine the smaller 
#     building blocks
intersections=h.find_intersections(G)

# "Full graph" for the calculations that will follow
FG = nx.complete_graph(intersections)   # undirected by default

# (2a) Delete spurious edges
to_delete=h.del_nonparallel(FG, G) # this is a list of edges to remove
FG.remove_edges_from(to_delete)

# (2b) Delete edges crossing more than 2 nodes
to_delete=h.del_long_segments(FG) # again another list of edges to delete
FG.remove_edges_from(to_delete)

# (3) Identify smaller shapes with a built-in cycle-finder algorithm (reuse 
# things that work well!)
min_cycles=nx.minimum_cycle_basis(FG)

# (4) Computes the final answer: this is the trivial part

# For convenience for the calculations that follow, repeat the last point at the end
for sublist in min_cycles:
    sublist.append(sublist[0])

# There you go.
print(h.final_answer(min_cycles))