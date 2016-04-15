# coding utf-8
"""
Utils module, i.e., transformations of strings, urls etc.

:author: Asan Agibetov

"""
from functools import wraps


def memo(f):
    """Memoization for function $f$"""
    cache = {}

    @wraps(f)
    def wrap(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    return wrap


def find_node_name(node_id, g):
    """Go through the attributes and find the node with the given name"""
    return g.node[node_id]["label"]


def find_causal_endpoints(H):
    """
    hypothgraph -> (source, target) of causal chain

    Extracts endpoints of the causal chain

    """
    return [n
            for (n, d) in H.nodes_iter(data=True)
            if d['causal_endpoint'] == 1]


def find_missing_nodes(H):
    """
    (hypothgraph) -> iter of missing nodes

    Find all non-evidenced nodes

    """
    return (n for (n, d) in H.nodes_iter(data=True) if d["evidenced"] != 1)


def find_evidenced_nodes(H):
    """
    (hypothgraph) -> iter of evidenced nodes

    Find all evidenced nodes

    """
    return (n for (n, d) in H.nodes_iter(data=True) if d['evidenced'] == 1)
