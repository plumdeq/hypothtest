#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Boundary computation for the hypothgraph methods
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

# # Testing hypothesis configuration

from hypotest.setup_hypothgraph import convert_to_hypothgraph
from hypotest.confidence import hypoth_conf

# ## Fixtures
import pytest
import itertools as it


# This graph is complete among 0..4 nodes, and then we add a little tail up to
# node 9
@pytest.fixture
def get_digraph_with_cycle():
    digraph = nx.complete_graph(5, create_using=nx.DiGraph())
    digraph.add_path(xrange(4, 10))

    hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(digraph)

    return hypothgraph


def test_generate_rich_endpoints(get_digraph_with_cycle):
    hypothgraph = get_digraph_with_cycle

    # just run 100 tests
    for _ in xrange(100):
        source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)
        all_simple_paths = list(nx.all_simple_paths(hypothgraph, source, target))
        assert len(all_simple_paths) >= 2
