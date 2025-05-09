import networkx as nx
import matplotlib.pyplot as plt
from math import hypot
import math


def plot(segments, title=None):
    """
    Plots a graph provided where segments follows the format

segments = (
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


def plot_graph(G):
    """
    G is a graph already.
    """
    pos = { node: node for node in G.nodes() }

    plt.figure(figsize=(6,6))
    nx.draw_networkx_nodes(
        G, pos,
        node_size=600,
        node_color='cornflowerblue',
        edgecolors='k'
    )
    nx.draw_networkx_edges(
        G, pos,
        width=3,
        edge_color='tomato'
    )

    nx.draw_networkx_labels(
        G, pos,
        font_size=9
    )

    plt.gca().set_aspect('equal', 'box')  
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def find_intersecting_point(l1, l2):
    """
    Return (xi, yi) where (xi, yi) is the intersection of the
    infinite lines through p1-p2 and p3-p4.
    Input: each point is a pair (x, y).
    """
    (x1, y1), (x2, y2) = l1
    (x3, y3), (x4, y4) = l2

    denom = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    if denom == 0:            # parallel or coincident
        return None, None

    c1 = x1*y2 - y1*x2
    c2 = x3*y4 - y3*x4

    xi = (c1*(x3 - x4) - (x1 - x2)*c2) / denom
    yi = (c1*(y3 - y4) - (y1 - y2)*c2) / denom

    # parameters for the two segments
    t = ((x3 - x1)*(y3 - y4) - (y3 - y1)*(x3 - x4)) / denom
    u = ((x3 - x1)*(y1 - y2) - (y3 - y1)*(x1 - x2)) / denom

    return (xi, yi)



def are_parallel(l1, l2, tol=1e-9):
    """
    Return True if the (infinite) lines defined by the two point pairs are parallel.
    """
    (x1, y1), (x2, y2) = l1
    (x3, y3), (x4, y4) = l2

    # Direction vectors
    v1x, v1y = x2 - x1, y2 - y1
    v2x, v2y = x4 - x3, y4 - y3

    # Guard against zero-length lines
    if v1x == v1y == 0 or v2x == v2y == 0:
        raise ValueError("At least one line has zero length (two identical end-points).")

    # 2-D cross product
    cross = v1x * v2y - v1y * v2x

    # Scale tolerance with the largest direction-vector magnitude so that
    # the test is invariant to coordinate scale.
    scale = max(hypot(v1x, v1y), hypot(v2x, v2y))
    return abs(cross) <= tol * scale




# +--------------------------------------------------+
# |                  Main algorith                   |
# |                                                  |
# | Here is the meat of the code                     |
# +--------------------------------------------------+


def find_intersections(G):
    """
    This finds all intersecting points in the graph, resulting from lines which
    intercept each other. This is crucial information for what follows

    G is a graph.
    """
    intersections=set()

    for e in G.edges():
        for f in G.edges():
            # avoid the same vertex
            if e!=f:
                inter=find_intersection(e,f)
                if None not in inter:
                    intersections.add(inter)

    return intersections


