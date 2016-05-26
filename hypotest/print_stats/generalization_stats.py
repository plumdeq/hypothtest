# coding: utf8
"""
Script to print latex tables for the generalization stats over different
configurations of the hypothesis

Essentially, we are producing different *delta* confidences, starting from an
initial configuration of the hypothesis, by slightly changing the source and the
target of the hypothesis. And we do so for all the unevidenced nodes.

:author: Asan Agibetov

"""
import pandas as pd

from hypotest import utils as hypotest_utils
from hypotest.print_stats import utils as stats_utils
from hypotest.assert_evidence import assert_evidence, unassert_evidence
from hypotest.inference import generalization


def generalization_stats(H, endpoints=None, evidenced_nodes=None):
    """
    (hypothgraph, (source, target)@opt, [evidenced_node]@opt) ->
        generalization obj

    Simulate the generalization of the hypothesis and collect all data in a
    generalization object

    The generalization object is

    {
        'hyperthropy': {
            'confidence': [0.2, ...],
            'dist_delta': [-1, ...]
        },
        'cell viability': {
            ...
        }
    }


    """
    # assert new endpoints and evidenced nodes in the copy of the graph and
    # return reference to it
    H = stats_utils.preapre_hypothesis_graph(H, endpoints, evidenced_nodes)

    source, target = hypotest_utils.find_causal_endpoints(H)
    unevidenced_nodes = hypotest_utils.find_missing_nodes(H)

    generalizations = {}
    # we evidence one node at a time and see how well does it generalize
    for unevidenced_node in unevidenced_nodes:
        generalizations[unevidenced_node] = generalize_wrapper(
            H, unevidenced_node, f=generalization.generalization_data_for_plot)

    return generalizations


def generalize_wrapper(H, unevidenced_node, f=generalization.generalize,
                       *args, **kwargs):
    """
    () -> evidences ``unevidenced_node``; f() ; unevidence back the node

    ``f`` is the generalization function

    """
    assert_evidence(H, unevidenced_node)
    result = f(H, *args, **kwargs)
    unassert_evidence(H, unevidenced_node)

    return result


def convert_to_dataframe(H, endpoints=None, evidenced_nodes=None):
    """
    (hypothgraph, (source, target)@opt, [evidenced_node]@opt) ->
        generalization obj

    Data preparation for a dataframe, such that we have

        index confidence dist_delta conf_delta node_id
        0      0.2       -1        0.5        'hyperthropy'
        1      0.2       -2        0.5        'hyperthropy'
        ...
        2      0.2       -1        0.5        'cell viability'
        3      0.2       -3        0.5        'cell viability'

    The stats object is

    {
        'hyperthropy': {
            'confidences': [0.2, ...],
            'dist_deltas': [-1, ...]
        },
        'cell viability': {
            ...
        }
    }

    """
    generalization_obj = generalization_stats(H, endpoints, evidenced_nodes)
    # we need to duplicate node_id for all other values, we identify the length
    # of other arrays only ones
    series_size = None

    # final dataframe
    final_df = None

    for node_id, stats_obj in generalization_obj.items():
        if series_size is None:
            series_size = len(stats_obj['confidences'])

        stats_obj['unevidenced_node'] = [H.node[node_id]['label']] * \
            series_size

        # first time creating the dataframe
        if final_df is None:
            final_df = pd.DataFrame(stats_obj)
        else:
            df = pd.DataFrame(stats_obj)
            final_df = pd.concat([final_df, df])
            final_df.reset_index()

    return final_df
