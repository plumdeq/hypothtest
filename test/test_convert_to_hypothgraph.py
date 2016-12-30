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

# ## Test convert to hypothgraph
#
# Make hypoth graph creates a hypothesis graph from any directed graph, here we
# make sure that this graph contains the necessary structure.
from hypotest.setup_hypothgraph import convert_to_hypothgraph

# ## Fixtures
import pytest


# Create a very simple digraph, which we will later convert into a hypothgraph
@pytest.fixture
def get_complete_graph():
    complete_graph = nx.complete_graph(10)
    directed_graph = complete_graph.to_directed()

    return directed_graph


def test_convert_to_hypothgraph(get_complete_graph):
    digraph = get_complete_graph
    # assert there are no computed meta data like `evidence_weight` etc.
    for node, node_data in digraph.nodes_iter(data=True):
        assert not 'evidence_weight' in node_data
        assert not 'importance_weight' in node_data

    hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(digraph)

    # every node should have computed btwin_centrality
    for node, node_data in hypothgraph.nodes_iter(data=True):
        assert 'evidence_weight' in node_data
        assert 'importance_weight' in node_data

    # any hypotehsis_source?
    any_source = ('hypothesis_source' in node_data
                  for node, node_data in hypothgraph.nodes_iter(data=True))
    assert any(any_source)

    # any hypothesis_target?
    any_target = ('hypothesis_target' in node_data
                  for node, node_data in hypothgraph.nodes_iter(data=True))
    assert any(any_target)
