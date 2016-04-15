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
