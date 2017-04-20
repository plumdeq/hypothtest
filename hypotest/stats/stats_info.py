# coding: utf8
"""
author: Asan Agibetov

   Copyright 2015-2017 Asan Agibetov <asan.agibetov@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Print all important statistical information on the hypothesis

"""
from hypotest.study_planning import find_missing_nodes
from hypotest.assign_weights import compute_importance_weights
from hypotest.confidence_propagation import most_informative_missing_node


def print_stats(H, source, target):
    """
    (hypothgraph, source, target) -> io stream

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
    most_informatives = most_informative_missing_node(H, source, target)

    print("\n====================")
    print("Nodes informativeness")
    print("====================")
    for name, informativeness in most_informatives:
        print("{} informativenss: {}".format(name, informativeness))


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
