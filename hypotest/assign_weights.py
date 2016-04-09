# coding: utf8
"""
Use various SNA metrics to automatically compute weights

:author: Asan Agibetov

"""
from hypotest.utils import memo

import networkx as nx


@memo
def compute_importance_weights(g, metric="betweeness"):
    """
    (hypothgraph, [metric]) -> hypothgraph

    Compute importance weights except for those set manually

    """
    computed_weights = nx.betweenness_centrality(g)

    nx.set_node_attributes(g, 'computed importance factor', computed_weights)

    return g
