# coding: utf8
"""
Print all important statistical information on the hypothesis

:author: Asan Agibetov

"""
from hypotest.study_planning import find_missing_nodes
from hypotest.assign_weights import compute_importance_weights


def print_stats(H):
    """
    (hypothgraph) -> io stream

    Prints stats info about the hypothesis graph, i.e., importance factors for
    nodes, number of nodes, missing nodes, and what is missing for the
    hypothesis to hold

    """
    # assign weights
    H = compute_importance_weights(H)

    n_nodes = len(H.nodes())
    n_edges = len(H.edges())

    n_missing_nodes = len(list(find_missing_nodes(H)))

    # they will come out [(node, attr_dict), ...]
    sorted_importance = sort_importance_factor(H)

    print("# of nodes: {}, edges: {}".format(n_nodes, n_edges))
    print("# of missing nodes: {}".format(n_missing_nodes))

    print("\n==================")
    print("Importance weights")
    print("==================")
    for n, d in sorted_importance:
        print("{} importance: {}".format(d["name"],
                                         d["computed importance factor"]))


def sort_importance_factor(H):
    """
    (hypothtest) -> dict of sorted nodes by biggest importance factor

    """
    def key_func(G):
        """Sort on 'computed importance factor' field"""
        n, d = G
        return d["computed importance factor"]

    sorted_importance = sorted(H.nodes_iter(data=True),
                               key=key_func, reverse=True)

    return sorted_importance
