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

Script to prepare the experimental results for global and local importance
measures

"""
import networkx as nx

from hypotest import confidence_propagation as cp
from hypotest import hypotest_utils
from hypotest.print_stats import utils as stats_utils


def latex_table(H, endpoints=None, evidenced_nodes=None):
    """
    (hypothgraph, (source, target)@opt, [evidenced_node]@opt) -> latex
        table@string

    Prints a latex table with importance measures for the nodes, for the given
    hypothesis configuration

    """
    H1 = stats_utils.preapre_hypothesis_graph(H, endpoints, evidenced_nodes)
    source, target = hypotest_utils.find_causal_endpoints(H1)

    delta_importance = dict(cp.most_informative_missing_node(H1, source,
                                                             target))
    nx.set_node_attributes(H1, 'delta importance', delta_importance)

    table = '\\\\\n'.join(node_info(node_id, node_dict)
                          for node_id, node_dict in H1.nodes_iter(data=True))

    return header() + '\n' + table


def latex_table_template():
    """
    Return latex table template, can be changed for different latex table
    definitions

    """
    return ""


def header():
    """
    Custom header for the latex table

    """
    header = r'\textbf{Factor ID} & \textbf{Factor label} & '
    header += r'\textbf{Global importance} $\psi$ & '
    header += r'\textbf{Delta importance} $\Delta_{C_h_i}$'

    return header


def node_info(node_id, node_dict):
    """
    ([(node_id, { 'label': 'diminuition...'))...] -> string with stats

    Takes a list of tuples (node_id, node_dict)

    Wraper which returns importance measures for a given node

    """
    return '%s & %s & %.3f & %.3f' % (node_id, node_dict['label'],
                                      node_dict['computed importance factor'],
                                      node_dict['delta importance'])
