#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Test relative confidence of a subgraph to a bigger graph
import networkx as nx
import pytest

from hypotest.confidence import compute_confidence
from hypotest.graph_generation import hypoth_conf, boundary, sub_hypothgraph
from hypotest.setup_hypothgraph import sample_graphs

Hypoth_Conf = hypoth_conf.Hypoth_Conf

@pytest.fixture
def get_sample_configuration():
    hypothgraph = sample_graphs.sample_hypothgraph()
    source, target = hypoth_conf.generate_rich_endpoints(hypothgraph)

    subgraph = sub_hypothgraph.generate_sub_hypothgraph(
            hypothgraph, source, target)

    return hypothgraph, subgraph, source, target

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

def test_relative_confidence_richer(get_sample_configuration):
    big, small, source, target = get_sample_configuration

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
