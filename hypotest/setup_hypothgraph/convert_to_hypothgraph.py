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
# # Convert any digraph into a hypothgraph
#
# A hypothgraph needs to have additional parameters computed
#
# - `evidence_weight`
# - `importance_weight`
# - `boundary nodes` (`hypothesis_source` and `hypothesis_target`)
#
from hypotest.graph_mutation import importance_weights, evidence_weights


# Convert networkx graph into a hypograph with causality meta-data updated
def convert_to_hypothgraph(digraph):
    # assign global important weights (topology) to the graph
    digraph = importance_weights.assign_importance_weights(digraph)

    # assign evidence weights to the graph
    digraph = evidence_weights.assign_evidence_weights(digraph)

    return digraph
