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
#
# # Node contribution
#
# Node contribution depends on the hypothesis configuration, and is computed as
# a difference in overall confidence whenever this node is evidenced or not.
# That is, say node `x` is not evidenced, and it is inside the hypothesis
# configuration path, then its contribution is computed as
# `conf(x_unevidenced) - conf(x_evidenced)`

def difference_importance(H, source, target, candidate_evidenced_node,
                          fn_importance=default_fn_importance, log=False):
    """
    (graph, path) -> float

    Compute difference in confidence value with or without candidate evidenced
    node

    """
    confidence_without = paths_confidence(H, source, target,
                                          fn_importance=fn_importance)

    assert_evidence(H, candidate_evidenced_node)
    confidence_with = paths_confidence(H, source, target,
                                       fn_importance=fn_importance)
    unassert_evidence(H, candidate_evidenced_node)

    gain_in_confidence = abs(confidence_with - confidence_without)

    if log:
        print("missing nodes {}".format(list(find_missing_nodes(H))))
        print("candidate evidenced node {}".format(candidate_evidenced_node))
        print("with confidence - {}, without - {}".format(confidence_with,
                                                          confidence_without))
        print("gain in confidence: {}".format(gain_in_confidence))

    return gain_in_confidence


def most_informative_missing_node(H, source=None, target=None,
                                  fn_importance=default_fn_importance):
    """
    (hypothgraph, source, target) -> [(node_id, delta_metric), ...]

    Simulate finding an evidence for one missing node, and assess the difference
    importance

    """
    if not source or not target:
        source, target = find_causal_endpoints(H)

    missing_nodes = find_missing_nodes(H)
    most_informative = {}

    for missing_node in missing_nodes:
        # evidence him and compute overall confidence
        most_informative[missing_node] = \
            difference_importance(H, source, target, missing_node)

    sorted_most_informative = sorted(most_informative.items(),
                                     key=itemgetter(1),
                                     reverse=True)

    return sorted_most_informative
