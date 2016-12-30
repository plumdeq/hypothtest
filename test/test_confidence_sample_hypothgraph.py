#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# same old trick to put this directory into the path
import os
import sys

import random
import networkx as nx

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
mypath = os.path.join(dirname, '..')
mypath = os.path.abspath(mypath)
sys.path.insert(0, mypath)

# # Testing confidence computation for sample hypothesis graph

# Sample hypothesis graph contains cycles
#
from hypotest.confidence import compute_confidence, hypoth_conf, boundary
from hypotest.setup_hypothgraph import sample_graphs

# ## Fixtures
import pytest

Hypoth_Conf = hypoth_conf.Hypoth_Conf

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
#
# Our test graph function, gives us a simple path graph and a set of
# hypothesis configurations
@pytest.fixture
def get_sample_hypothgraph_and_configurations():
    hypothgraph     =  sample_graphs.sample_hypothgraph()

    source, target  =  hypoth_conf.generate_reach_endpoints(hypothgraph)

    partial_nodes   =  list(boundary.partial_nodes_boundary_interior(hypothgraph, source, target))
    full_nodes      =  list(boundary.in_boundary_interior(hypothgraph, source, target))

    nothing         =  Hypoth_Conf(source=source, target=target, evidenced_nodes=[])
    partial         =  Hypoth_Conf(source=source, target=target, evidenced_nodes=partial_nodes)
    full            =  Hypoth_Conf(source=source, target=target, evidenced_nodes=full_nodes)

    return {
        'hypothgraph': hypothgraph,
        'nothing': nothing,
        'partial_within': partial,
        'full_within': full
    }


# ### Nothing evidenced on path graph
#
# Confidence with no nodes evidenced should be strictly smaller than the max
# possible confidence
def test_nothing_evidenced_on_path_graph(get_sample_hypothgraph_and_configurations):
    test_data   = get_sample_hypothgraph_and_configurations
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
def test_partial_evidenced_within_on_path_graph(get_sample_hypothgraph_and_configurations):
    test_data      = get_sample_hypothgraph_and_configurations
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
def test_full_evidenced_within_on_path_graph(get_sample_hypothgraph_and_configurations):
    test_data   = get_sample_hypothgraph_and_configurations
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
def test_evidenced_outside_on_path_graph(get_sample_hypothgraph_and_configurations):
    test_data      = get_sample_hypothgraph_and_configurations
    hypothgraph    = test_data['hypothgraph']
    partial_within = test_data['partial_within']
    source         = partial_within.source
    target         = partial_within.target

    before_confidence       =  compute_confidence.confidence(hypothgraph, partial_within)
    before_max_confidence   =  compute_confidence.max_confidence(hypothgraph, source, target)
    before_norm_confidence  =  compute_confidence.normalized_confidence(hypothgraph, partial_within)

    # Evidence nodes which will not contribute to the causation confidence
    on_boundary_nodes = boundary.on_boundary(hypothgraph, source, target)
    outside_evidence_nodes = partial_within.evidenced_nodes + list(on_boundary_nodes)

    # create new hypothesis configuration
    new_conf = Hypoth_Conf(source=source,
                           target=target,
                           evidenced_nodes=outside_evidence_nodes)

    after_confidence       =  compute_confidence.confidence(hypothgraph, new_conf)
    after_max_confidence   =  compute_confidence.max_confidence(hypothgraph, source, target)
    after_norm_confidence  =  compute_confidence.normalized_confidence(hypothgraph, new_conf)

    assert before_confidence == after_confidence
    assert before_max_confidence == after_max_confidence
    assert before_norm_confidence == after_norm_confidence

