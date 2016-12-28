#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# # Confidence propagation
#
# Confidence depends on the hypothesis configuration, which consists of
# evidenced nodes, hypothesis source and target (boundary nodes). In case there
# is a cycle, the topological order is not possible and thus the source and
# target can be interchanged.
#
# The max confidence between two random variables `X`, `Y` is the one you obtain
# when all the nodes are evidenced, which are on the shortest paths from `X` to
# `Y`. Thus, you need a helper function to compute weighted path from any node
# `u` to any node `v`.
#
# :author: Asan Agibetov
#
from operator import itemgetter
import networkx as nx

from hypotest.utils import (find_missing_nodes, sort_endpoints,
                            find_causal_endpoints)
from hypotest.assert_evidence import assert_evidence, unassert_evidence

MIN_CONFIDENCE = -100


def path_confidence(H, path, fn_importance=default_fn_importance):
    """
    (hypothgraph, path) -> float

    H
        hypothesis graph
    path
        list of nodes on the path

    fn_importance (optional)
        function which chooses how to compute confidence for one node

    """
    if not path:
        return MIN_CONFIDENCE

    confidence_measures = [fn_importance(H, node) for node in path]

    return sum(confidence_measures)


def paths_confidence(H, source, target,
                     fn_importance=default_fn_importance,
                     log=False):
    """
    (graph, source, target, func) -> (int)

    Propagate confidence factor for given source and target nodes
    Please note, that we make sure that the source and target are sorted
    topologically

    H
        hypothesis graph

    source, target
        nodes

    """
    # if no evidence then confidence is the lowest
    if (source is None or target is None):
        raise Exception("You should provide source and target")

    # re-order topologically
    source, target = sort_endpoints(H, source, target)

    # return 0 for undefined confidence if no path
    if not nx.has_path(H, source, target):
        return 0

    # compute all paths between source and target
    try:
        paths = nx.all_shortest_paths(H, source, target)
    except nx.NetworkXNoPath:
        print("No path between {} and {}".format(source, target))
        return MIN_CONFIDENCE

    confidence_measures = [path_confidence(H, path, fn_importance=fn_importance)
                           for path in paths]

    if log:
        print("confidence measures are {}".format(confidence_measures))

    return sum(confidence_measures)/float(len(confidence_measures))


def difference_importance(H, source, target, candidate_evidenced_node,
                          fn_importance=default_fn_importance, log=False):
    """
    (graph, path) -> float

    Compute difference in confidence value with or without candidate evidenced
    node

    """
    confidence_without = paths_confidence(H, source, target,
                                          fn_importance=fn_importance)

    assert_evidence(H, candidate_evidenced_node)
    confidence_with = paths_confidence(H, source, target,
                                       fn_importance=fn_importance)
    unassert_evidence(H, candidate_evidenced_node)

    gain_in_confidence = abs(confidence_with - confidence_without)

    if log:
        print("missing nodes {}".format(list(find_missing_nodes(H))))
        print("candidate evidenced node {}".format(candidate_evidenced_node))
        print("with confidence - {}, without - {}".format(confidence_with,
                                                          confidence_without))
        print("gain in confidence: {}".format(gain_in_confidence))

    return gain_in_confidence


def most_informative_missing_node(H, source=None, target=None,
                                  fn_importance=default_fn_importance):
    """
    (hypothgraph, source, target) -> [(node_id, delta_metric), ...]

    Simulate finding an evidence for one missing node, and assess the difference
    importance

    """
    if not source or not target:
        source, target = find_causal_endpoints(H)

    missing_nodes = find_missing_nodes(H)
    most_informative = {}

    for missing_node in missing_nodes:
        # evidence him and compute overall confidence
        most_informative[missing_node] = \
            difference_importance(H, source, target, missing_node)

    sorted_most_informative = sorted(most_informative.items(),
                                     key=itemgetter(1),
                                     reverse=True)

    return sorted_most_informative
