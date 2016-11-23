# coding: utf8
"""
Common functions for all stats printing scripts

:author: Asan Agibetov

"""
from hypotest import assert_endpoints
from hypotest import assert_evidence


def preapre_hypothesis_graph(H, endpoints=None, evidenced_nodes=None):
    """
    Makes a copy of the hypothesis graph, and asserts endpoints (if any), as
    well as the evidenced nodes

    """
    H1 = H.copy()

    if endpoints:
        try:
            assert_endpoints.assert_endpoints(H1, *endpoints)
        except Exception as e:
            print(e)
            return e

    if evidenced_nodes:
        for evidenced_node in evidenced_nodes:
            assert_evidence.assert_evidence(H1, evidenced_node)

    return H1
