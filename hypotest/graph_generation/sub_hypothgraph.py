#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
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

    return sub_hypothgraph
