# coding: utf8
"""
Find missing nodes in the causal chain

Basically iterate via all nodes attributes, and find those factors which have
not been evidenced

:author: Asan Agibetov

"""
import networkx as nx
from hypotest.confidence_propagation import most_informative_missing_node


def find_missing_nodes(H):
    """
    (hypothgraph) -> iter of missing nodes

    Find all non-evidenced nodes

    """
    return (n for (n, d) in H.nodes_iter(data=True) if d["evidenced"] != 1)


def compute_delta(H, source, target):
    """
    (hypograph, source, target) -> hypograph with delta attributes

    For given source and target nodes, set attribute for delta importance

    """
    delta = dict(most_informative_missing_node(H, source, target))
    nx.set_node_attributes(H, 'delta', delta)

    return H
