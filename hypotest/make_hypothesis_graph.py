# coding: utf8
"""
Create manually the hypothesis graph

We first create a list of nodes, then a list of edges. We then provide functions
which fill in default values, i.e., ``evidenced: -1``. And finally we provide a
function which builds the graph.

:author: Asan Agibetov

"""
import networkx as nx
import random


nodes = [
    (0, {'label': 'pro-inflammatory cytokines'}),
    (1, {'label': 'mechanical stimuli'}),
    (2, {'label': 'chondrocytes'}),
    (3, {'label': 'hyperthropy'}),
    (4, {'label': 'cell viability'}),
    (5, {'label': 'disruption of macromolecular content'}),
    (6, {'label': 'diminuition of hydraulic pressure'}),
    (7, {'label': 'mechanical overloading'}),
    (8, {'label': 'cartilage thinning'}),
    (9, {'label': 'reduced range of joint angles'}),
    (10, {'label': 'reduced range of joint moments'}),
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
    # choose at random end points of the causal chain
    g = set_causal_chain_endpoints(g)

    for (n, d) in g.nodes_iter(data=True):
        d["evidenced"] = -1

    for (s, t, d) in g.edges_iter(data=True):
        d["label"] = "causes"

    return g


def set_causal_chain_endpoints(H):
    """
    hypograph -> hypograph with attr set for two nodes

    Sets two nodes as endpoints of the causal chain

    """
    s, t = random.randint(0, 10), random.randint(0, 10)

    for n in H.nodes_iter():
        if n == s or n == t:
            H.node[n]['causal_endpoint'] = 1
        else:
            H.node[n]['causal_endpoint'] = 0

    return H
