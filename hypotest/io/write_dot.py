#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# # Write to dot format
#
# Write hypothesis graphs in dot format. Grontocrawler already can write one
# simple hypothesis graph in dot format, so here we write the subgraph and the
# big graph to dot. To disambiguate edges and nodes coming from two graphs, we
# apply a different style to  edges and nodes of one of the graphs (e.g.,
# different color, style of the edge).

import sys

# ## Styles
#
# Nodes of the big graph will have no shape (just label)
big_node_style = '"%s" [label="%s",shape="none"] ;\n'
# Edges of the big graph will be dashed
big_edge_style = '"%s" -> "%s" [label="%s",style="dashed"] ;\n'

# Nodes of the small graph are ellipse form and edges are bold and solid
small_node_style = '"%s" [label="%s",shape="ellipse"] ;\n'
small_edge_style = '"%s" -> "%s" [label="%s",style="bold"] ;\n'

# Causal endpoints are filled nodes
endpoint_node_style = '"%s" [label="%s",shape="ellipse",style="filled",color="red"] ;\n'


# Creat `dot` from digraph representation of the subgraph. We need both the big
# and the small graphs. We assume that `big, small` are `NetworkX` graphs
#
def to_dot(big, small, source, target, stream=sys.stdout):
    """
    (graph, graph, steram) -> string > stream

    Args:
        - big, small (networkx.DiGraph): Hypothesis graph and its subgraph
        - stream (default: sys.stdout | file): Where to write the output
        - source, target (nodes): Causal endpoints
    Returns:
        - (string -> stream): `dot` representation of the graph

    """
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
