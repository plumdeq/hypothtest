# coding: utf8
"""
Evaluate confidence in the given causal chain

:author: Asan Agibetov

"""
from operator import itemgetter

from hypotest.study_planning import find_missing_nodes
from hypotest.assert_evidence import assert_evidence, unassert_evidence
from hypotest.utils import find_node_name


def default_fn_importance(H, node):
    """
    Compute importance factor for given node

    """
    return H.node[node]["evidenced"] * \
        H.node[node]["computed importance factor"]


def evaluate_confidence_for_causal_chain(H, causal_chain,
                                         fn_importance=default_fn_importance):
    """
    (graph, path, func) -> (int)

    Propage confidence factor for a given causal chain

    H
        hypothesis graph

    causal_chain
        a path - list of nodes

    fn_importance (optional)
        function which chooses how to compute confidence for one node


    """
    # if no evidence then confidence is the lowest
    if not causal_chain:
        return -100

    confidence_measures = [fn_importance(H, node) for node in causal_chain]

    return sum(confidence_measures)


def difference_importance(H, causal_chain, log=False):
    """
    (graph, path) -> float

    Assess the importance of evidenced facts in the causal chain

    """
    confidence_with = evaluate_confidence_for_causal_chain(H, causal_chain)
    confidence_without = evaluate_confidence_for_causal_chain(H, [])

    if log:
        print("missing nodes {}".format(list(find_missing_nodes(H))))
        print("with confidence - {}, without - {}".format(confidence_with,
                                                          confidence_without))

    return confidence_with - confidence_without


def most_informative_missing_node(H, causal_chain,
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
        assert_evidence(H, missing_node)
        most_informative[find_node_name(missing_node, H)] = \
            difference_importance(H, causal_chain, log=True)
        unassert_evidence(H, missing_node)

    sorted_most_informative = sorted(most_informative.items(),
                                     key=itemgetter(1),
                                     reverse=True)

    return sorted_most_informative
