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
    (3, {'name': 'cell viability'}),
    (4, {'name': 'disruption of macromolecular content'}),
    (5, {'name': 'diminuition of hydraulic pressure'}),
    (6, {'name': 'mechanical overloading'}),
    (7, {'name': 'cartilage thnining'}),
    (8, {'name': 'reduced range of joint angles'}),
    (9, {'name': 'reduced range of joint moments'}),
]


edges = [
    (0, 2),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (7, 8),
    (7, 9)
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
