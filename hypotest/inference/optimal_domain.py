# coding: utf8
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

Experiments finding the best domain

For a given configuration of a hypothesis, and given evidenced nodes, find the
best endpoints (given the confidence function)

"""
import networkx as nx
import itertools as it
from collections import namedtuple
from operator import attrgetter


from hypotest import assert_endpoints
from hypotest import confidence_propagation as cp
from hypotest import utils


DomainStats = namedtuple('DomainStats', ['source', 'target', 'confidence',
                                         'conf_delta', 'distance',
                                         'dist_delta'])


def optimal_domain(H, threshold=0.0):
    """
    (hypothgraph) -> sorted({[(source, target): confidence, ... }])

    We try all possible combinations of (source, target) pair - boundaries or
    limits of the hypothesis confidence propagation, and see which ones are the
    best or are above a given threshold

    """
    # make all experiments on a copy of the hypothesis graph
    H = H.copy()

    domains_stats = []

    # optimization for already tried endpoints
    simulated_endpoints = []

    source, target = utils.find_causal_endpoints(H)

    # we need to compare with the current confidence and distance
    current_confidence = cp.paths_confidence(H, source, target)
    current_distance = nx.shortest_path_length(H, source, target)

    for s, t in generate_endpoints(H):
        if not (s, t) in simulated_endpoints:

            try:
                # assign new endpoints
                new_source, new_target = utils.sort_endpoints(H, s, t)
                assert_endpoints.assert_endpoints(H, new_source, new_target)

                new_confidence = cp.paths_confidence(H, new_source, new_target)
                new_distance = nx.shortest_path_length(H, new_source,
                                                       new_target)

                # increase or decrease in confidence, for the new domain
                conf_delta = new_confidence - current_confidence
                dist_delta = new_distance - current_distance

                # increase or decrease in distance, and in confidence
                stats = {
                    'confidence': new_confidence,
                    'distance': new_distance,
                    'conf_delta': conf_delta,
                    'dist_delta': dist_delta,
                    'source': new_source,
                    'target': new_target
                }

                domains_stats.append(DomainStats(**stats))

            except Exception as e:
                print(e)

    return sort_domains_stats(domains_stats)


def sort_domains_stats(domains_stats):
    """
    Sorts domains stats according to the confidence (desc)

    """
    return sorted(domains_stats, key=attrgetter('confidence'), reverse=True)


def generate_endpoints(H):
    """
    (hypothgraph) -> [(source, target),... ]

    N choose 2 (combination) on all the nodes from H

    """
    nodes = H.nodes()

    return it.combinations(nodes, 2)
