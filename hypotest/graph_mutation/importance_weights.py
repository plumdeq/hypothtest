# coding: utf8
# # Graph mutation
#
# Use various SNA metrics to automatically compute weights
#
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
"""
#
import networkx as nx


# By default we use betweenees centrality measure
def default_global_importance_measure(hypothgraph):
    """
    (hypograph) > dict(node=importance)

    Default global importance measure

    """
    return nx.betweenness_centrality(hypothgraph, endpoints=True)


def assign_importance_weights(hypothgraph, measure=default_global_importance_measure):
    """
    (hypothgraph, [fun: measure]) -> hypothgraph

    Compute importance weights except for those set manually

    """
    computed_weights = default_global_importance_measure(hypothgraph)

    nx.set_node_attributes(hypothgraph, 'importance_weight', computed_weights)

    return hypothgraph
