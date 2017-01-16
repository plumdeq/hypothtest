#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Sample Digraph and Hypothesis graph
#
# Sample hypothesis graph is `digraph` (networkx) which we obtain from the
# `grontocrawler` and convert it to a hypograph with updated meta-data
#
from hypotest.setup_hypothgraph import convert_to_hypothgraph

from grontocrawler.sample_ontology.hypo_ontology import g
from grontocrawler.sample_ontology.hypo_ontology_unnormalized import g as unnormalized_g
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

    hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(digraph)

    return hypothgraph


def sample_unnormalized():
    digraph = produce_graph.produce_graph(unnormalized_g, options=['existential-arcs'])

    return digraph
