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
import numpy as np
import networkx as nx

from hypotest.setup_hypothgraph import convert_to_hypothgraph
from hypotest.graph_generation import sub_hypothgraph, hypoth_conf, boundary
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


# Subgraph should have the smaller or equal boundary to the bigger graph
# That is, all boundary_inter_nodes(subgraph) <=
# boundary_inter_nodes(big_graph) and on_boundary_nodes(subgraph) <=
# on_boundary_nodes(big_graph)
def test_generate_subgraph(get_trivial_example):
    hypothgraph = get_trivial_example

    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)

    subgraph = sub_hypothgraph.generate_sub_hypothgraph(hypothgraph, source, target)

    # check boundary interior
    boundary_interior_subgraph = boundary.in_boundary_interior(subgraph, source, target)
    boundary_interior_biggraph = boundary.in_boundary_interior(hypothgraph, source, target)

    assert set(boundary_interior_subgraph).issubset(set(boundary_interior_biggraph))

    # check on boundary
    on_boundary_subgraph = boundary.on_boundary(subgraph, source, target)
    on_boundary_biggraph = boundary.on_boundary(hypothgraph, source, target)

    assert set(on_boundary_subgraph).issubset(set(on_boundary_biggraph))


# Ratio of on-boundary-paths '0', should not contain any path to a on_boundary
# node, however the boundary interior paths should be included in the boundary
# interior of the bigger graph
def test_zero_on_boundary_paths(get_sample_hypothgraph):
    hypothgraph = get_sample_hypothgraph
    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)

    subgraph = sub_hypothgraph.generate_sub_hypothgraph(hypothgraph, source, target, ratio_on_boundary_paths=0)

    # check boundary interior
    boundary_interior_subgraph = list(boundary.in_boundary_interior(subgraph, source, target))
    boundary_interior_biggraph = boundary.in_boundary_interior(hypothgraph, source, target)

    assert len(boundary_interior_subgraph) > 0
    assert set(boundary_interior_subgraph).issubset(set(boundary_interior_biggraph))

    # check on boundary
    on_boundary_subgraph = list(boundary.on_boundary(subgraph, source, target))
    on_boundary_biggraph = boundary.on_boundary(hypothgraph, source, target)

    assert len(on_boundary_subgraph) == 0


# If we produce subgraphs only from the paths from source to target then all
# the produced subgraphs are sub hypothesis graphs of a bigger hypothesis graph,
# i.e., preserve the boundary interior
def test_boundary_interior_preserving(get_sample_hypothgraph):
    hypothgraph = get_sample_hypothgraph
    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)

    # no on boundary paths
    ratio_on_boundary_paths = 0

    # we gradually increase the ratio, we should have at least one path from
    # source to target
    ratios = np.linspace(0.1, 1, 10)

    for ratio in ratios:
        new_subgraph = sub_hypothgraph.generate_sub_hypothgraph(
                hypothgraph, source, target, ratio_endpoints_paths=ratio,
                ratio_on_boundary_paths=ratio_on_boundary_paths)

        assert boundary.is_sub_hypothgraph(new_subgraph, hypothgraph, source, target)
