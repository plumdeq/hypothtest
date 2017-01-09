#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Computing confidences for a given hypothesis graph
#
# Given a hypothesis graph and the causal endpoints we compute the full
# spectrum of confidences based on nodes in the boundary interior.
from hypotest.confidence import compute_confidence
from hypotest.graph_generation import boundary, hypoth_conf


Hypoth_Conf = hypoth_conf.Hypoth_Conf


# Add gradually nodes from the boundary interior and evaluate the confidence
def confidence_spectrum(hypothgraph, source, target, normalized=False):
    evidenced_nodes = []
    confidences = []
    iterative_hypoth_conf = Hypoth_Conf(source, target, evidenced_nodes)

    # which type of confidence are we computing, normalized or not
    func_confidence = compute_confidence.confidence
    if normalized:
        func_confidence = compute_confidence.normalized_confidence

    # initial confidence
    confidences.append(func_confidence(hypothgraph, iterative_hypoth_conf))

    # all nodes in the boundary interior
    nodes_boundary_interior = boundary.in_boundary_interior(
            hypothgraph, source, target)

    # add confidence values
    for boundary_interior_node in nodes_boundary_interior:
        evidenced_nodes.append(boundary_interior_node)
        iterative_hypoth_conf = Hypoth_Conf(source, target, evidenced_nodes)
        confidences.append(func_confidence(hypothgraph, iterative_hypoth_conf))

    return confidences


# Relative confidences of a subgraph to its max confidence, and to the max
# confidence possible, we return a dictionary of values which is suitable for
# pandas dataframes
def relative_confidence_spectrum(big, small, source, target):
    evidenced_nodes = []
    iterative_hypoth_conf = Hypoth_Conf(source, target, evidenced_nodes)
    dict_confidences = {}

    # shortcut names for confidence functions
    func_conf = compute_confidence.confidence
    func_conf_norm = compute_confidence.normalized_confidence

    # compute max confidences in the small and in the big graphs
    max_small_confidence = compute_confidence.max_confidence(small, source, target)
    max_big_confidence = compute_confidence.max_confidence(big, source, target)

    # all nodes in the boundary interior of the SUBGRAPH
    nodes_boundary_interior = boundary.in_boundary_interior(
            small, source, target)

    # initial confidence values
    dict_confidences['sub_confidence_spectrum'] = [
            func_conf(small, iterative_hypoth_conf)]
    dict_confidences['big_confidence_spectrum'] = [
            func_conf(big, iterative_hypoth_conf)]
    dict_confidences['sub_confidence_normalized_spectrum'] = [
            func_conf_norm(small, iterative_hypoth_conf)]
    dict_confidences['big_confidence_normalized_spectrum'] = [
            func_conf_norm(big, iterative_hypoth_conf)]

    # add confidence values
    for boundary_interior_node in nodes_boundary_interior:
        evidenced_nodes.append(boundary_interior_node)
        iterative_hypoth_conf = Hypoth_Conf(source, target, evidenced_nodes)

        dict_confidences['sub_confidence_spectrum'].append(
                func_conf(small, iterative_hypoth_conf))
        dict_confidences['big_confidence_spectrum'].append(
                func_conf(big, iterative_hypoth_conf))
        dict_confidences['sub_confidence_normalized_spectrum'].append(
                func_conf_norm(small, iterative_hypoth_conf))
        dict_confidences['big_confidence_normalized_spectrum'].append(
                func_conf_norm(big, iterative_hypoth_conf))

    return dict_confidences