#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Normalize graph
#
# We first normalize all the "neg | pos" arcs
#
# 1. Switch(arc_i == `neg | pos`)
#
#    you also need to add nodes to the list of already normalized nodes
#
#    before you transform the nodes, you need
#    to check `incoming` and `outcoming` arcs:
#
#   (source, target = arc_i):
#
#       a. for all arcs_i-1 "s_i-1 -- results in --> source", transform into
#          "s_i-1 -- results in -> positive regulation of source"
#       b. for all arcs_i+1 "target -- results in --> t_i+1", transform into
#          "positive regulation of target -- results in -> t_i+1"
#
# Then, we make the the second pass in which, we check all "linear" arcs,
# and if any of these arcs, contains a node in the "normalized" hash, then we
# adopt the "positive" version. Otherwise, we simply copy the arc
#
# 2. Switch(arc_j == 'results in') you also need to check both incoming and
#    outgoing nodes:
#
#   (source, target = arc_j):
#
#       a. for all arcs_j-1 "s_j-1 -- results in -> source" OR nothing,
#          transform into

from hypotest.graph_mutation import normalize_node, normalize_arc

import networkx as nx

LINEAR_RELATION = normalize_arc.LINEAR_RELATION


# Since we do two-time pass on the same edges of the original graph, we need to
# maintain a list of already converted `non-linear` arcs as well
def normalize_hypothgraph(unnormalized):
    converted_non_linear = []

    normalized, normalized_nodes = convert_non_linear_relations(unnormalized)
    normalized, normalized_nodes = convert_linear_relations(
            unnormalized, normalized_nodes, normalized=normalized)

    return (normalized, normalized_nodes)


# ## Normalize the hypothegraph
def convert_non_linear_relations(unnormalized, normalized=None, linear_relation=LINEAR_RELATION):
    """
    In the first iteration cycle we convert all the non-linear relations, and
    return the already normalized hypothe graph and the list of all normalized
    nodes

    """
    normalized = normalized or nx.DiGraph()
    normalized_nodes = []

    # for source_node, target_node, arc in normalize_nodes_and_arc_iter(
    #         unnormalized, linear_relation=linear_relation):
    #     normalized_hypothgraph.add_nodes_from([source_node, target_node])
    #     normalized_hypothgraph.add_edges_from([arc])

    for arc in unnormalized.edges_iter(data=True):
        source, target, arc_dict = arc

        label = arc_dict['label']

        if not normalize_arc.is_linear_relation(label):
            # normalize arc_id and add nodes to the normalized_nodes list
            normalized_arc = normalize_arc.normalize_non_linear_arc(
                    arc, normalized_nodes, linear_relation=LINEAR_RELATION)

            normalized_source_id, normalized_target_id, _ = normalized_arc

            # normalize id and label of both source and target
            normalized_source = convert_node(
                    unnormalized, source, normalized_source_id)

            normalized_target = convert_node(
                    unnormalized, target, normalized_target_id)

            # add to the new graph the source, the target and the arc
            normalized.add_nodes_from([normalized_source, normalized_target])
            normalized.add_edges_from([normalized_arc])


    return (normalized, normalized_nodes)


# To convert linear relations we need the list of normalized nodes
def convert_linear_relations(unnormalized, normalized_nodes, normalized=None, linear_relation=LINEAR_RELATION):
    """
    In the first iteration cycle we convert all the non-linear relations, and
    return the already normalized hypothe graph and the list of all normalized
    nodes

    """
    normalized = normalized or nx.DiGraph()

    # for source_node, target_node, arc in normalize_nodes_and_arc_iter(
    #         unnormalized, linear_relation=linear_relation):
    #     normalized_hypothgraph.add_nodes_from([source_node, target_node])
    #     normalized_hypothgraph.add_edges_from([arc])

    for arc in unnormalized.edges_iter(data=True):
        source, target, arc_dict = arc

        label = arc_dict['label']

        if normalize_arc.is_linear_relation(label):
            # normalize arc_id and add nodes to the normalized_nodes list
            normalized_arc = normalize_arc.normalize_linear_arc(arc, normalized_nodes)

            normalized_source_id, normalized_target_id, _ = normalized_arc

            # normalize id and label of both source and target
            normalized_source = convert_node(
                    unnormalized, source, normalized_source_id)

            normalized_target = convert_node(
                    unnormalized, target, normalized_target_id)

            # add to the new graph missing nodes and the arc
            if normalized_source_id not in normalized.nodes_iter(data=True):
                normalized.add_nodes_from([normalized_source])

            if normalized_target_id not in normalized.nodes_iter(data=True):
                normalized.add_nodes_from([normalized_target])

            normalized.add_edges_from([normalized_arc])

    return (normalized, normalized_nodes)


def convert_node(unnormalized, original_node_id, normalized_node_id):
    """
    A wrapper function to assign correct `id` and `label` to the node

    """
    normalized_node_dict = unnormalized.node[original_node_id].copy()
    normalized_node_label = normalize_node.normalize_node_label(normalized_node_id)
    normalized_node_dict['label'] = normalized_node_label

    return normalized_node_id, normalized_node_dict
