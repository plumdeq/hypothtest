#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
author: Asan Agibetov

   Copyright 2015-2017 Asan Agibetov <asan.agibetov@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
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
