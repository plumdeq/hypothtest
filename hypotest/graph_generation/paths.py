#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Paths
#
# We generate paths with a given constraint between the causal evaluation
# endpoints, i.e. nodes in the boundary interior, and between the causal source endpoint
# and nodes on the boundary. So we have simple paths between the source and all
# the nodes in the boundary interior, and all paths between the source and
# nodes on the boundary. We take a specific ratio of paths from the two sets to
# produce a sub hypothgraph, such that the boundary_interior(subhypoth) <=
# boundary_interior(hypoth) and on_boundary(subhypoth) <=
# on_boundary(subhypoth).
#
# ## Helper functions
#
# ### Sort paths from one node to another
#
# For given source and target, compute all simple paths and sort them according
# to the path lengths
import random
import math
import networkx as nx
import itertools as it

from hypotest.graph_generation import boundary


def sort_simple_paths(hypothgraph, source, target):
    simple_paths = list(nx.all_simple_paths(hypothgraph, source, target))

    sorted_paths = sorted(simple_paths, key=len)

    return sorted_paths

# ### Give a path with at least % of max path length
#
# We go through all paths we compare each path's length to the max possible
# path length, and if it is at least the given ratio (0-100%) we return that
# path

def simple_path_with_ratio(hypothgraph, source, target, ratio=0.5):
    sorted_paths = sort_simple_paths(hypothgraph, source, target)

    max_length = max(sorted_paths, len)
    ratio_length = math.ceil(ratio * max_length)

    # if current path's length is at least as big as the given ratio to the max
    # path, return it
    for path in sorted_paths:
        if len(path) >= ratio:
            return path


# ### Add path generators
#
# #### One to many path generator
#
# You give me a source and list of targets, I produce a chain of path
# generators from source to each of the targets
def chain_one_to_many_path_generator(hypothgraph, source, targets):
    """
    (graph, node, [node...]) -> generator([node...])

    """
    path_generator = ()
    for target in targets:
        path_generator = it.chain(
                nx.all_simple_paths(hypothgraph, source, target), path_generator)

    return path_generator


# #### Many to many path generator
#
# We recursively add path generator for every possible pair of elements. We use
# permutations (combinations with repetitions, i.e. 'AB' and 'BA' are two
# distinct elements)
def chain_many_to_many_path_generator(hypothgraph, nbunch):
    """
    (graph, [node...]) -> generator([node...])

    """
    path_generator = ()
    for source, target in it.permutations(nbunch, 2):
        path_generator = it.chain(
                nx.all_simple_paths(hypothgraph, source, target), path_generator)

    return path_generator

# ### Take raio of paths
#
# Given a set of paths, randomly return paths, the number of returned paths
# should be within a given ratio to all possible paths
def take_ratio_paths_rand(hypothgraph, paths, ratio=0.5):
    """
    (graph, [[node...], [node...]], float) -> generator([node...])

    """
    all_paths = list(paths)
    total_nb_paths = len(all_paths)

    # how many paths should be returned
    nb_paths_to_return = math.ceil(ratio * total_nb_paths)
    nb_paths_returned_so_far = 0

    # draw randomly paths untill we reach the ratio of paths to be returned
    while nb_paths_returned_so_far < nb_paths_to_return:
        max_index = len(all_paths)-1
        random_path_index = random.randint(0, max_index)

        yield all_paths.pop(random_path_index)
        nb_paths_returned_so_far += 1


# ## Boundary interior and on boundary paths
#
# Using the helper functions we can now produce paths with given constraints,
# inside the boundary interior, as well as on the boundary

# ### Causal endpoints path ratio
#
# Give a ratio of all paths from the causal source to the causal target

def take_ratio_endpoints_paths_rand(hypothgraph, source, target, ratio=0.5):
    all_paths = nx.all_simple_paths(hypothgraph, source, target)

    return take_ratio_paths_rand(hypothgraph, all_paths, ratio=ratio)


# ### Taking ratio random paths among boundary nodes
#
def take_ratio_boundary_paths_rand(hypothgraph, source, target, ratio=0.5):
    on_boundary_nodes = boundary.on_boundary(hypothgraph, source, target)

    boundary_paths = chain_many_to_many_path_generator(
            hypothgraph, on_boundary_nodes)

    return take_ratio_paths_rand(hypothgraph, boundary_paths, ratio=ratio)


# # Paths via ending points
#
# These functions are needed for the subgraph generation based on the ratio of
# all paths that PASS THROUGH the causal endpoints
#
def passing_via_endpoints(hypothgraph, source, target):
    all_paths = chain_many_to_many_path_generator(hypothgraph, hypothgraph.nodes_iter())

    for path in all_paths:
        if source in path and target in path:
            yield path


# ## Paths via endpoints sorted
def passing_via_endpoints_sorted(hypothgraph, source, target):
    sorted_paths = list(passing_via_endpoints(hypothgraph, source, target))
    sorted_paths = sorted(sorted_paths, key=len)

    for path in sorted_paths:
        yield path
