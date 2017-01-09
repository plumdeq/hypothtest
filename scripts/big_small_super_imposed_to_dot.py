#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Asan Agibetov
#
# This script draws a diagram for a big hypothesis graph and its
# sub hypothesis graph superimposed. In addition, this script draws one diagram
# for supergraph and one diagram for the subgraph
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
    source, target = hypoth_conf.generate_rich_endpoints(big, min_nb_paths=5)

    small = sub_hypothgraph.generate_sub_hypothgraph(
            big, source, target,
            ratio_endpoints_paths=ratio_endpoints_paths,
            ratio_on_boundary_paths=ratio_on_boundary_paths,
            data=True)

    return big, small, source, target


# CL tool to convert OWL ontologies into `dot` graph format
#
def main():
    parser = argparse.ArgumentParser()

    def_output_superimposed = os.path.join(hypotest_folder, './shared/dot/super_imposed.dot')
    def_output_small = os.path.join(hypotest_folder, './shared/dot/small.dot')
    def_output_big = os.path.join(hypotest_folder, './shared/dot/big.dot')
    def_ratio_endpoints = 0.3
    def_ratio_boundary = 0.01

    parser.add_argument('--ratio-endpoints', default=def_ratio_endpoints)
    parser.add_argument('--ratio-boundary', default=def_ratio_boundary)
    parser.add_argument('--output-superimposed', default=def_output_superimposed)
    parser.add_argument('--output-small', default=def_output_small)
    parser.add_argument('--output-big', default=def_output_big)

    args = parser.parse_args()

    # get a sample hypothgraph
    big, small, source, target = sample_big_and_small(
                    ratio_endpoints_paths=float(args.ratio_endpoints),
                    ratio_on_boundary_paths=float(args.ratio_boundary))

    conf = hypoth_conf.Hypoth_Conf(source, target, [])

    # write the subgraph
    with open(args.output_small, 'w') as f:
        write_dot.hypothgraph_with_invisible_to_dot(big, small, conf, stream=f)

    # write the big graph
    with open(args.output_big, 'w') as f:
        write_dot.hypothgraph_to_dot(big, conf, stream=f)

    # write the super imposed graph
    with open(args.output_superimposed, 'w') as f:
        write_dot.big_small_to_dot(big, small, conf, stream=f)


if __name__ == '__main__':
    main()
