#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Normalization of a graph
#
# Hypothesis graph normalization is the process of *rewriting* relations `R_i`
# `negatively regulates` or `positively regulates` between the two occurrents
# `occ_1 R_i occ_2` to a *linear* causal form.
#
# * `occ_1 -- results in or causes --> occ_2`
#
# The rewriting rules for the relations are given by graph patterns, that
# indicate how to transform terms and relations.

import networkx as nx
from rdflib import namespace

positive_prefix = 'Positive_regulation_of_'
negative_prefix = 'Negative_regulation_of_'

linear_relation = 'results in'

#
# ## Normalize node
#
# We need to normalize `source` node's "id" and "label"

# ### Normalize id
#
# check if node_id is normalized, i.e., has `Positive_regulation_of` or
# `Negative_regulation_of`, by default we transform into `Positive_regulation_of`
def normalize_node_id(node_id, prefix_key='pos'):
    """
    (URIRef, str) -> ('Positively_regulation_of' | 'Negative_regulation_of_' + URIRef)

    """
    prefix = positive_prefix

    if prefix_key == 'neg':
        prefix = negative_prefix

    new_node_id = ''

    if not node_id.find(positive_prefix) == -1 or \
            not node_id.find(negative_prefix) == -1:

        return node_id

    # assume that all ids are URIs of type `http://muliscale.ch/label`
    ns, label = namespace.split_uri(node_id)
    new_label = ''.join([prefix, label])

    new_node_id = ''.join([ns, new_label])

    return new_node_id


# ### Normalize label
#
# To normalize label we simply extract the `qname` in lower case
def normalize_node_label(normalized_id):
    """
    (URIRef) -> ('Positively_regulation_of' + label)

    """
    # ensure `normalized_id` is unicode
    normalized_id = unicode(normalized_id)

    ns, label = namespace.split_uri(normalized_id)

    label = label.replace('_', ' ')

    return str(label)


def normalize_node(node, prefix_key='pos'):
    """
    (node_id, node_dict) -> (node_id, node_dict)

    """
    node_id, node_dict = node
    normalized_node_dict = node_dict.copy()
    label = normalized_node_dict['label']

    normalized_node_id = normalize_node_id(node_id, prefix_key=prefix_key)
    normalized_node_dict['label'] = normalize_node_label(normalized_node_id)

    return normalized_node_id, normalized_node_dict

#
# ## Normalizing one arc
#
# To normalize one arc we check if the label of the arc is `R = negatively |
# positively regulates` we rewrite the `source` as positive and  `target` node
# as `R target`
def normalize_arc(arc, linear_relation=linear_relation):
    """
    (source, target, edge_dict) -> (normalized arc)

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

    return normalized_source, normalized_target, normalized_edge_dict


# ## Normalize both source, target and arc
#
# Noramalize both the arc and nodes (source, target) with dicts
def normalize_nodes_and_arc(source, target, arc, linear_relation=linear_relation):
    """
    ((id, dic), (id, dict), (id_s, id_t, dict)) -> (norm_source, norm_target, norm_arc)

    """
    normalized_source, normalized_target, normalized_arc = None, None, None
    arc_s, arc_t, arc_dict = arc
    relation = arc_dict['label']

    # branch on whether it is `negative` or `positive`
    if relation.find('negative') > -1:
        normalized_source = normalize_node(source)
        normalized_target = normalize_node(target, prefix_key='neg')

    if relation.find('positive') > -1:
        normalized_source = normalize_node(source)
        normalized_target = normalize_node(target)

    normalized_arc = normalize_arc(arc, linear_relation=linear_relation)

    return normalized_source, normalized_target, normalized_arc


# ## Normalize iteratively arcs and nodes
#
# We iterate over arcs which contain either `negative | positive` and we
# transform arcs
def normalize_nodes_and_arc_iter(unnormalized, linear_relation=linear_relation):
    for arc in unnormalized.edges_iter(data=True):
        source, target, arc_dict = arc

        label = arc_dict['label']

        if label.find('negative') > -1 or label.find('positive') > -1:
            source_dict = unnormalized.node[source]
            target_dict = unnormalized.node[target]

            source_node = (source, source_dict)
            target_node = (target, target_dict)

            yield normalize_nodes_and_arc(source_node, target_node, arc)


# ## Normalize the hypothegraph
def normalize_hypothgraph(unnormalized, linear_relation=linear_relation):
    normalized_hypothgraph = nx.DiGraph()

    for source_node, target_node, arc in normalize_nodes_and_arc_iter(
            unnormalized, linear_relation=linear_relation):
        normalized_hypothgraph.add_nodes_from([source_node, target_node])
        normalized_hypothgraph.add_edges_from([arc])

    return normalized_hypothgraph
