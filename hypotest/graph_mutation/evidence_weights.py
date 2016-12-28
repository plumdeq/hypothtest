#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Evidence weights
#
# Evidence weights is assigned to each node, a factor, indicating the
# importance of the finding which confirms the presence of such a factor
from hypotest.utils import utils

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
@utils.memo
def compute_evidence_weights(hypothgraph, measure=default_evidence_importance_measure):
    """
    (hypothgraph, [fun: measure]) -> hypothgraph

    """
    computed_weights = default_evidence_importance_measure(hypothgraph)

    nx.set_node_attributes(hypothgraph, 'evidence_weight', computed_weights)

    return hypothgraph
