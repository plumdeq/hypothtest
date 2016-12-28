#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# # Utils functions for setting up the hypothgraph



# Converting to a hypothesis graph means adding `evidenced` attribute as well
# as the hypothesis boundaries
def fill_missing_values(digraph):
    for node, data in digraph.nodes_iter(data=True):
        if not 'evidenced' in data:
            digraph.node[node]['evidenced'] = 0
        if not 'causal_endpoint' in data:
            digraph.node[node]['causal_endpoint'] = 0

    return digraph


