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

# # Testing boundary of the hypothesis graph

# Boundary of the hypothesis graph depends on the hypothesis configuration.
# Nodes in the boundary interior are all the nodes which can be accessed from
# the hypothesis configuration source node. Nodes on the boundary are all nodes
# which are not in the interior of the boundary
from hypotest.setup_hypothgraph import convert_to_hypothgraph
from hypotest.confidence import boundary

# ## Fixtures
import pytest


# This graph is complete among 0..4 nodes, and then we add a little tail up to
# node 9
@pytest.fixture
def get_digraph_with_cycle():
    digraph = nx.complete_graph(5, create_using=nx.DiGraph())
    digraph.add_path(xrange(4, 10))

    hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(digraph)
    source = 0
    target = 5

    return hypothgraph, source, target


# Testing the digraph with a cycle, nodes in the boundary interior are all
# nodes accessible from source to target of the hypothesis configuration
def test_nodes_inside_boundary(get_digraph_with_cycle):
    hypothgraph, source, target = get_digraph_with_cycle

    # all nodes within boundary are accessible from source
    nodes_in_boundary_interior = boundary.in_boundary_interior(hypothgraph, source, target)
    for node_inside_boundary in nodes_in_boundary_interior:
        assert nx.has_path(hypothgraph, source, node_inside_boundary)


# Nodes on the boundary are all the nodes which are not in the boundary
# interior
def test_nodes_on_boundary(get_digraph_with_cycle):
    hypothgraph, source, target = get_digraph_with_cycle

    nodes_on_boundary = boundary.on_boundary(hypothgraph, source, target)
    nodes_in_boundary_interior = list(boundary.in_boundary_interior(hypothgraph, source, target))

    for node_on_boundary in nodes_on_boundary:
        assert not node_on_boundary in nodes_in_boundary_interior


def test_partial_in_boundary(get_digraph_with_cycle):
    hypothgraph, source, target = get_digraph_with_cycle

    nodes_in_boundary_interior = list(boundary.in_boundary_interior(hypothgraph, source, target))
    nodes_partial_in_boundary = list(boundary.partial_nodes_boundary_interior(hypothgraph, source, target))

    assert len(nodes_partial_in_boundary) < len(nodes_in_boundary_interior)

    for partial_node in nodes_partial_in_boundary:
        assert partial_node in nodes_in_boundary_interior
