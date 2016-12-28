#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Sample Digraph and Hypothesis graph
#
# Sample hypothesis graph is `digraph` (networkx) which we obtain from the
# `grontocrawler` and convert it to a hypograph with updated meta-data

from hypotest.graph_mutation import (
        importance_weights, evidence_weights, boundary)

from grontocrawler.sample_ontology.hypo_ontology import g
from grontocrawler.graph import produce_graph


# Send the sample digraph from a sample hypothesis ontology
def sample_digraph():
    return produce_graph.produce_graph(g, options=['existential-arcs'])


# Convert networkx graph into a hypograph with causality meta-data updated
def sample_hypothgraph(digraph=None):
    if digraph:
        digraph = digraph.copy()
    else:
        digraph = sample_digraph()

    # assign global important weights (topology) to the graph
    digraph = importance_weights.assign_importance_weights(digraph)

    # assign evidence weights to the graph
    digraph = evidence_weights.assign_evidence_weights(digraph)

    # assign random boudary nodes
    random_source, random_target = boundary.random_boundary_nodes(digraph)
    digraph = boundary.assign_boundary(digraph, random_source, random_target)

    return digraph
