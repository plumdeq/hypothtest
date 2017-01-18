#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# occ1 - neg -> occ2, should give occ1 - result in -> neg reg of occ2
import pytest

import networkx as nx

from grontocrawler.utils import graph_utils
from hypotest.graph_mutation import (normalize_arc, normalize_node)



def test_normalize_node_id():
    node_id1 = u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction'
    expected_id1 = u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction'
    normalized_id1 = normalize_node.normalize_node_id(node_id1)

    assert normalized_id1 == expected_id1

    node_id2 = u'http://plumdeq.xyz/hypothesis/TNF_alpha_overproduction'
    expected_id2 = u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_TNF_alpha_overproduction'
    normalized_id2 = normalize_node.normalize_node_id(node_id2, prefix_key='neg')

    assert normalized_id2 == expected_id2

def test_normalize_node_label():
    normalized_id1 = u'http://plumdeq.xyz/hypothesis/Positive_regulation_of_TNF_alpha_overproduction'
    expected_label1 = 'Positive regulation of TNF alpha overproduction'

    normalized_label1 = normalize_node.normalize_node_label(normalized_id1)

    assert normalized_label1 == expected_label1

    normalized_id2 = u'http://plumdeq.xyz/hypothesis/Negative_regulation_of_TNF_alpha_overproduction'
    expected_label2 = 'Negative regulation of TNF alpha overproduction'

    normalized_label2 = normalize_node.normalize_node_label(normalized_id2)

    assert normalized_label2 == expected_label2


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

    received_arc1 = normalize_arc.normalize_non_linear_arc(arc1, [])
    received_arc2 = normalize_arc.normalize_non_linear_arc(arc2, [])
    received_arc3 = normalize_arc.normalize_non_linear_arc(arc3, [])
    received_arc4 = normalize_arc.normalize_non_linear_arc(arc4, [])

    assert graph_utils.are_same_edges(received_arc1, expected_arc1)
    assert graph_utils.are_same_edges(received_arc2, expected_arc2)
    assert graph_utils.are_same_edges(received_arc3, expected_arc3)
    assert graph_utils.are_same_edges(received_arc4, expected_arc4)
