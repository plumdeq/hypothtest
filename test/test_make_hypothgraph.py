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

# ## Test make hypothgraph
#
# Make hypoth graph creates a hypothesis graph from any directed graph, here we
# make sure that this graph contains the necessary structure.
from hypotest.setup_hypothgraph import make_hypograph

# ## Fixtures
import pytest


# uses grontocrawler to produce a digraph
@pytest.fixture
def get_digraph():
    return make_hypograph()


def test_setup_hypothgraph(get_digraph):
    digraph = get_digraph

    before_endpoints = len([(n, d) for n, d in digraph.nodes_iter(data=True)
                                   if 'causal_endpoint' in d ])

    assert before_endpoints == 0
