#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Sample Hypothesis graph
#
# Sample hypothesis graph is `digraph` (networkx) which we obtain from the
# `grontocrawler`
from grontocrawler.sample_ontology.hypo_ontology import g
from grontocrawler.graph import produce_graph


# Send the sample hypothgraph
def get_hypograph():
    return produce_graph.produce_graph(g, options=['existential-arcs'])
