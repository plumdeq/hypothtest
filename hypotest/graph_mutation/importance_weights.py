# coding: utf8
# # Graph mutation
#
# Use various SNA metrics to automatically compute weights
#
# :author: Asan Agibetov
#
from hypotest.utils import utils

import networkx as nx


# By default we use betweenees centrality measure
def default_global_importance_measure(hypothgraph):
    """
    (hypograph) > dict(node=importance)

    Default global importance measure

    """
    return nx.betweenness_centrality(hypothgraph, endpoints=True)


@utils.memo
def compute_importance_weights(hypothgraph, measure=default_global_importance_measure):
    """
    (hypothgraph, [fun: measure]) -> hypothgraph

    Compute importance weights except for those set manually

    """
    computed_weights = default_global_importance_measure(hypothgraph)

    nx.set_node_attributes(hypothgraph, 'importance_weight', computed_weights)

    return hypothgraph
