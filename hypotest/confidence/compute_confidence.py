#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# # Confidence computation
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
# author: Asan Agibetov
#
import functools
from operator import itemgetter
import networkx as nx

from hypotest.utils import (find_missing_nodes, sort_endpoints,
                            find_causal_endpoints)
from hypotest.assert_evidence import assert_evidence, unassert_evidence

MIN_CONFIDENCE = -100

# ## Node importance measures
#
# The default global importance measure is `evidence_weight` x `importance_weight`
def default_node_importance_measure(hypothgraph, node):
    """
    (hypothgraph, node) -> contribution measure

    """
    evidence_weight = hypothgraph.node[node]["evidence_weight"]
    importance_weight = hypothgraph.node[node]["importance_weight"]

    return evidence_weight * importance_weight

# max confidence measure has all the nodes evidenced, i.e., evidence_weight at
# max
def max_node_importance_measure(hypothgraph, node):
    """
    (hypothgraph, node) -> max possible contribution measure

    """
    evidence_weight = 1
    importance_weight = hypothgraph.node[node]["importance_weight"]

    return evidence_weight * importance_weight


# Given a path compute a weighted path of all the nodes
def weighted_path(hypothgraph, nodes_in_path,
                  func_importance=default_global_importance_measure):
    """
    (hypothgraph, path, fun: node_measure) -> float

    H
        hypothesis graph
    path
        list of nodes on the path

    fn_importance (optional)
        function which chooses how to compute confidence for one node

    """
    return sum(func_importance(hypothgraph, node) for node in nodes_in_path]


# For a given hypothesis configuration compute the confidence which you can get
# as a proportion of the mean weighted path to the mean weighted path whenever
# all the nodes in the path are evidenced
def normalized_confidence(hypothgraph, source, target,
        func_importance=default_global_importance_measure,
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
    # re-order topologically
    source, target = sort_endpoints(H, source, target)

    # return 0 for undefined confidence if no path
    if not nx.has_path(H, source, target):
        raise Exception("No path between {} and {}".format(source, target)

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


# Max confidence we can get wrt. hypothesis configuration. We evidence all the
# nodes in the path and compute its maximum possible confidence.
def max_confidence(hypothgraph, source, target):
    # re-order topologically
    source, target = sort_endpoints(H, source, target)

    # if there is no path raise Exception
    if not nx.has_path(H, source, target):
        raise Exception("No path between {} and {}".format(source, target)

    # you evaluate weighted paths on all paths from source to target
    all_simple_paths = nx.all_simple_paths(hypothgraph, source, target)
    nb_paths = len(all_simple_paths)

    # we define a partial function to compute weighted paths, where the node
    # importance is fixed with all nodes evidenced
    max_weighted_path = functools.partial(weighted_path,
        func_importance=default_node_importance_measure)

    confidence_measures = [max_weighted_path(hypothgraph, path) for path in all_simple_paths]

    return sum(confidence_measures)/nb_paths
