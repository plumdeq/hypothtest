#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# put on path `hypotest` package
#
import os
import sys


hypotest_folder = os.path.dirname(os.path.abspath(__file__))
hypotest_folder = os.path.join(hypotest_folder, '..')
sys.path.insert(0, hypotest_folder)

import argparse

from hypotest.setup_hypothgraph import sample_graphs
from hypotest.graph_generation import sub_hypothgraph, hypoth_conf
from hypotest.io import write_dot

# Prepare a sample big and small graphs
def sample_big_and_small(ratio_endpoints_paths=0.5, ratio_on_boundary_paths=0.5):
    big = sample_graphs.sample_hypothgraph()
    source, target = hypoth_conf.generate_rich_endpoints(big)

    small = sub_hypothgraph.generate_sub_hypothgraph(
            big, source, target,
            ratio_endpoints_paths=ratio_endpoints_paths,
            ratio_on_boundary_paths=ratio_on_boundary_paths)

    return big, small, source, target

# CL tool to convert OWL ontologies into `dot` graph format
#
def main():
    parser = argparse.ArgumentParser()

    def_output = os.path.join(hypotest_folder, './shared/dot/digraph.dot')
    def_ratio_endpoints = 0.5
    def_ratio_boundary = 0.5

    parser.add_argument('--ratio-endpoints', default=def_ratio_endpoints)
    parser.add_argument('--ratio-boundary', default=def_ratio_boundary)
    parser.add_argument('-o', '--output-dot', default=def_output)

    args = parser.parse_args()

    # get a sample hypothgraph
    big, small, source, target = sample_big_and_small(
                    ratio_endpoints_paths=float(args.ratio_endpoints),
                    ratio_on_boundary_paths=float(args.ratio_boundary))

    with open(args.output_dot, 'w') as f:
        write_dot.to_dot(big, small, source, target, stream=f)


if __name__ == '__main__':
    main()
