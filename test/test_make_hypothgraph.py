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

# ## Test make hypothgraph
#
# Make hypoth graph creates a hypothesis graph from any directed graph, here we
# make sure that this graph contains the necessary structure.
from hypotest.setup_hypothgraph import sample_hypothgraph, utils
from grontocrawler.sample_ontology.hypo_ontology import g
from grontocrawler.graph import produce_graph

# ## Fixtures
import pytest


# uses grontocrawler to produce a digraph
@pytest.fixture
def get_digraph():
    return sample_hypothgraph.get_digraph()


def test_setup_hypothgraph(get_digraph):
    digraph = get_digraph

    # no boundaries before
    before_endpoints = utils.hypothesis_boundary(digraph)

    assert not before_endpoints

    hypothgraph = sample_hypothgraph.make_hypothgraph(digraph)

    # hypothesis configuration boundaries are assigned
    source, target = utils.hypothesis_boundary(hypothgraph)
    assert not source == None
    assert not target == None

    # both are different and there is a path between them
    assert source != target
    assert nx.has_path(hypothgraph, source, target)
