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

Script to print latex tables for the generalization stats over different
configurations of the hypothesis

Essentially, we are producing different *delta* confidences, starting from an
initial configuration of the hypothesis, by slightly changing the source and the
target of the hypothesis. And we do so for all the unevidenced nodes.

"""
import pandas as pd

from hypotest import utils as hypotest_utils
from hypotest.print_stats import utils as stats_utils
from hypotest.assert_evidence import assert_evidence, unassert_evidence
from hypotest import assert_endpoints
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


def generalization_different_evidenced_nodes(H, endpoints, evidenced_list,
                                             evidenced_list_labels):
    """
    (hypothgraph, (source, target),
        [[evidenced1, ....], ...], [label_list1, ...) -> stats_obj

    Constructs hypothesis configuration, one for each from the
    evidenced_nodes_list, and compares the generalization scores for each of
    them

    """
    source, target = endpoints
    hypoth_confs = [H.copy() for _ in range(len(evidenced_list))]

    stats_evidenced = {}

    # evidence all the needed nodes
    for hypoth_conf, evidenced_nodes, label in zip(hypoth_confs,
                                                   evidenced_list,
                                                   evidenced_list_labels):
        assert_endpoints.assert_endpoints(hypoth_conf, source, target)
        for evidenced_node in evidenced_nodes:
            assert_evidence(hypoth_conf, evidenced_node)

        stats_evidenced[label] = \
            generalization.generalization_data_for_plot(hypoth_conf)

    return stats_evidenced


# CAN BE REFACTOR SO THAT IT REUSES PREVIOUS FUNCTION FOR DATAFRAME CONVERSION
#
def generalization_evidenced_df(H, endpoints, evidenced_list,
                                evidenced_list_labels):
    """
    Arranges statistics for differenct generalization under different hypothesis
    configurations in a Pandas dataframe

    """
    evidenced_obj = generalization_different_evidenced_nodes(
        H, endpoints, evidenced_list, evidenced_list_labels)

    # we need to duplicate node_id for all other values, we identify the length
    # of other arrays only ones
    series_size = None

    # final dataframe
    final_df = None

    for label, stats_obj in evidenced_obj.items():
        if series_size is None:
            series_size = len(stats_obj['confidences'])

        stats_obj['evidenced configuration'] = [label] * \
            series_size

        # first time creating the dataframe
        if final_df is None:
            final_df = pd.DataFrame(stats_obj)
        else:
            df = pd.DataFrame(stats_obj)
            final_df = pd.concat([final_df, df])
            final_df.reset_index()

    return final_df
