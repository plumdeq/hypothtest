#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Normalizing causal chains
#
# 1. You need to go through every arc and check the label of the arc
#   1.a) label is 'linear' ('results in' or 'causes') then, we are either at
#        the beginning of the unnormalized chain, or in the end
#       1.a.a) [begining of unnormalized chain] check if `target` participates
#               in any relation of type 'neg' or 'pos', and if yes then transform
#               'target' -> 'positive regulation of target' for all outgoing arcs
#       1.a.b) [end of unnormalized chain] check if `source`
#
#   1.b) label is 'neg' or 'pos' then we are in the unnormalized chain, we rewrite both `source` and `target`
#        according to the type of the relation of the arc. Then we check
#        whether we can normalize the end.
#       1.b.a) [begining of unnormalized chain] check if `target` participates
#               in any relation of type 'neg' or 'pos', and if yes then transform
#               'target' -> 'positive regulation of target' for all outgoing arcs
from grontocrawler.utils import graph_utils
from hypotest.graph_mutation import normalize_hypothgraph

import pytest
import networkx as nx


@pytest.fixture
def get_chained_neg():
    nodes = [
        (u'http://plumdeq.xyz/hypothesis/Synovial_inflamation',
            { 'label': 'Synovial inflammation' }),
        (u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction',
            { 'label': 'TNF alpha overproduction' }),
        (u'http://plumdeq.xyz/hypothesis/Chondrocytes_anabolism',
            { 'label': 'Chondrocytes anabolism' }),
        (u'http://plumdeq.xyz/hypothesis/Proteoglycan_production',
            { 'label': 'Proteoglycan production' }),
    ]

    arcs = [
        (u'http://plumdeq.xyz/hypothesis/Synovial_inflamation',
         u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction',
         { 'label': 'results in' }),
        (u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction',
         u'http://plumdeq.xyz/hypothesis/Chondrocytes_anabolism',
         { 'label': 'negatively regulates' }),
        (u'http://plumdeq.xyz/hypothesis/Chondrocytes_anabolism',
         u'http://plumdeq.xyz/hypothesis/Proteoglycan_production',
         { 'label': 'results in' }),
    ]

    unnormalized = nx.DiGraph()
    unnormalized.add_nodes_from(nodes)
    unnormalized.add_edges_from(arcs)

    expected_nodes = [
        (u'http://plumdeq.xyz/hypothesis/Synovial_inflamation',
            { 'label': 'Synovial inflamation' }),
        (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction',
         { 'label': 'Positive regulation of TNF alpha overproduction' }),
        (u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_Chondrocytes_anabolism',
         { 'label': 'Negative regulation of Chondrocytes anabolism' }),
        (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_Chondrocytes_anabolism',
         { 'label': 'Positive regulation of Chondrocytes anabolism' }),
    ]

    expected_arcs = [
        (u'http://plumdeq.xyz/hypothesis/Synovial_inflamation',
         u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction',
         { 'label': 'results in' }),
        (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction',
         u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_Chondrocytes_anabolism',
         { 'label': 'results in' }),
        (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_Chondrocytes_anabolism',
         u'http://plumdeq.xyz/hypothesis/Proteoglycan_production',
         { 'label': 'results in' })
    ]

    return unnormalized, expected_nodes, expected_arcs


# occ1 - results in -> occ2 - neg -> occ3 should give us
# * occ1 - results in -> pos of occ2
# * occ2 - results in -> neg of occ3
def test_normalize_chained_neg(get_chained_neg):
    unnormalized, expected_nodes, expected_arcs = get_chained_neg
    normalized, normalized_nodes = normalize_hypothgraph.normalize_hypothgraph(unnormalized)

    # we obtain same nodes
    for expected_node in expected_nodes:
        assert graph_utils.is_node_in_nodes(expected_node, normalized.nodes_iter(data=True))

    # we obtain same edges
    for expected_arc in expected_arcs:
        assert graph_utils.is_edge_in_edges(expected_arc, normalized.edges_iter(data=True))
