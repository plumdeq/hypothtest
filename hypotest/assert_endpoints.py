# coding: utf8
"""
Simulate inputing evidence from the user for the endpoints

:author: Asan Agibetov

"""
from hypotest import utils


def assert_endpoints(H, new_source, new_target):
    """
    (hypothgraph, new_source, new_target) -> H wnodeith nodes data altered

    """
    # check if the path exists and sort them
    new_source, new_target = utils.sort_endpoints(H, new_source, new_target)

    old_s, old_t = utils.find_causal_endpoints(H)

    # unassert old
    for node in (old_s, old_t):
        unassert_endpoint(H, node)

    # assert new
    for node in (new_source, new_target):
        assert_endpoint(H, node)

    return H


def unassert_endpoint(H, node):
    """
    H.node.causal_endpoint = 0

    """
    H.node[node]['causal_endpoint'] = 0

    return H


def assert_endpoint(H, node):
    """
    H.node.causal_endpoint = 1

    """
    H.node[node]['causal_endpoint'] = 1

    return H
