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
# # Boundary of the hypothesis configuration
#
# Boundary of the hypothesis graph depends on the hypothesis configuration.
# Nodes in the boundary interior are all the nodes between the source and
# target, which can be accessed from
# the hypothesis configuration source node. Nodes on the boundary are all nodes
# which are not in the interior of the boundary

# ## Note
#
# If you have cycles and the graph is connected than you will have a path
# between any two nodes. Moreover, the topological sort does not mean anything
# anymore, since it is not defined on directed graphs with cycles
import networkx as nx
import random
import math

from hypotest.graph_generation import hypoth_conf


# Generates all nodes accessible from source
def in_boundary_interior(hypothgraph, source, target):
    # if there is no path, nothing we can do
    try:
        source, target = hypoth_conf.sort_hypoth_conf_endpoints(hypothgraph, source, target)
    except Exception as e:
        raise e

    simple_paths = nx.all_simple_paths(hypothgraph, source, target)
    all_nodes = (node for path in simple_paths for node in path)
    boundary_interior = set(all_nodes)

    return boundary_interior


# Complement of boundary interior
def on_boundary(hypothgraph, source, target):
    boundary_interior = None
    try:
        boundary_interior = in_boundary_interior(hypothgraph, source, target)
    except Exception as e:
        raise e

    on_boundary_nodes = (node
                         for node in hypothgraph.nodes_iter()
                         if not node in boundary_interior)

    return on_boundary_nodes


# We need to evidence only partial nodes in the interior of the boundary, we
# provide a ratio of boundary_interior nodes
def partial_nodes_boundary_interior(hypothgraph, source, target, ratio_nodes=0.5):
    in_boundary = list(in_boundary_interior(hypothgraph, source, target))
    nb_nodes_to_produce = max(min(math.ceil(len(in_boundary) * ratio_nodes), len(in_boundary)), 0)
    nb_nodes_to_produce = int(nb_nodes_to_produce)

    # randomly pop out partial boundary interior nodes to the desired ratio
    # nodes
    for _ in range(nb_nodes_to_produce):
        random_node = random.choice(in_boundary)
        yield random_node


# Based on the notion of boundary we can check if a smaller digraph is a sub
# hypothesis graph of a bigger digraph. The same topology means the boundary
# interior of the subgraph is subset or equal of the big graph. We don't care
# about the `on_boundary` nodes
def is_sub_hypothgraph(small_graph, big_graph, source, target):
    boundary_interior_subgraph = list(in_boundary_interior(small_graph, source, target))
    boundary_interior_biggraph = list(in_boundary_interior(big_graph, source, target))

    subset_boundary_interior = set(boundary_interior_subgraph).issubset(set(boundary_interior_biggraph))

    return subset_boundary_interior
