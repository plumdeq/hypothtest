#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import networkx as nx

from hypotest.setup_hypothgraph import convert_to_hypothgraph
from hypotest.graph_generation import paths
#
# # Generation of subhypothgraphs
#
# To generate a subhypothgraph, we need to make sure that it corresponds to
# several properties. The necessary property is the endpoints of the boundary,
# the percentage of the paths in the boundary interior and the percentage of
# the paths on the boundary.
#
# ## Note
#
# Please note that to generate subgraphs, we first take nodes from the paths
#
# This function will try to generate a subgraph from the hypothegraph, which
# will contain the required number of paths in the boundary interior and on the
# boundary. On the boundary paths are generated as paths from the `source`
def generate_sub_hypothgraph(hypothgraph, source, target,
                            ratio_endpoints_paths=0.5,
                            ratio_on_boundary_paths=0.5,
                            data=False):
    sub_hypothgraph = nx.DiGraph()
    sub_hypothgraph = convert_to_hypothgraph.convert_to_hypothgraph(sub_hypothgraph)

    # adding endpoints paths
    endpoints_paths = paths.take_ratio_endpoints_paths_rand(
            hypothgraph, source, target, ratio=ratio_endpoints_paths)

    for endpoints_path in endpoints_paths:
        sub_hypothgraph.add_path(endpoints_path)

    # adding on boundary paths
    on_boundary_paths = paths.take_ratio_boundary_paths_rand(
            hypothgraph, source, target, ratio=ratio_on_boundary_paths)

    for on_boundary_path in on_boundary_paths:
        sub_hypothgraph.add_path(on_boundary_path)

    # add data if required
    sub_hypothgraph = copy_data_to_subgraph(hypothgraph, sub_hypothgraph)

    return sub_hypothgraph


# Go through nodes and edges and coput data attributes, assumes that nodes and
# edges exist in the big graph
def copy_data_to_subgraph(big, small):
    for small_node in small.nodes_iter():
        if small_node in big.nodes_iter():
            small.node[small_node] = big.node[small_node]
        else:
            print('{} is not in the big graph'.format(small_node))

    # g.edge is one signle dictionary of type { 'source': { 'target': edge_dict
    # } }
    for small_edge in small.edges_iter():
        u, v = small_edge

        if u in big.edge:
            if v in big.edge[u]:
                small.edge[u][v] = big.edge[u][v]
        else:
            print('{} is not in the big graph'.format(small_edge))

    return small
