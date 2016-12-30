#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
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

from hypotest.confidence import hypoth_conf


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


# We need to evidence only partial nodes in the interior of the boundary
def partial_nodes_boundary_interior(hypothgraph, source, target):
    partial_nb = 0

    while partial_nb <= 0:
        in_boundary = list(in_boundary_interior(hypothgraph, source, target))
        partial_nb = len(in_boundary)/2

    total_boundary_nb = len(in_boundary)-1

    # we have at least one partial node to evidence, take some nodes while we
    # reach the partial number of nodes
    produced_nodes = 0
    while produced_nodes != partial_nb:
        rand_ind = random.randint(0, total_boundary_nb)
        yield in_boundary[rand_ind]
        produced_nodes += 1
