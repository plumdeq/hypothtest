#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Node contribution
#
# Every node will have its contribution to the hypothesis configuration. The
# default node contribution is `evidence_weight` x `importance_weight`
import networkx as nx

# This function is defined on the nodes of the graph and measures the
# contribution of this node to the maximum correlation
def default_contribution_measure(hypothgraph):
    """
    (hypothgraph, node) -> dict(node=contribution measure)

    """
    contribution_weights = {}

    for node, node_data in hypothgraph.nodes_iter(data=True):
        if not 'contribution_weight' in node_data:
            evidence_weight = hypothgraph.node[node]["evidence_weight"]
            importance_weight = hypothgraph.node[node]["importance_weight"]

            contribution_weights[node] = evidence_weight * importance_weight

    return contribution_weights


# Assign the contribution weights
def assign_contribution_weights(hypothgraph, measure=default_contribution_measure):
    """
    (hypothgraph, [fun: measure]) -> hypothgraph

    """
    computed_weights = default_contribution_measure(hypothgraph)

    nx.set_node_attributes(hypothgraph, 'contribution_weight', computed_weights)

    return hypothgraph
