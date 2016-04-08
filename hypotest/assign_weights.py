# coding: utf8
"""
Use various SNA metrics to automatically compute weights

:author: Asan Agibetov

"""
import networkx as nx


def compute_importance_weights(g, metric="betweeness"):
    """Compute importance weights except for those set manually"""
    computed_weights = nx.betweenness_centrality(g)

    nx.set_node_attributes(g, 'computed importance factor', computed_weights)

    return g
