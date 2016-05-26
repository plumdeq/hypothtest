# coding: utf8
"""
Scripts to prepare the experimental results

:author: Asan Agibetov

"""
import networkx as nx


from hypotest import assert_endpoints
from hypotest import assert_evidence
from hypotest import confidence_propagation as cp
from hypotest import utils


def latex_table(H, endpoints=None, evidenced_nodes=None):
    """
    (hypothgraph, (source, target)@opt, [evidenced_node]@opt) -> latex
        table@string

    Prints a latex table with importance measures for the nodes, for the given
    hypothesis configuration

    """
    H1 = H.copy()

    if endpoints:
        try:
            assert_endpoints.assert_endpoints(H1, *endpoints)
        except Exception as e:
            print(e)
            return e

    if evidenced_nodes:
        for evidenced_node in evidenced_nodes:
            assert_evidence.assert_evidence(H1, evidenced_node)

    source, target = utils.find_causal_endpoints(H1)

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
    header += r'\textbf{Global importance} $\phi$ & '
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
