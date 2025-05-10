import networkx as nx
import matplotlib.pyplot as plt
from math import hypot
import math
import numpy as np


# +--------------------------------------------------+
# |       Helper geometrical functions               |
# +--------------------------------------------------+

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
    Return True if lines l1 and l2 defined by the two point pairs are parallel.
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



def is_on_segment(p, seg, *, eps=1e-9):
    """
    True if point `p` lies on the **closed** segment `seg`.
    
    Parameters
    ----------
    p : tuple 
    seg : ((x1, y1), (x2, y2)) tuple   – segment endpoints
    eps     : tolerance for floating-point colinearity test
    """
    px, py = p
    (ax, ay), (bx, by) = seg
    
    # 1. Colinearity test   |(b-a) x (p-a)| == 0
    cross = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
    if abs(cross) > eps:
        return False

    # 2. Projection test  0 ≤ (p-a)·(b-a) ≤ |b-a|²
    dot = (px - ax) * (bx - ax) + (py - ay) * (by - ay)
    if dot < 0:
        return False

    squared_len = (bx - ax) ** 2 + (by - ay) ** 2
    if dot > squared_len:
        return False

    return True


distance=lambda p1,p2: math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)



# +--------------------------------------------------+
# |                  Main algorithm                  |
# |                                                  |
# |           Here is the meat of the code           |
# +--------------------------------------------------+


# Find intersections
# ===================

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
                inter=find_intersecting_point(e,f)
                if None not in inter:
                    intersections.add(inter)

    return intersections

# Segmentation
# ==============

def del_nonparallel(FG,G):
    """
    Discard all lines which are not parallel to any existing ones in the graph.
    Result is a list of edges to delete from the graph.

    Both are networkx graphs here.
    FG is one with spurious lines.
    G is the original graph
    """
    # set with connections between nodes
    to_delete=set()

    for fg in FG.edges():
        # if the fg line under consideration is parallel to any pre-existing line, keep it with survive=True
        survive=False
        for g in G.edges():
            if fg!=g:
                if are_parallel(g, fg):
                    survive=True

        if not survive:
            to_delete.add(fg)

    return to_delete



def del_long_segments(FG):
    """
    Keep only edges that cross only two nodes. Build a list of edges to delete from graph.
    """
    # set with connections between nodes
    to_delete=set()

    for edge in FG.edges():
        # if the edge under consideration crosses more than two nodes, discard it 
        survive=True
        for node in FG.nodes():
            if node!=edge[0] and node!=edge[1]:
                if is_on_segment(node,edge):
                    survive=False             

        if not survive:
            to_delete.add(edge)

    return to_delete



def final_answer(cycles):
    """
    Computes perimeters and their product
    """
    perimeters=[]
    
    for cycle in cycles:
        perimeter=0
        sides=len(cycle)-1
        
        for i in range(sides):
            perimeter+=distance(cycle[i],cycle[i+1])

        perimeters.append(perimeter)

    return np.prod(perimeters)
