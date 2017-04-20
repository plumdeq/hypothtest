#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
# # Confidence computation
#
# Confidence depends on the hypothesis configuration, which consists of
# evidenced nodes, hypothesis source and target (boundary nodes). In case there
# is a cycle, the topological order is not possible and thus the source and
# target can be interchanged.
#
# The max confidence between two random variables `X`, `Y` is the one you obtain
# when all the nodes are evidenced, which are on all the simple paths from `X` to
# `Y`. Thus, you need a helper function to compute weighted path from any node
# `u` to any node `v`.
#
import functools
from operator import itemgetter
import networkx as nx

from hypotest.graph_generation.hypoth_conf import sort_hypoth_conf_endpoints

# ## Constants
#
# Some constants for confidence
MIN_CONFIDENCE = 0

# ## Node importance measures
#
# The default global importance measure is `evidence_weight` x
# `importance_weight`
def default_node_importance_measure(hypothgraph, node):
    """
    (hypothgraph, node) -> contribution measure

    """
    # evidence_weight = hypothgraph.node[node]["evidence_weight"]
    # importance_weight = hypothgraph.node[node]["importance_weight"]

    # return evidence_weight * importance_weight

    return 1


# Given a path compute a weighted path of all the nodes, where each nodes
# importance is contributed if he is evidenced or not
def weighted_path(hypothgraph, nodes_in_path, evidenced_nodes=[],
                  func_importance=default_node_importance_measure):
    """
    (hypothgraph, path, fun: node_measure) -> float

    H
        hypothesis graph

    nodes_in_path
        list of nodes on the path

    evidenced_nodes
        list of evidenced nodes

    fn_importance (optional)
        function which chooses how to compute confidence contribution for one node

    """
    return sum(
        func_importance(hypothgraph, node)
        for node in nodes_in_path
        if node in evidenced_nodes
    )


# Wrapper function to compute tha max confidence, by currying
# evidenced nodes as all nodes in the path
def max_weighted_path(hypothgraph, nodes_in_path, **kwargs):
    evidenced_nodes=nodes_in_path
    f = functools.partial(weighted_path, hypothgraph, nodes_in_path,
                          evidenced_nodes=evidenced_nodes)

    return f(**kwargs)


# For a given hypothesis configuration compute the confidence which you can get
# as a proportion of the mean weighted path to the mean weighted path whenever
# all the nodes in the path are evidenced
def confidence(hypothgraph, hypoth_conf,
               func_importance=default_node_importance_measure, log=False):
    """
    (graph, hypoth_conf, func) -> (int)

    Propagate confidence factor for given source and target nodes
    Please note, that we make sure that the source and target are sorted
    topologically

    H
        hypothesis graph

    hypoth_conf
        tuple(source, target, evidenced_nodes)

    """
    source, target = hypoth_conf.source, hypoth_conf.target
    evidenced_nodes = hypoth_conf.evidenced_nodes

    # re-order topologically, note that sort_boundary
    # throws exception if there are no paths from source to target
    try:
        source, target = sort_hypoth_conf_endpoints(hypothgraph, source, target)
    except nx.NetworkXNoPath:
        print("No path between {} and {}".format(source, target))
        return MIN_CONFIDENCE

    # compute all paths between source and target
    simple_paths = nx.all_simple_paths(hypothgraph, source, target)

    # Compute weighted paths for all simple paths with a given node importance
    # function
    weighted_path_values = [
        weighted_path(hypothgraph, simple_path,
                      evidenced_nodes, func_importance=func_importance)
        for simple_path in simple_paths
    ]

    # nb_paths = len(weighted_path_values)

    if log:
        print("confidence measures are {}".format(confidence_measures))

    # return sum(weighted_path_values)/float(nb_paths)
    return float(sum(weighted_path_values))

# Max confidence we can get wrt. hypothesis configuration. We evidence all the
# nodes in the path and compute its maximum possible confidence.
def max_confidence(hypothgraph, source, target,
                   func_importance=default_node_importance_measure):
    # re-order topologically, note that sort_boundary
    # throws exception if there are no paths from source to target
    try:
        source, target = sort_hypoth_conf_endpoints(hypothgraph, source, target)
    except nx.NetworkXNoPath:
        print("No path between {} and {}".format(source, target))
        return MIN_CONFIDENCE

    # compute all paths between source and target
    simple_paths = nx.all_simple_paths(hypothgraph, source, target)

    # Compute weighted paths for all simple paths with a given node importance
    # function
    max_weighted_path_values = [
        max_weighted_path(hypothgraph, simple_path, func_importance=func_importance)
        for simple_path in simple_paths
    ]

    # nb_paths = len(max_weighted_path_values)

    # return sum(max_weighted_path_values)/float(nb_paths)
    return float(sum(max_weighted_path_values))

# Normalized confidence is our confidence normalized by the max possible
# confidence
def normalized_confidence(hypothgraph, hypoth_conf,
                          func_importance=default_node_importance_measure):
    source, target = hypoth_conf.source, hypoth_conf.target
    evidenced_nodes = hypoth_conf.evidenced_nodes
    # re-order topologically, note that sort_boundary
    # throws exception if there are no paths from source to target
    try:
        source, target = sort_hypoth_conf_endpoints(hypothgraph, source, target)
    except nx.NetworkXNoPath:
        print("No path between {} and {}".format(source, target))
        return MIN_CONFIDENCE

    confidence_measure = confidence(hypothgraph, hypoth_conf, func_importance=func_importance)
    max_confidence_measure = max_confidence(hypothgraph, source, target, func_importance=func_importance)

    return float(confidence_measure)/max_confidence_measure
