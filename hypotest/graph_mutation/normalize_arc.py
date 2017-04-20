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
# # Normalize arc
#
# Hypothesis graph normalization is the process of *rewriting* relations `R_i`
# `negatively regulates` or `positively regulates` between the two occurrents
# `occ_1 R_i occ_2` to a *linear* causal form.
#
# * `occ_1 -- results in or causes --> occ_2`
#
# The rewriting rules for the relations are given by graph patterns, that
# indicate how to transform terms and relations.


LINEAR_RELATION = "results in"
POSITIVE_PREFIX = 'Positive_regulation_of_'
NEGATIVE_PREFIX = 'Negative_regulation_of_'

from hypotest.graph_mutation.normalize_node import normalize_node_id, normalize_node_label


def normalize_non_linear_arc(arc, normalized_nodes, linear_relation=LINEAR_RELATION):
    """
    Rewrites the tuple `source, target`, e.g., `pos of source`

    """
    source, target, edge_dict = arc
    normalized_source = ''
    normalized_target = ''
    normalized_label = ''
    normalized_edge_dict = edge_dict.copy()

    label = normalized_edge_dict['label']

    # branch on whether it is `negative` or `positive`
    if label.find('negative') > -1:
        normalized_source = normalize_node_id(source)
        normalized_target = normalize_node_id(target, prefix_key='neg')
        normalized_label = linear_relation

    if label.find('positive') > -1:
        normalized_source = normalize_node_id(source)
        normalized_target = normalize_node_id(target)
        normalized_label = linear_relation

    normalized_edge_dict['label'] = normalized_label

    # add original nodes into the list of normalized nodes
    normalized_nodes.extend([source, target])

    return normalized_source, normalized_target, normalized_edge_dict



def normalize_linear_arc(arc, normalized_nodes):
    """
    Rewrites the tuple `source, target`, e.g., `pos of source`

    """
    source, target, edge_dict = arc
    normalized_source = source
    normalized_target = target
    normalized_label = LINEAR_RELATION
    normalized_edge_dict = edge_dict.copy()

    if source in normalized_nodes:
        normalized_source = normalize_node_id(source, prefix_key='pos')
    if target in normalized_nodes:
        normalized_target = normalize_node_id(target, prefix_key='pos')

    return normalized_source, normalized_target, normalized_edge_dict



# to normalize arcs we need to check the type of the arc and then dispatch to
# relative subroutines
def normalize_arc(arc, normalized_nodes, linear_relation=LINEAR_RELATION):
    source, target, arc_dict = arc
    label = arc_dict['label']

    if is_linear_relation(label):
        normalized_arc = normalize_linear_arc(
                arc, normalized_nodes)
    else:
        normalized_arc = normalize_non_linear_arc(
                arc, normalized_nodes, linear_relation=LINEAR_RELATION)

    return normalized_arc


# ## Utils
def is_linear_relation(relation):
    if relation == LINEAR_RELATION:
        return True
    else:
        return False
