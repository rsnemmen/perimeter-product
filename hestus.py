import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(segments, title=None):
    """
    Plots a graph provided as 

square = (
    ((1, 1), (1, 2)),
    ((1, 2), (2, 2)),
    ((2, 2), (2, 1)),
    ((2, 1), (1, 1)),
)
    """
    # Build an undirected graph ----------------------------------------------
    G = nx.Graph()
    G.add_edges_from(segments)          # endpoints become nodes, tuples are edges

    # optional: store geometry on the edge so you can retrieve it later
    for u, v in G.edges:
        G.edges[u, v]["geometry"] = (u, v)

    # Visualise ---------------------------------------------------------------
    # NetworkX draws vertices; we already have coordinates, so supply them:
    pos = {node: node for node in G.nodes}   # node -> (x,y)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=600,
        node_color="cornflowerblue",
        edge_color="tomato",
        width=3,
    )
    
    plt.gca().set_aspect("equal")
    if title:
        plt.title(title)
    plt.show()