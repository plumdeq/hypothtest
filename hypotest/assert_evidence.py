# coding: utf8
"""
Simulate inputing evidence from the user

:author: Asan Agibetov

"""


def assert_evidence(g, node):
    """
    Assert evidence in graph ``g``. A controller for the event, in case more
    complex logic is required

    """
    g.node[node]["evidenced"] = 1

    return g


def unassert_evidence(g, node):
    """Unassert evidence for node"""
    g.node[node]["evidenced"] = -1

    return g
