#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
author: Asan Agibetov

   Copyright 2015-2017 Asan Agibetov <asan.agibetov@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from rdflib import namespace

POSITIVE_PREFIX = 'Positive_regulation_of_'
NEGATIVE_PREFIX = 'Negative_regulation_of_'
#
# # Normalize nodes
#
# check if node_id is normalized, i.e., has `Positive_regulation_of` or
# `Negative_regulation_of`, by default we transform into `Positive_regulation_of`
def normalize_node_id(node_id, prefix_key='pos'):
    """
    Normalizes the id and the label of the node and adds in a list the
    normalized node. Note that the list is MUTATED

    (URIRef, list, [str]) -> ('Positively_regulation_of' | 'Negative_regulation_of_' + URIRef, label)

    """
    node_id = unicode(node_id)
    prefix = POSITIVE_PREFIX

    if prefix_key == 'neg':
        prefix = NEGATIVE_PREFIX

    new_node_id = ''

    if not node_id.find(POSITIVE_PREFIX) == -1 or \
            not node_id.find(NEGATIVE_PREFIX) == -1:

        return node_id

    # assume that all ids are URIs of type `http://muliscale.ch/label`
    ns, qname = namespace.split_uri(node_id)
    new_qname = ''.join([prefix, qname])

    new_node_id = ''.join([ns, new_qname])

    return new_node_id


def normalize_node_label(normalized_id):
    """
    Replace all '_' with ' ' in the `node_id`

    (URIRef) -> ('Positively_regulation_of' + label)

    """
    # ensure `normalized_id` is unicode
    normalized_id = unicode(normalized_id)

    ns, label = namespace.split_uri(normalized_id)

    label = label.replace('_', ' ')

    return str(label)
