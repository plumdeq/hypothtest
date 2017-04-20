#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# # Write to dot format
#
# Write hypothesis graphs in dot format. Grontocrawler already can write one
# simple hypothesis graph in dot format, so here we write the subgraph and the
# big graph to dot. To disambiguate edges and nodes coming from two graphs, we
# apply a different style to  edges and nodes of one of the graphs (e.g.,
# different color, style of the edge).

import sys


from hypotest.graph_generation import boundary


# ## Styles
#
# Nodes of the big graph will have no shape (just label)
big_node_style = '"%s" [label="%s",shape="ellipse",style="dotted",fontsize=13.0,fontname="Tahoma"] ;\n'
# Edges of the big graph will be dashed
big_edge_style = '"%s" -> "%s" [label="%s",style="dotted",fontsize=12.0,fontname="Tahoma"] ;\n'

# Nodes of the small graph are ellipse form and edges are bold and solid
small_node_style = '"%s" [label="%s",shape="ellipse",fontsize=14.0,fontname="Arial"] ;\n'
small_edge_style = '"%s" -> "%s" [label="%s",style="bold",fontsize=13.0,fontname="Arial"] ;\n'

# If we have only one graph to draw then nodes are ellipses, i.e., `small_node_style`
node_style = small_node_style

# If we have only one graph to draw then edges are full, i.e., `small_edge_style`
edge_style = small_edge_style

# Causal endpoints are filled nodes
endpoint_node_style = '"%s" [label="%s",shape="ellipse",style="filled",color="red"] ;\n'

# Nodes in the boundary interior are filled blue
boundary_interior_node_style = '"%s" [label="%s",shape="ellipse",style="filled", color="blue"] ;\n'

# Evidenced nodes are filled green
evidenced_node_style = '"%s" [label="%s",shape="ellipse",style="filled",color="green"] ;\n'

# When we draw visible graph with invisible nodes and edges, visible nodes are
# the same as `big_node_style`
visible_node_style    =  small_node_style
visible_edge_style    =  small_edge_style
invisible_node_style  =  '"%s" [label="%s",style="invisible"] ;\n'
invisible_edge_style  =  '"%s" -> "%s" [label="%s",shape="none",arrowhead="dot",arrowsize=0.1,style="invisible"] ;\n'


# Creat `dot` from digraph representation of the subgraph and full graph.
# We assume that `big, small` are `NetworkX` graphs
#
def big_small_to_dot(big, small, conf, stream=sys.stdout):
    """
    (graph, graph, steram) -> string > stream

    Args:
        - big, small (networkx.DiGraph): Hypothesis graph and its subgraph
        - stream (default: sys.stdout | file): Where to write the output
        - conf (hypo_conf.Hypoth_Conf): Hypothesis configuration

            - source, target (nodes): Causal endpoints
            - evidenced_nodes ([node...]): Evidenced nodes

    Returns:
        - (string -> stream): `dot` representation of the graph

    """
    source, target, evidenced_nodes = conf

    stream.write('digraph g {\n')

    # Go through the nodes of the big graph, if the node is in the small graph
    # then apply `small_node_style`, otherwise use `big_node_style`. Special
    # attention to the endpoints
    for (node, node_data) in big.nodes_iter(data=True):
        node_str = big_node_style

        if node in small.nodes_iter():
            node_str = small_node_style

        if node == source or node == target:
            node_str = endpoint_node_style

        stream.write(node_str % (node, node_data['label']))

    # Go through the edges of the big graph, if the edge is in the small graph
    # then apply `small_edge_style`, otherwise use `big_edge_style`
    for (source, target, edge_data) in big.edges_iter(data=True):
        edge_str = big_edge_style

        if (source, target) in small.edges_iter():
            edge_str = small_edge_style

        stream.write(edge_str % (source, target, edge_data['label']))

    stream.write('}\n')

    return None


# Write to dot one hypothesis graph by applying different styles to the
# endpoints, evidenced nodes and the boundary nodes. You should also highlight
# the paths from endpoints
def hypothgraph_to_dot(hypothgraph, conf, stream=sys.stdout, show_boundary_interior=False, show_evidenced=False):
    """
    (graph, hypoth_conf, stream) -> string > stream

    Args:
        - hypothgraph (networkx.DiGraph): Hypothesis graph
        - conf (hypo_conf.Hypoth_Conf): Hypothesis configuration

            - source, target (nodes): Causal endpoints
            - evidenced_nodes ([node...]): Evidenced nodes

        - stream (default: sys.stdout | file): Where to write the output
        - show_boundary_interior (default: False): Should we apply different style to boundary interior nodes?
        -show_evidenced (default: False): Should we apply different style to evidenced nodes?
    Returns:
        - (string -> stream): `dot` representation of the graph

    """
    # extract configuration of the confidence evaluation of a hypothesis
    source, target, evidenced_nodes = conf

    boundary_interior_nodes = list(
            boundary.in_boundary_interior(hypothgraph, source, target))

    stream.write('digraph g {\n')

    # Go through the nodes of the hypothesis graph and apply the right node
    # styles
    for (node, node_data) in hypothgraph.nodes_iter(data=True):
        node_str = node_style

        # precedence is `boundary_interior_node` < `endpoint_node` < `evidenced_node`
        if show_boundary_interior and node in boundary_interior_nodes:
            node_str = boundary_interior_node_style

        if node == source or node == target:
            node_str = endpoint_node_style

        if show_evidenced and node in evidenced_nodes:
            node_str = evidenced_node_style

        stream.write(node_str % (node, node_data['label']))

    # Go through the edges of the big graph, if the edge is in the small graph
    # then apply `small_edge_style`, otherwise use `big_edge_style`
    for (s, t, edge_data) in hypothgraph.edges_iter(data=True):
        edge_str = edge_style

        stream.write(edge_str % (s, t, edge_data['label']))

    stream.write('}\n')

    return None


# Draw a subgraph G'=< N', E' > relative to the big graph G = < N, E >, such
# that the n' \in N' are visible nodes and n \in N - N' are not visible. Nodes
# in the big graph but not in the subgraph are invisible, the same for the
# edges
def hypothgraph_with_invisible_to_dot(big, small, conf, stream=sys.stdout):
    """
    (graph, graph, steram) -> string > stream

    Args:
        - small, big (networkx.DiGraph): Subgraph and its super hypothgraph
        - stream (default: sys.stdout | file): Where to write the output
        - conf (hypo_conf.Hypoth_Conf): Hypothesis configuration

            - source, target (nodes): Causal endpoints
            - evidenced_nodes ([node...]): Evidenced nodes

    Returns:
        - (string -> stream): `dot` representation of the graph

    """
    source, target, evidenced_nodes = conf

    stream.write('digraph g {\n')

    # Go through the nodes of the big graph, if the node is in the small graph
    # then apply `small_node_style`, otherwise use `big_node_style`. Special
    # attention to the endpoints
    for (node, node_data) in big.nodes_iter(data=True):
        node_str = invisible_node_style

        if node in small.nodes_iter():
            node_str = visible_node_style

        if node == source or node == target:
            node_str = endpoint_node_style

        stream.write(node_str % (node, node_data['label']))

    # Go through the edges of the big graph, if the edge is in the small graph
    # then apply `small_edge_style`, otherwise use `big_edge_style`
    for (source, target, edge_data) in big.edges_iter(data=True):
        edge_str = invisible_edge_style
        edge_label = ""

        # write label if visible
        if (source, target) in small.edges_iter():
            edge_str = visible_edge_style
            edge_label = edge_data['label']

        stream.write(edge_str % (source, target, edge_label))

    stream.write('}\n')

    return None
