#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# occ1 - neg -> occ2, should give occ1 - result in -> neg reg of occ2
import pytest

import networkx as nx

from hypotest.setup_hypothgraph import convert_to_hypothgraph
from hypotest.setup_hypothgraph import normalize
from grontocrawler.utils import graph_utils

@pytest.fixture
def get_simple_unnormalized():
    nodes = [
        (u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction',
            { 'label': 'TNF alpha overproduction' }),
        (u'http://plumdeq.xyz/hypothesis/Chondrocytes_anabolism',
            { 'label': 'Chondrocytes anabolism' }),
        (u'http://plumdeq.xyz/hypothesis/Proteoglycan_production',
            { 'label': 'Proteoglycan production' })
    ]

    arcs = [
        (u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction',
         u'http://plumdeq.xyz/hypothesis/Chondrocytes_anabolism',
         { 'label': 'negatively regulates' }),
        (u'http://plumdeq.xyz/hypothesis/Chondrocytes_anabolism',
         u'http://plumdeq.xyz/hypothesis/Proteoglycan_production',
         { 'label': 'positively regulates' })
    ]

    unnormalized = nx.DiGraph()
    unnormalized.add_nodes_from(nodes)
    unnormalized.add_edges_from(arcs)

    unnormalized = convert_to_hypothgraph.convert_to_hypothgraph(unnormalized)

    expected_nodes = [
        (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction',
         { 'label': 'Positive regulation of TNF alpha overproduction' }),
        (u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_Chondrocytes_anabolism',
         { 'label': 'Negative regulation of Chondrocytes anabolism' }),
        (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_Proteoglycan_production',
         { 'label': 'Positive regulation of Proteoglycan production' })
    ]

    expected_arcs = [
        (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction',
         u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_Chondrocytes_anabolism',
         { 'label': 'results in' }),
        (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_Chondrocytes_anabolism',
         u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_Proteoglycan_production',
         { 'label': 'results in' })
    ]

    return unnormalized, expected_nodes, expected_arcs


def test_normalize_node_id():
    node_id1 = u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction'
    expected_id1 = u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction'
    normalized_id1 = normalize.normalize_node_id(node_id1)

    assert normalized_id1 == expected_id1

    node_id2 = u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction'
    expected_id2 = u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_TNF_alpha_overproduction'
    normalized_id2 = normalize.normalize_node_id(node_id2, prefix_key='neg')

    assert normalized_id2 == expected_id2

def test_normalize_node_label():
    normalized_id1 = u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction'
    expected_label1 = 'Positive regulation of TNF alpha overproduction'

    normalized_label1 = normalize.normalize_node_label(normalized_id1)

    assert normalized_label1 == expected_label1

    normalized_id2 = u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_TNF_alpha_overproduction'
    expected_label2 = 'Negative regulation of TNF alpha overproduction'

    normalized_label2 = normalize.normalize_node_label(normalized_id2)

    assert normalized_label2 == expected_label2


def test_normalize_node():
    node1 = (u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction',
                { 'label': 'TNF alpha overproduction' })

    expected_node1 = (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction',
                        { 'label': 'Positive regulation of TNF alpha overproduction' })

    received_node1 = normalize.normalize_node(node1)

    assert graph_utils.are_same_nodes(received_node1, expected_node1)

    node2 = (u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction',
                { 'label': 'TNF alpha overproduction' })

    expected_node2 = (u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_TNF_alpha_overproduction',
                        { 'label': 'Negative regulation of TNF alpha overproduction' })

    received_node2 = normalize.normalize_node(node2, prefix_key='neg')

    assert graph_utils.are_same_nodes(received_node2, expected_node2)


def test_normalized_arc():
    arc1 = (u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction',
            u'http://plumdeq.xyz/hypothesis/Chondrocytes_anabolism',
            { 'label': 'negatively regulates' })


    expected_arc1 = (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction',
                     u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_Chondrocytes_anabolism',
                     { 'label': 'results in' })

    arc2 = (u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction',
            u'http://plumdeq.xyz/hypothesis/Chondrocytes_anabolism',
            { 'label': 'positively regulates' })

    expected_arc2 = (u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction',
                     u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_Chondrocytes_anabolism',
                     { 'label': 'results in' })

    arc3 = (u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_TNF_alpha_overproduction',
            u'http://plumdeq.xyz/hypothesis/Chondrocytes_anabolism',
            { 'label': 'negatively regulates' })

    expected_arc3 = (u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_TNF_alpha_overproduction',
                     u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_Chondrocytes_anabolism',
                     { 'label': 'results in' })

    arc4 = (u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_TNF_alpha_overproduction',
            u'http://plumdeq.xyz/hypothesis/Chondrocytes_anabolism',
            { 'label': 'positively regulates' })

    expected_arc4 = (u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_TNF_alpha_overproduction',
                     u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_Chondrocytes_anabolism',
                     { 'label': 'results in' })

    received_arc1 = normalize.normalize_arc(arc1)
    received_arc2 = normalize.normalize_arc(arc2)
    received_arc3 = normalize.normalize_arc(arc3)
    received_arc4 = normalize.normalize_arc(arc4)

    assert graph_utils.are_same_edges(received_arc1, expected_arc1)
    assert graph_utils.are_same_edges(received_arc2, expected_arc2)
    assert graph_utils.are_same_edges(received_arc3, expected_arc3)
    assert graph_utils.are_same_edges(received_arc4, expected_arc4)


def test_simple_graph_pattern(get_simple_unnormalized):
    simple_unnormalized, expected_nodes, expected_arcs = get_simple_unnormalized

    # check that we obtain the expected arcs
    simple_normalized = normalize.normalize_hypothgraph(simple_unnormalized)

    for arc in expected_arcs:
        assert graph_utils.is_edge_in_edges(
                arc, simple_normalized.edges_iter(data=True))
