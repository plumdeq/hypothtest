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

# ## Test sample hypothgraph
#
# Sample hypothgraph, checking whether it works
from hypotest.setup_hypothgraph import sample_graphs

# ## Fixtures
import pytest


# uses grontocrawler to produce a digraph
@pytest.fixture
def get_hypothgraph():
    return sample_graphs.sample_hypothgraph()


# hypothgraph should have 'evidence measure', 'importance measure' assigned to
# every node. It should also have 'hypothesis source' and 'hypothesis target'
def test_annotations_hypothgraph(get_hypothgraph):
    hypothgraph = get_hypothgraph

    # every node should have computed btwin_centrality
    for node, node_data in hypothgraph.nodes_iter(data=True):
        assert 'evidence_weight' in node_data
        assert 'importance_weight' in node_data
