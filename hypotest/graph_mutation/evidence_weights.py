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


# By default we use '-1' for unevidenced nodes and '1' for evidenced nodes
def default_evidence_importance_measure(hypothgraph):
    """
    (hypograph) > dict(node=importance)

    """
    evidence_weights = {}
    for node, node_data in hypothgraph.nodes_iter(data=True):
        if not 'evidence_weight' in node_data:
            evidence_weights[node] = -1


# Assign the evidence measures
def assign_evidence_weights(hypothgraph, measure=default_evidence_importance_measure):
    """
    (hypothgraph, [fun: measure]) -> hypothgraph

    """
    computed_weights = default_evidence_importance_measure(hypothgraph)

    nx.set_node_attributes(hypothgraph, 'evidence_weight', computed_weights)

    return hypothgraph


# Find already evidenced nodes, or nodes that need to be evidenced
def nodes_to_evidence(hypothgraph):
    """
    (hypothgraph) -> iter of missing nodes

    Find all non-evidenced nodes

    """
    return (n for (n, d) in hypothgraph.nodes_iter(data=True) if d["evidenced"] != 1)


def evidenced_nodes(hypothgraph):
    """
    (hypothgraph) -> iter of evidenced nodes

    Find all evidenced nodes

    """
    return (n for (n, d) in hypothgraph.nodes_iter(data=True) if d['evidenced'] == 1)
