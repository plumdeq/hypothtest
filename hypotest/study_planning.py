# coding: utf8
"""
Find missing nodes in the causal chain

Basically iterate via all nodes attributes, and find those factors which have
not been evidenced

:author: Asan Agibetov

"""


def find_missing_nodes(H):
    """Find all non-evidenced nodes"""
    return (n for (n, d) in H.nodes_iter(data=True) if d["evidenced"] != 1)
