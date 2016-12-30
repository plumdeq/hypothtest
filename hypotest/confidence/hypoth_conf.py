#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
import random
import networkx as nx
from collections import namedtuple

# ## Hypothesis configuration
#
# Hypothesis configuration is a tuple (source, target, evidenced_nodes) that
# dictates how the confidence is measured
Hypoth_Conf = namedtuple('Hypoth_Conf', ['source', 'target', 'evidenced_nodes'])


# Boundary nodes drawn at random
def random_hypoth_conf_endpoints(digraph):
    """
    (digraph) -> (source, target)

    """
    min_length = 0
    max_length = len(digraph.nodes())-1

    s_index = random.randint(min_length, max_length)
    t_index = random.randint(min_length, max_length)

    # convert indices in the array to ids in the graph
    source = list(digraph.nodes_iter())[s_index]
    target = list(digraph.nodes_iter())[t_index]

    # recompute if source and target are the same, or if there is no path
    # between them
    if source == target or not nx.has_path(digraph, source, target):
        return random_hypoth_conf_endpoints(digraph)

    else:
        return (source, target)


# Unassign any assigned boundary
def unassign_boundary(hypothgraph):
    boundary_nodes = get_boundary_nodes(hypothgraph)

    if boundary_nodes is None:
        return hypothgraph

    # delete 'hypothesis_source' and 'hypothesis_target' from dict
    source, target = boundary_nodes
    del hypothgraph[source]['hypothesis_source']
    del hypothgraph[source]['hypothesis_target']


# Assign boundary nodes to the digraph
def assign_boundary(hypothgraph, source, target):
    """
    (hypothgraph, (source, target)) -> hypothgraph

    """
    # sort source, target (if not already sorted ) and check that there is a
    # path from source to target otherwise raise exception
    source, target = sort_boundary(hypothgraph, source, target)

    # unassign previous boundary nodes
    hypothgraph = unassign_boundary(hypothgraph)

    # assign hypothesis configuration endpoints
    for node in hypothgraph.nodes_iter():
        if node == source:
            hypothgraph.node[node]['hypothesis_source'] = 1

        if node == target:
            hypothgraph.node[node]['hypothesis_target'] = 1

    return hypothgraph


# Extract source and target of the hypothesis configuration
def get_boundary_nodes(hypothgraph):
    source, target = None, None

    try:
        source = next(node
                      for node, data in hypothgraph.nodes_iter(data=True)
                      if 'hypothesis_source' in data)
    except Exception:
        return None

    try:
        target = next(node
                      for node, data in hypothgraph.nodes_iter(data=True)
                      if 'hypothesis_target' in data)

    except Exception:
        return None

    return (source, target)


# Given two nodes, we sort them topologically, we also check whether there is a
# path between the two nodes
def sort_hypoth_conf_endpoints(hypothgraph, u, v):
    """
    (hypothgraph, endpoint1, endpoint2) -> sorted(endpoint1, endpoint2)

    We run the topological sort on hypothgraph and make sure that u and v are correctly
    sorted

    """
    # We may have cycles, in that case no topological sorting is possible
    try:
        topol_sorted = nx.topological_sort(hypothgraph)
        u_index, v_index = topol_sorted.index(u), topol_sorted.index(v)
        source, target = (u, v) if u_index < v_index else (v, u)

    # TODO catch proper NetworkX exception (cf. definition of
    # `nx.topological_sort`)
    except Exception:
        source, target = u, v

    if not nx.has_path(hypothgraph, source, target):
        raise Exception("No path between {} and {}".format(source, target))

    return (source, target)
