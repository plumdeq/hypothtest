# coding: utf8
"""
Perform experiments

For a given configuration of a hypothesis, try the following experiments:

1) Generalization of a hypothesis, i.e. grow one or two end (s) of the boundary
   and see how the confidence changes
2) For given unevidenced nodes, find the best endpoints (given the confidence
   function)
3) For a given threshold of confidence, find the best hypothesis configuration

:author: Asan Agibetov

"""
import networkx as nx
from collections import namedtuple

from hypotest import utils
from hypotest import confidence_propagation as cp

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
    (hypothgraph) -> (source, target, increase in nodes, new confidence, delta
                      confidence)

    We identify endpoints, and then we try to *grow* the boundary (predecessors
    for the source, successors for target) and recompute the confidence function

    """
    b1, b2 = utils.find_causal_endpoints(H)
    # identify which is source, which is target
    source, target = (b1, b2) if b1 < b2 else (b2, b1)

    preds = H.predecessors(source)
    succs = H.successors(target)

    return (preds, succs)
