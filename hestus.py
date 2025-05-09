import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(segments):
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
    plt.title("As a graph in NetworkX")
    plt.show()