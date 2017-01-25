#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Computing confidences for a given hypothesis graph
#
# Given a hypothesis graph and the causal endpoints we compute the full
# spectrum of confidences based on nodes in the boundary interior.
import itertools as it

from hypotest.confidence import compute_confidence
from hypotest.graph_generation import boundary, hypoth_conf


Hypoth_Conf = hypoth_conf.Hypoth_Conf


# Add gradually nodes from the boundary interior and evaluate the confidence
# However, since there might be a choice of which nodes to evidence, we need to
# compute mean confidence for a number of evidenced nodes mean(|E| = 1..N) etc.
#
def confidences_possibilities(hypothgraph, source, target,
                              number_of_evidenced, normalized=False):
    """
    (graph, node, node, list, bool) -> list[confidence_for_possibility]

    """
    # base case when we have no evidences, it is zero
    if number_of_evidenced == 0:
        return [0.0]

    # all nodes which potentially need to be evidenced
    interior_nodes = boundary.in_boundary_interior(hypothgraph, source, target)

    # we accumulate confidence values here
    confidences = []

    # which type of confidence are we computing, normalized or not
    func_confidence = compute_confidence.confidence
    if normalized:
        func_confidence = compute_confidence.normalized_confidence

    # take combinations of interior nodes for the required number of evidenced
    # nodes
    for evidenced_possibility in it.combinations(interior_nodes, number_of_evidenced):
        # make a hypothesis configuration
        new_conf = Hypoth_Conf(source, target, evidenced_possibility)
        confidences.append(func_confidence(hypothgraph, new_conf))

    return confidences


# Compute the possible spectrum of mean confidences for the gradually
# increasing number of evidenced nodes
def confidence_spectrum(hypothgraph, source, target, normalized=False):
    spectrum = []

    # all nodes in the boundary interior
    interior = list(boundary.in_boundary_interior(hypothgraph, source, target))

    # from zero to full number of potential evidences
    for number_of_evidence_possibilities in range(len(interior) + 1):
        confidences = confidences_possibilities(
                hypothgraph, source, target,
                number_of_evidence_possibilities,
                normalized=normalized)

        spectrum.append(confidences)

        # mean_confidence = sum(confidences)/float(len(confidences))
        # mean_confidences.append(mean_confidence)

    return spectrum


# #################################
# DEPRECATED
# #################################

# Compute the possible spectrum of confidences for the gradually
# increasing number of evidenced nodes
def old_confidence_spectrum(hypothgraph, source, target, normalized=False):
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
