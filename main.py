# (1) Find new intersections between lines.
# This is essential to determine the smaller building blocks
intersections=find_intersections
FG = nx.complete_graph(intersections)   # undirected by default

# (2a) Delete spurious edges
to_delete=del_nonparallel(FG, G)
FG.remove_edges_from(to_delete)

# (2b) Delete edges crossing more than 2 nodes
to_delete=del_long_segments(FG):
FG.remove_edges_from(to_delete)

# (3) Identify smaller shapes
min_cycles=nx.minimum_cycle_basis(FG)

# (4) Computes the final answer: this is the trivial part
for sublist in min_cycles:
    sublist.append(sublist[0])

final_answer(min_cycles)