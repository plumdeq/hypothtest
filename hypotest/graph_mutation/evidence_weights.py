#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Evidence weights
#
# Evidence weights is assigned to each node, a factor, indicating the
# importance of the finding which confirms the presence of such a factor
import networkx as nx


# By default all evidences have equal weight of 1
def default_evidence_measure(hypothgraph):
    """
    (hypograph) -> dict(node=importance)

    """
    evidence_weights = {}
    for node, node_data in hypothgraph.nodes_iter(data=True):
        if not 'evidence_weight' in node_data:
            evidence_weights[node] = 1

    return evidence_weights


# Assign the evidence measures
def assign_evidence_weights(hypothgraph, measure=default_evidence_measure):
    """
    (hypothgraph, [fun: measure]) -> hypothgraph

    """
    computed_weights = default_evidence_measure(hypothgraph)

    nx.set_node_attributes(hypothgraph, 'evidence_weight', computed_weights)

    return hypothgraph
