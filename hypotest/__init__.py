# coding: utf8
"""
Main entry to the package, reference to the default mutable Hypothesis Graph

"""
from hypotest.make_hypothesis_graph import make_hypothesis_graph
from hypotest.assign_weights import compute_importance_weights

H = make_hypothesis_graph()
H = compute_importance_weights(H)
