#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# same old trick to put this directory into the path
import os
import sys

import networkx as nx

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
mypath = os.path.join(dirname, '..')
mypath = os.path.abspath(mypath)
sys.path.insert(0, mypath)

# # Testing graph mutation functions

# Make hypoth graph creates a hypothesis graph from any directed graph, here we
# make sure that this graph contains the necessary structure.
from hypotest.setup_hypothgraph import sample_graphs
from hypotest.graph_mutation import boundary
from hypotest.confidence import compute_confidence

# ## Fixtures
import pytest

# Some sample graphs on which we test the confidence propagation


def test_compute_confidence():
    pass
