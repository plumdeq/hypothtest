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

Find missing nodes in the causal chain

Basically iterate via all nodes attributes, and find those factors which have
not been evidenced

"""
import networkx as nx
from hypotest.confidence_propagation import most_informative_missing_node


def compute_delta(H, source, target):
    """
    (hypograph, source, target) -> hypograph with delta attributes

    For given source and target nodes, set attribute for delta importance

    """
    delta = dict(most_informative_missing_node(H, source, target))
    nx.set_node_attributes(H, 'delta', delta)

    return H
