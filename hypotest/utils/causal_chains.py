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

Lists all causal chains in the hypothesis graph

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
        if d["label"] == node_name:
            return n
