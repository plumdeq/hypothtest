#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Define boundary of the hypothesis graph
#
# A boundary of the hypothesis is simply two endpoints such that there is a
# path from the source to the target.

# ## Note
#
# If you have cycles and the graph is connected than you will have a path
# between any two nodes
import random
import networkx as nx


# Default boundary nodes are drawn at random
def default_boundary_nodes(digraph):
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
        return default_boundary_nodes(digraph)

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
def assign_boundary(hypothgraph, compute_boundary_nodes=default_boundary_nodes):
    """
    (hypothgraph, [fun: boundary_nodes]) -> hypothgraph

    """
    hypothgraph = unassign_boundary(hypothgraph)
    source, target = compute_boundary_nodes(hypothgraph)

    # check that there is a path from source to target otherwise raise
    # exception
    if not nx.has_path(hypothgraph, source, target):
        raise Exception('No path from {} to {}'.format(source, target))

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
