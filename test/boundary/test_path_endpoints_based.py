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

# # Test generation of paths that pass through the causal endpoints
#
# We test that all the generated paths, contain the causal endpoints, all are
# unique and can be sorted by their lengths
import networkx as nx

from hypotest.graph_generation import boundary, hypoth_conf, paths
from hypotest.setup_hypothgraph import sample_graphs

import math
# ## Fixtures
import pytest


@pytest.fixture
def get_sample_hypothgraph():
    return sample_graphs.sample_hypothgraph()


# Both endpoints are in the returned paths, complement of the returned set does
# not contain both endpoints
def test_paths_pass_through_endpoints(get_sample_hypothgraph):
    hypothgraph = get_sample_hypothgraph
    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)

    paths_via_endpoints = list(paths.passing_via_endpoints(hypothgraph, source, target))

    for path in paths_via_endpoints:
        assert source in path
        assert target in path

    # generator over all complement paths
    all_paths = paths.chain_many_to_many_path_generator(hypothgraph, hypothgraph.nodes_iter())
    other_paths = (other_path
                   for other_path in all_paths
                   if not other_path in paths_via_endpoints)

    for other_path in other_paths:
        assert not (source in other_path and target in other_path)


# All paths passing via endpoints are sorted
def test_paths_pass_through_endpoints_are_sorted(get_sample_hypothgraph):
    hypothgraph = get_sample_hypothgraph
    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)

    sorted_paths_via_endpoints = list(paths.passing_via_endpoints_sorted(hypothgraph, source, target))

    # paths are monotonically increasing
    for previous, current in zip(sorted_paths_via_endpoints, sorted_paths_via_endpoints[1:]):
        assert len(current) >= len(previous)


# Number of edges grows monotonically
def test_nb_edges_increase_monotonically_paths_via_endpoints(get_sample_hypothgraph):
    hypothgraph = get_sample_hypothgraph
    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)

    sorted_paths_via_endpoints = list(paths.passing_via_endpoints_sorted(hypothgraph, source, target))

    # we test by iteratively creating a sub hypothesis graph, and checking that
    # the two consecutively produced snapshots of the sub hypothesis graph will
    # contain monotonically increasing number of edges. Moreover, at every time
    # step the hypothesis graph topology is preserved

    # we collect the number of produced edges
    nb_edges_snapshots = []

    iterative_sub_hypothgraph = nx.DiGraph()

    for sorted_path in sorted_paths_via_endpoints:
        iterative_sub_hypothgraph.add_path(sorted_path)

        nb_edges_snapshots.append(len(iterative_sub_hypothgraph.edges()))

    # check monotonicity
    for previous, current in zip(nb_edges_snapshots, nb_edges_snapshots[1:]):
        assert current >= previous
