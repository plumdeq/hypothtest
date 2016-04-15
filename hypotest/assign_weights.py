# coding: utf8
"""
Use various SNA metrics to automatically compute weights

:author: Asan Agibetov

"""
from hypotest.utils import memo

import networkx as nx


def dfn_global_importance_metric(H):
    """
    (hypograph) > dict(node=importance)

    Default global importance metric

    """
    return nx.betweenness_centrality(H, endpoints=True)


@memo
def compute_importance_weights(H, metric=dfn_global_importance_metric):
    """
    (hypothgraph, [metric]) -> hypothgraph

    Compute importance weights except for those set manually

    """
    computed_weights = dfn_global_importance_metric(H)

    nx.set_node_attributes(H, 'computed importance factor', computed_weights)

    return H
