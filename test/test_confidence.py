#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# same old trick to put this directory into the path
import os
import sys

import networkx as nx

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
mypath = os.path.join(dirname, '..')
mypath = os.path.abspath(mypath)
sys.path.insert(0, mypath)

# # Testing confidence computation

# Max confidence is the sum of weighted paths where all nodes are evidenced.
# Essentially, we perform a series of tests on path graphs, and complete graphs
#
from hypotest.setup_hypothgraph import sample_graphs
from hypotest.graph_mutation import boundary
from hypotest.confidence import compute_confidence
from hypotest.setup_hypothgraph import convert_to_hypothgraph

# ## Fixtures
import pytest

Hypoth_Conf = compute_confidence.Hypoth_Conf

@pytest.fixture
def get_complete_graph():
    complete_graph = nx.complete_graph(10, nx.DiGraph())
    hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(complete_graph)

    return hypothgraph


# ## Hypothesis configuration
#
# Some sample graphs on which we test the confidence propagation
# We have the following types of hypothesis configurations
#
# * nothing evidenced should be less than max confidence
# * partial evidence within boundary should be less than max condidence, and
#   more than nothing evidenced
# * full evidence within boundary should be exactly the same as max confidence
# * nothing evidenced  within boundary and everything evidenced outside the boundary
#   should be exactly less than the max confidence
#



# Our test graph function, gives us a simple path graph and a set of
# hypothesis configurations
@pytest.fixture
def get_path_graph_and_configurations():
    path_graph = nx.path_graph(10, nx.DiGraph())
    hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(path_graph)

    # hypothesis configurations (source, target, evidenced_nodes), we fix
    # source and target to some nodes
    source = 0
    target = 4

    # nothing evidenced, partially within boundary, full within boundary,
    # nothing inside, some outside
    nothing         =  Hypoth_Conf(source=source, target=target, evidenced_nodes=[])
    partial_within  =  Hypoth_Conf(source=source, target=target, evidenced_nodes=[0, 2])
    full_within     =  Hypoth_Conf(source=source, target=target, evidenced_nodes=[0, 1, 2, 3, 4])

    return {
        'hypothgraph': hypothgraph,
        'nothing': nothing,
        'partial_within': partial_within,
        'full_within': full_within,
    }

# ### Unit test weighted path computation
def test_weighted_path_on_path_graph(get_path_graph_and_configurations):
    test_data = get_path_graph_and_configurations
    hypothgraph = test_data['hypothgraph']

    # when nothing is evidenced on the path weighted path should be 0
    null_confidence = compute_confidence.weighted_path(hypothgraph, [0, 1, 2, 3], [])
    assert null_confidence == 0

    # when something is evidenced the confidence should be more than zero
    some_confidence = compute_confidence.weighted_path(hypothgraph, [0, 1, 2, 3], [0, 1])
    assert some_confidence > null_confidence

    # when every node in path is evidenced we get max confidence, which should
    # be bigger than some_confidence
    max_confidence = compute_confidence.weighted_path(hypothgraph, [0, 1, 2, 3], [0, 1, 2, 3])
    assert max_confidence > some_confidence



# ### Nothing evidenced on path graph
#
# Confidence with no nodes evidenced should be strictly smaller than the max
# possible confidence
def test_nothing_evidenced_on_path_graph(get_path_graph_and_configurations):
    test_data   = get_path_graph_and_configurations
    hypothgraph = test_data['hypothgraph']
    nothing     = test_data['nothing']

    # confidence with nothing evidenced should be 0
    confidence = compute_confidence.confidence(hypothgraph, nothing)
    assert confidence == 0

    # max confidence for the same boundary should be bigger than confidence
    max_confidence = compute_confidence.max_confidence(hypothgraph, nothing.source, nothing.target)
    assert max_confidence > confidence

    # normalized confidence should also be zero since we have nothing evidenced
    normalized_confidence = compute_confidence.normalized_confidence(hypothgraph, nothing)
    assert normalized_confidence == 0


# Confidence with partial nodes evidenced should be bigger than zero, max
# confidence should be bigger than confidence. Normalized confidence should be
# in [0..1] range
def test_partial_evidenced_within_on_path_graph(get_path_graph_and_configurations):
    test_data      = get_path_graph_and_configurations
    hypothgraph    = test_data['hypothgraph']
    partial_within = test_data['partial_within']

    # confidence with nothing evidenced should be 0
    confidence = compute_confidence.confidence(hypothgraph, partial_within)
    assert confidence > 0

    # max confidence for the same boundary should be bigger than confidence
    max_confidence = compute_confidence.max_confidence(
            hypothgraph, partial_within.source, partial_within.target)
    assert max_confidence > confidence

    # normalized confidence should be in (0..1)
    normalized_confidence = compute_confidence.normalized_confidence(
            hypothgraph, partial_within)
    assert normalized_confidence > 0 and normalized_confidence < 1


# Confidence with all nodes evidenced should be bigger than zero, max
# confidence should be equal to confidence. Normalized confidence should be
# 1
def test_full_evidenced_within_on_path_graph(get_path_graph_and_configurations):
    test_data   = get_path_graph_and_configurations
    hypothgraph = test_data['hypothgraph']
    full_within = test_data['full_within']

    # confidence with nothing evidenced should be 0
    confidence = compute_confidence.confidence(hypothgraph, full_within)
    assert confidence > 0

    # max confidence for the same boundary should be equal to confidence
    max_confidence = compute_confidence.max_confidence(
            hypothgraph, full_within.source, full_within.target)
    assert max_confidence == confidence

    # normalized confidence should be 1
    normalized_confidence = compute_confidence.normalized_confidence(
            hypothgraph, full_within)
    assert normalized_confidence == 1


# Evidencing nodes outside boundary does not influence confidences
#
def test_evidenced_outside_on_path_graph(get_path_graph_and_configurations):
    test_data      = get_path_graph_and_configurations
    hypothgraph    = test_data['hypothgraph']
    partial_within = test_data['partial_within']

    before_confidence       =  compute_confidence.confidence(hypothgraph, partial_within)
    before_max_confidence   =  compute_confidence.max_confidence(hypothgraph, partial_within.source, partial_within.target)
    before_norm_confidence  =  compute_confidence.normalized_confidence(hypothgraph, partial_within)

    # evidence nodes outside the boundary
    simple_paths = nx.all_simple_paths(hypothgraph, partial_within.source, partial_within.target)
    all_nodes = (node for path in simple_paths for node in path)
    nodes_within_boundary = set(all_nodes)
    outside_boundary_nodes = (node
                              for node in hypothgraph.nodes_iter()
                              if not node in nodes_within_boundary)

    outside_evidence_nodes = partial_within.evidenced_nodes + list(outside_boundary_nodes)

    # create new hypothesis configuration
    new_conf = Hypoth_Conf(source=partial_within.source,
                           target=partial_within.target,
                           evidenced_nodes=outside_evidence_nodes)

    after_confidence       =  compute_confidence.confidence(hypothgraph, new_conf)
    after_max_confidence   =  compute_confidence.max_confidence(hypothgraph, new_conf.source, new_conf.target)
    after_norm_confidence  =  compute_confidence.normalized_confidence(hypothgraph, new_conf)

    assert before_confidence == after_confidence
    assert before_max_confidence == after_max_confidence
    assert before_norm_confidence == after_norm_confidence
