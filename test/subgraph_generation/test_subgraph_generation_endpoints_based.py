#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# same old trick to put this directory into the path
import os
import sys

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
mypath = os.path.join(dirname, '..')
mypath = os.path.abspath(mypath)
sys.path.insert(0, mypath)

# # Testing graph generation functions

# Graph generation functions are used to generate graphs given certain
# constraints. Here we generate subgraphs from the paths passing through the
# endpoints, and we do so by monotonically increasing the ratio of
# #edges(subgraph)/#edges(graph)
import networkx as nx

from hypotest.graph_generation import sub_hypothgraph, hypoth_conf, boundary
from hypotest.setup_hypothgraph import sample_graphs

import math
# ## Fixtures
import pytest


@pytest.fixture
def get_sample_hypothgraph():
    return sample_graphs.sample_hypothgraph()


# Test subgraph generation
#
# Generated subgraph from sorted paths passing through the endpoints, has the
# same topology (boundary-interior, on-boundary nodes) and its number of edges
# grows monotonically


def test_subhypothgraph_based_endpoints(get_sample_hypothgraph):
    hypothgraph = get_sample_hypothgraph
