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

Common functions for all stats printing scripts
"""
from hypotest import assert_endpoints
from hypotest import assert_evidence


def preapre_hypothesis_graph(H, endpoints=None, evidenced_nodes=None):
    """
    Makes a copy of the hypothesis graph, and asserts endpoints (if any), as
    well as the evidenced nodes

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

    return H1
