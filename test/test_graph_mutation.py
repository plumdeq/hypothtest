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

# # Testing graph mutation functions

# Make hypoth graph creates a hypothesis graph from any directed graph, here we
# make sure that this graph contains the necessary structure.
from hypotest.setup_hypothgraph import sample_graphs, convert_to_hypothgraph

# ## Fixtures
import pytest


# uses grontocrawler to produce a digraph
@pytest.fixture
def get_digraph():
    return sample_graphs.sample_digraph()

@pytest.fixture
def get_hypothgraph():
    return sample_graphs.sample_hypothgraph()


# hypothgraph has 'importance_weight' assigned to every node
def test_importance_weights_hypothgraph(get_hypothgraph):
    hypothgraph = get_hypothgraph

    # every node should have computed btwin_centrality
    for node, node_data in hypothgraph.nodes_iter(data=True):
        assert 'importance_weight' in node_data
        # weight should be in 0..1
        weight = node_data['importance_weight']
        assert weight >= 0 and weight <= 1


# hypothgraph should have 'evidence measure' assigned to every node
def test_evidence_weights_hypothgraph(get_hypothgraph):
    hypothgraph = get_hypothgraph

    # every node should have computed btwin_centrality
    for node, node_data in hypothgraph.nodes_iter(data=True):
        assert 'evidence_weight' in node_data
