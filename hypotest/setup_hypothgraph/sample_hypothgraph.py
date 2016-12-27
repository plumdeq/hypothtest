#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Sample Hypothesis graph
#
# Sample hypothesis graph is `digraph` (networkx) which we obtain from the
# `grontocrawler` and convert it to a hypograph with updated meta-data

from hypotest.setup_hypothgraph import utils

from grontocrawler.sample_ontology.hypo_ontology import g
from grontocrawler.graph import produce_graph


# Send the sample digraph from a sample hypothesis ontology
def get_digraph():
    return produce_graph.produce_graph(g, options=['existential-arcs'])


# Convert networkx graph into a hypograph with causality meta-data updated
def make_hypothgraph(digraph=None):
    digraph = digraph.copy() or get_digraph()

    source, target = utils.random_endpoints(digraph)

    # assign hypothesis configuration endpoints
    for node in digraph.nodes_iter():
        if node == source:
            digraph.node[node]['hypo_source'] = 1

        if node == target:
            digraph.node[node]['hypo_target'] = 1

    return digraph
