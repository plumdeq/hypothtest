# coding: utf8
"""
Evaluate confidence in the given causal chain

:author: Asan Agibetov

"""
from operator import itemgetter
import networkx as nx

from hypotest.study_planning import find_missing_nodes
from hypotest.assert_evidence import assert_evidence, unassert_evidence
from hypotest.utils import find_node_name

MIN_CONFIDENCE = -100


def default_fn_importance(H, node):
    """
    Compute importance factor for given node

    """
    return H.node[node]["evidenced"] * \
        H.node[node]["computed importance factor"]


def path_confidence(H, path, fn_importance=default_fn_importance):
    """
    (hypothgraph, path) -> float

    H
        hypothesis graph
    path
        list of nodes

    fn_importance (optional)
        function which chooses how to compute confidence for one node

    """
    if not path:
        return MIN_CONFIDENCE

    confidence_measures = [fn_importance(H, node) for node in path]

    return sum(confidence_measures)


def paths_confidence(H, source, target,
                     fn_importance=default_fn_importance,
                     log=False):
    """
    (graph, source, target, func) -> (int)

    Propagate confidence factor for given source and target nodes

    H
        hypothesis graph

    source, target
        nodes

    """
    # if no evidence then confidence is the lowest
    if source is None or target is None:
        raise Exception("You should provide source and target")

    # compute all paths between source and target
    paths = nx.all_shortest_paths(H, source, target)

    confidence_measures = [path_confidence(H, path, fn_importance=fn_importance)
                           for path in paths]

    if log:
        print("confidence measures are {}".format(confidence_measures))

    return sum(confidence_measures)/float(len(confidence_measures))


def difference_importance(H, source, target, candidate_evidenced_node,
                          fn_importance=default_fn_importance, log=False):
    """
    (graph, path) -> float

    Compute difference in confidence value with or without candidate evidenced
    node

    """
    confidence_without = paths_confidence(H, source, target,
                                          fn_importance=fn_importance)

    assert_evidence(H, candidate_evidenced_node)
    confidence_with = paths_confidence(H, source, target,
                                       fn_importance=fn_importance)
    unassert_evidence(H, candidate_evidenced_node)

    gain_in_confidence = abs(confidence_with - confidence_without)

    if log:
        print("missing nodes {}".format(list(find_missing_nodes(H))))
        print("candidate evidenced node {}".format(candidate_evidenced_node))
        print("with confidence - {}, without - {}".format(confidence_with,
                                                          confidence_without))
        print("gain in confidence: {}".format(gain_in_confidence))

    return gain_in_confidence


def most_informative_missing_node(H, source, target,
                                  fn_importance=default_fn_importance):
    """
    (hypothgraph, path) -> missing_node_id

    Simulate finding an evidence for one missing node, and assess the difference
    importance

    """
    missing_nodes = find_missing_nodes(H)
    most_informative = {}

    for missing_node in missing_nodes:
        # evidence him and compute overall confidence
        most_informative[find_node_name(missing_node, H)] = \
            difference_importance(H, source, target, missing_node)

    sorted_most_informative = sorted(most_informative.items(),
                                     key=itemgetter(1),
                                     reverse=True)

    return sorted_most_informative
