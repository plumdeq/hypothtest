# coding: utf8
"""
Create manually the hypothesis graph

We first create a list of nodes, then a list of edges. We then provide functions
which fill in default values, i.e., ``evidenced: -1``. And finally we provide a
function which builds the graph.

:author: Asan Agibetov

"""
import networkx as nx


nodes = [
    (0, {'name': 'pro-inflammatory cytokines'}),
    (1, {'name': 'mechanical stimuli'}),
    (2, {'name': 'chondrocytes'}),
    (3, {'name': 'hyperthropy'}),
    (4, {'name': 'cell viability'}),
    (5, {'name': 'disruption of macromolecular content'}),
    (6, {'name': 'diminuition of hydraulic pressure'}),
    (7, {'name': 'mechanical overloading'}),
    (8, {'name': 'cartilage thinning'}),
    (9, {'name': 'reduced range of joint angles'}),
    (10, {'name': 'reduced range of joint moments'}),
]


edges = [
    (0, 2),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (8, 9),
    (8, 10)
]


def make_hypothesis_graph():
    """Creates a hypothesis graph by filling default values, and populating from
    nodes and edges lists"""
    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    g = fill_in_default_values(g)

    return g


def fill_in_default_values(g):
    """Fill in default values, i.e., evidenced=-1 for nodes, and name='causes'
    for edges"""
    for (n, d) in g.nodes_iter(data=True):
        d["evidenced"] = -1

    for (s, t, d) in g.edges_iter(data=True):
        d["name"] = "causes"

    return g
