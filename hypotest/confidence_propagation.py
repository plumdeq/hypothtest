# coding: utf8
"""
Evaluate confidence in the given causal chain

:author: Asan Agibetov

"""
from hypotest.study_planning import find_missing_nodes


def default_fn_importance(H, node):
    """
    Compute importance factor for given node

    """
    return H.node[node]["evidenced"] * \
        H.node[node]["computed importance factor"]


def evaluate_confience_for_causal_chain(H, causal_chain,
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
    confidence_measures = [fn_importance(H, node) for node in causal_chain]

    return sum(confidence_measures)


def difference_importance(H, causal_chain):
    """
    (graph, path) -> float

    Assess the importance of evidenced facts in the causal chain

    """
    missing_nodes = find_missing_nodes(H)
    confidence_with = evaluate_confience_for_causal_chain(H, causal_chain)
    confidence_without = evaluate_confience_for_causal_chain(H, missing_nodes)

    return confidence_with - confidence_without


def most_informative_missing_node(H, causal_chain,
                                  fn_importance=default_fn_importance):
    """
    Simulate finding an evidence for one missing node, and assess the difference
    importance

    """
    pass
