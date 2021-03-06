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

Perform experiments

For a given configuration of a hypothesis, try the following experiments:

1) Generalization of a hypothesis, i.e. grow one or two end (s) of the boundary
   and see how the confidence changes
2) For given evidenced nodes, find the best endpoints (given the confidence
   function)
3) For a given threshold of confidence, find the best hypothesis configuration

"""
import networkx as nx
from collections import namedtuple
from operator import attrgetter

from hypotest import utils
from hypotest import confidence_propagation as cp
from hypotest import assert_endpoints

Path = namedtuple('Path', ['confidence', 'conf_delta', 'distance',
                           'dist_delta'])


def generalize_directional(H, source, target, direction='backwards'):
    """
    (hypothgraph, source, backwards or forward) -> {
        'ancestor_i': (confidence(ancestor_i, target),
                       distance(ancestor_i, target)) |
        'descendant_i': (confidence(descendant_i, target),
                       distance(descendant_i, target)) |
        }

    Compute all ancestors or descendants from the source or target node, i.e.,
    all the nodes from which we can reach ``source | target``, and per every
    such farther node compute the distance in number of nodes, the new
    confidence, and the delta increase/decrese

    """
    # make all experiments on a copy of the hypothesis graph
    H = H.copy()

    farther_nodes, from_node = nx.algorithms.ancestors, source
    if direction != 'backwards':
        farther_nodes, from_node = nx.algorithms.descendants, target

    # we need to compare with the current confidence and distance
    current_confidence = cp.paths_confidence(H, source, target)
    current_distance = nx.shortest_path_length(H, source, target)

    generalization = {}

    for farther_node in farther_nodes(H, from_node):
        new_source, new_target = utils.sort_endpoints(H, farther_node, target)
        if direction != 'backwards':
            new_source, new_target = utils.sort_endpoints(H, farther_node,
                                                          source)

        # assign the new endpoints
        assert_endpoints.assert_endpoints(H, new_source, new_target)

        new_confidence = cp.paths_confidence(H, new_source, new_target)
        new_distance = nx.shortest_path_length(H, new_source, new_target)

        # increase or decrease in confidence, when we go farther
        conf_delta = new_confidence - current_confidence
        dist_delta = new_distance - current_distance
        if direction == 'backwards':
            dist_delta *= -1

        # increase or decrease in distance, depending on the direction

        stats = {
            'confidence': new_confidence,
            'distance': new_distance,
            'conf_delta': conf_delta,
            'dist_delta': dist_delta
        }

        generalization[(new_source, new_target)] = Path(**stats)

    return generalization


def generalize(H):
    """
    (hypothgraph) -> list of stats of bi-directional generalization

    We identify endpoints, and then we try to *grow* the boundary (predecessors
    for the source, successors for target) and recompute the confidence function

    """
    source, target = utils.find_causal_endpoints(H)

    # construct the same named tuple with the current state of the hypothesis
    current_confidence = cp.paths_confidence(H, source, target)
    current_distance = nx.shortest_path_length(H, source, target)

    stats = {
        'confidence': current_confidence,
        'distance': current_distance,
        'conf_delta': 0,
        'dist_delta': 0
    }

    current_state = [Path(**stats)]

    # generalize backwards anf forward, sort according to the delta distance
    backwards_gen = generalize_directional(H, source, target)
    forward_gen = generalize_directional(H, source, target,
                                         direction='forward')

    back_gen, forward_gen = [extract_paths_and_sort(backwards_gen),
                             extract_paths_and_sort(forward_gen)]

    return back_gen + current_state + forward_gen


# Utils
def extract_paths_and_sort(generalization_obj, key=attrgetter('dist_delta')):
    """
    generalization is an object, extract list and sort on *dist_delta*

    """
    paths = [path for endpoints, path in generalization_obj.items()]

    return sorted(paths, key=key)


def generalization_data_for_plot(H):
    """
    Returns then necessary data for the generalization

    delta in distance, confidence, delta in confidence


    """
    sorted_paths = generalize(H)

    dist_deltas = [attrgetter('dist_delta')(path) for path in sorted_paths]
    confidences = [attrgetter('confidence')(path) for path in sorted_paths]
    conf_deltas = [attrgetter('conf_delta')(path) for path in sorted_paths]

    stats = {
        'dist_deltas': dist_deltas,
        'confidences': confidences,
        'conf_deltas': conf_deltas
    }

    return stats
