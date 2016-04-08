# coding: utf8
"""
Lists all causal chains in the hypothesis graph

:author: Asan Agibetov

"""
import networkx as nx


def all_pairs_causal_chains(g):
    """Compute all causal chains in a hypothesis graph"""
    return nx.all_pairs_shortest_path(g)


def all_causal_chains(source_name, target_name, g):
    """Wrapper for shortest paths from source to target"""
    source = find_node(source_name, g)
    target = find_node(target_name, g)

    return nx.all_shortest_paths(g, source, target)


def find_node(node_name, g):
    """Go through the attributes and find the node with the given name"""
    for n, d in g.nodes_iter(data=True):
        if d["name"] == node_name:
            return n
