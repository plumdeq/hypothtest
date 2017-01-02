#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# same old trick to put this directory into the path
import os
import sys

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
mypath = os.path.join(dirname, '..')
mypath = os.path.abspath(mypath)
sys.path.insert(0, mypath)

# # Testing graph generation functions

# Graph generation functions are used to generate graphs. One of them is to
# construct a subgraph from a full graph given certain constraints. One such
# set of constraints could be the source and target nodes of the hypothesis
# configuration, as well as the percentage of the paths between the two nodes.
# The graph generation would then try to give you a subgraph with the given
# percentage of paths between the source and the target.
import networkx as nx

from hypotest.setup_hypothgraph import convert_to_hypothgraph
from hypotest.graph_generation import boundary, hypoth_conf, paths
from hypotest.setup_hypothgraph import sample_graphs

import math
# ## Fixtures
import pytest


# Trivial example will include a complete graph with some
@pytest.fixture
def get_trivial_example():
    digraph = nx.complete_graph(6, create_using=nx.DiGraph())
    hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(digraph)

    return hypothgraph


@pytest.fixture
def get_sample_hypothgraph():
    return sample_graphs.sample_hypothgraph()


# Number of ratio paths is smaller than the all paths
def test_ratio_endpoints_paths_trivial_hypothgraph(get_trivial_example):
    hypothgraph = get_trivial_example

    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)
    ratio_paths = 0.7

    endpoints_paths = list(nx.all_simple_paths(hypothgraph, source, target))
    endpoints_ratio_paths = list(
            paths.take_ratio_endpoints_paths_rand( hypothgraph, source, target, ratio=ratio_paths))

    # nb of generated paths is at least the given ratio to the total amount of
    # paths
    nb_ratio_paths = len(endpoints_ratio_paths)
    nb_total_paths = len(endpoints_paths)

    assert nb_ratio_paths == math.ceil(ratio_paths * nb_total_paths)


def test_ratio_endpoints_paths_sample_hypothgraph(get_sample_hypothgraph):
    hypothgraph = get_sample_hypothgraph

    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)
    ratio_paths = 0.7

    endpoints_paths = list(nx.all_simple_paths(hypothgraph, source, target))
    endpoints_ratio_paths = list(
            paths.take_ratio_endpoints_paths_rand( hypothgraph, source, target, ratio=ratio_paths))

    # nb of generated paths is at least the given ratio to the total amount of
    # paths
    nb_ratio_paths = len(endpoints_ratio_paths)
    nb_total_paths = len(endpoints_paths)

    assert nb_ratio_paths == math.ceil(ratio_paths * nb_total_paths)


# Number of ratio paths is smaller than the all paths
def test_ratio_on_boundary_paths_trivial_hypothgraph(get_trivial_example):
    hypothgraph = get_trivial_example

    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)
    ratio_paths = 0.7

    on_boundary_nodes = boundary.on_boundary(hypothgraph, source, target)
    boundary_paths = list(
            paths.chain_many_to_many_path_generator(hypothgraph, on_boundary_nodes))

    boundary_ratio_paths = list(
            paths.take_ratio_boundary_paths_rand( hypothgraph, source, target, ratio=ratio_paths))

    # nb of generated paths is at least the given ratio to the total amount of
    # paths
    nb_ratio_paths = len(boundary_ratio_paths)
    nb_total_paths = len(boundary_paths)

    assert nb_ratio_paths == math.ceil(ratio_paths * nb_total_paths)


def test_ratio_on_boundary_paths_sample_hypothgraph(get_sample_hypothgraph):
    hypothgraph = get_sample_hypothgraph

    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)
    ratio_paths = 0.7

    on_boundary_nodes = boundary.on_boundary(hypothgraph, source, target)
    boundary_paths = list(
            paths.chain_many_to_many_path_generator(hypothgraph, on_boundary_nodes))

    boundary_ratio_paths = list(
            paths.take_ratio_boundary_paths_rand( hypothgraph, source, target, ratio=ratio_paths))

    # nb of generated paths is at least the given ratio to the total amount of
    # paths
    nb_ratio_paths = len(boundary_ratio_paths)
    nb_total_paths = len(boundary_paths)

    assert nb_ratio_paths == math.ceil(ratio_paths * nb_total_paths)
