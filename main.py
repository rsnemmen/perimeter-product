intersections=find_intersections
FG = nx.complete_graph(intersections)   # undirected by default


# Delete spurious edges
del_nonparallel
FG.remove_edges_from(to_delete)