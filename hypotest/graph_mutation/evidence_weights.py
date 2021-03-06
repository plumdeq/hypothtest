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
