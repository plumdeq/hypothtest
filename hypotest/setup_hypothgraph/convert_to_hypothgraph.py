#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Convert any digraph into a hypothgraph
#
# A hypothgraph needs to have additional parameters computed
#
# - `evidence_weight`
# - `importance_weight`
# - `boundary nodes` (`hypothesis_source` and `hypothesis_target`)
#
from hypotest.graph_mutation import importance_weights, evidence_weights


# Convert networkx graph into a hypograph with causality meta-data updated
def convert_to_hypothgraph(digraph):
    # assign global important weights (topology) to the graph
    digraph = importance_weights.assign_importance_weights(digraph)

    # assign evidence weights to the graph
    digraph = evidence_weights.assign_evidence_weights(digraph)

    return digraph
