# coding utf-8
"""
Utils module, i.e., transformations of strings, urls etc.

:author: Asan Agibetov

"""
import networkx as nx
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
    source, target = [n
                      for (n, d) in H.nodes_iter(data=True)
                      if d['causal_endpoint'] == 1]

    source, target = sort_endpoints(H, source, target)

    return source, target


def sort_endpoints(H, u, v):
    """
    (hypothgraph, endpoint1, endpoint2) -> sorted(endpoint1, endpoint2)

    We run the topological sort on H and make sure that u and v are correctly
    sorted

    """
    topol_sorted = nx.topological_sort(H)
    u_index, v_index = topol_sorted.index(u), topol_sorted.index(v)

    source, target = (u, v) if u_index < v_index else (v, u)

    if not nx.has_path(H, source, target):
        raise Exception("No path between {} and {}".format(source, target))

    return source, target


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
