#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
import random
import networkx as nx

# # Utils functions for setting up the hypothgraph

# Assign two random endpoints of the hypothesis configuration, note that there
# should be a path between the two
def random_endpoints(digraph):
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
        return random_endpoints(digraph)

    else:
        return (source, target)


# Extract source and target of the hypothesis configuration
def hypothesis_boundary(hypothgraph):
    source, target = None, None

    try:
        source = next(node
                      for node, data in hypothgraph.nodes_iter(data=True)
                      if 'hypo_source' in data)
    except Exception:
        return None

    try:
        target = next(node
                      for node, data in hypothgraph.nodes_iter(data=True)
                      if 'hypo_target' in data)

    except Exception:
        return None

    return (source, target)
