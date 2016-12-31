#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Test relative confidence of a subgraph to a bigger graph
import networkx as nx
import pytest

from hypotest.confidence import compute_confidence, hypoth_conf, boundary
from hypotest.setup_hypothgraph import convert_to_hypothgraph

Hypoth_Conf = hypoth_conf.Hypoth_Conf

# # Relative confidence
#
# Here we compare confidence obtained in the subgraph to that obtained in the
# big graph.
#
# ## Possible configurations
#
# We can have confidence, max_confidence and normalized confidence for two
# different graphs. We can call local the subgraph, and global the big graph.
# Now, how does our local confidence compare to the global one? We can have
# usuall confidence calculation inside local only, which we can compare to the
# global individually, conf_local/conf_global, max_local/max_global,
# norm_local/norm_global. However, conf_local may actually be bigger than
# conf_global, while norm_local should always be lower than norm_global.
#
# ## Test graphs

# ### Trivial example
#
# If you have a subgraph (a, b) only and many paths (a, c, d, b), (a, d, b) in
# the big graph. That is, in the subgraph there is only one way to get to (a,
# b), while in the big graph there are many ways to get from a to b.

@pytest.fixture
def get_trivial_example():
    subgraph = nx.DiGraph()
    subgraph.add_edge(0, 3)

    big_graph = nx.complete_graph(4, create_using=nx.DiGraph())

    source, target = 0, 3

    big_hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(big_graph)
    sub_hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(subgraph)

    # big, small, source, target
    return big_hypothgraph, sub_hypothgraph, source, target

# ### Slightly more complex example
#
# We will have the main graph - a complete graph, and as its subgraph we will
# have a smaller part within the big graph, with some connections to the far
# node of the big graph. So the subgraph will have less paths to the far node
# than the big graph.
@pytest.fixture
def get_richer_example():
    big_graph = nx.complete_graph(10, create_using=nx.DiGraph())
    subgraph = big_graph.subgraph(xrange(4))

    # add some paths to a far node in the big graph
    subgraph.add_edge(2, 6)
    subgraph.add_edge(3, 6)
    subgraph.add_edge(3, 5)
    subgraph.add_edge(5, 6)

    # convert to hypothesis graphs and return
    big_hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(big_graph)
    sub_hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(subgraph)

    # big, small, source, target
    return big_hypothgraph, sub_hypothgraph, 2, 6


def test_relative_confidence_trivial(get_trivial_example):
    big, small, source, target = get_trivial_example

    # generate hypothesis configurations according to the small hypothesis
    nothing_small = Hypoth_Conf(source, target, [])
    partial_small = Hypoth_Conf(source, target,
                        list(boundary.partial_nodes_boundary_interior(small, source, target)))
    full_small    = Hypoth_Conf(source, target,
                        list(boundary.in_boundary_interior(small, source, target)))


    # relative confidence is the normalized confidence in the small
    # hypothegraph to the bigger hypothgraph
    nothing_conf_big   = compute_confidence.normalized_confidence(big, nothing_small)
    nothing_conf_small = compute_confidence.normalized_confidence(small, nothing_small)
    relative_nothing   = abs(nothing_conf_small - nothing_conf_big)

    partial_conf_big   = compute_confidence.normalized_confidence(big, partial_small)
    partial_conf_small = compute_confidence.normalized_confidence(small, partial_small)
    relative_partial   = abs(partial_conf_small - partial_conf_big)

    full_conf_big      = compute_confidence.normalized_confidence(big, full_small)
    full_conf_small    = compute_confidence.normalized_confidence(small, full_small)
    relative_full      = abs(full_conf_small - full_conf_big)

    # with nothing evidenced our confidence should be 0 regardless of the size
    # of the hypothesis
    assert nothing_conf_big == nothing_conf_small == 0

    # with partial nodes smaller hypothesis confidence is at least as big as
    # the confidence in the bigger hypothesis, but usually is bigger
    assert partial_conf_small >= partial_conf_big

    # with full nodes evidenced in the smaller hypothesis, the same
    # configuration in the bigger hypothesis can only give a smaller confidence
    assert full_conf_small >= full_conf_big


def test_relative_confidence_richer(get_richer_example):
    big, small, source, target = get_richer_example

    # generate hypothesis configurations according to the small hypothesis
    nothing_small = Hypoth_Conf(source, target, [])
    partial_small = Hypoth_Conf(source, target,
                        list(boundary.partial_nodes_boundary_interior(small, source, target)))
    full_small    = Hypoth_Conf(source, target,
                        list(boundary.in_boundary_interior(small, source, target)))


    # relative confidence is the normalized confidence in the small
    # hypothegraph to the bigger hypothgraph
    nothing_conf_big   = compute_confidence.normalized_confidence(big, nothing_small)
    nothing_conf_small = compute_confidence.normalized_confidence(small, nothing_small)
    relative_nothing   = abs(nothing_conf_small - nothing_conf_big)

    partial_conf_big   = compute_confidence.normalized_confidence(big, partial_small)
    partial_conf_small = compute_confidence.normalized_confidence(small, partial_small)
    relative_partial   = abs(partial_conf_small - partial_conf_big)

    full_conf_big      = compute_confidence.normalized_confidence(big, full_small)
    full_conf_small    = compute_confidence.normalized_confidence(small, full_small)
    relative_full      = abs(full_conf_small - full_conf_big)

    # with nothing evidenced our confidence should be 0 regardless of the size
    # of the hypothesis
    assert nothing_conf_big == nothing_conf_small == 0

    # with partial nodes smaller hypothesis confidence is at least as big as
    # the confidence in the bigger hypothesis, but usually is bigger
    assert partial_conf_small >= partial_conf_big

    # with full nodes evidenced in the smaller hypothesis, the same
    # configuration in the bigger hypothesis can only give a smaller confidence
    assert full_conf_small >= full_conf_big


# Test monotonicity of relative confidence
