# TODO

We collect all the items (e.g., features, bug fixes) that need to be done here

## Items

* [x] check that hypothgraph has annotations (e.g., 'evidenced': yes | no, 'btwin_centrality': [0, 1])
* [x] more graph mutation refactoring (assignment of boundary nodes, of evidences etc.)
* [x] test and refactor confidence propagation code for path graphs (simplest cases)
* [x] add boundary functions, as, nodes within boundary (all accessible via simple paths) and outside
* [x] test confidence with more complex graphs
* [x] test relative confidence sub hypothesis to full hypothesis on a simple graph
* [x] generate a sub hypothesis graph for given source and target (update generation function with the percentage of nodes in the boundary interior)
* [x] test relative confidence sub to full on a sample hypothesis graph
* [x] write subgraph to a dot language (based on grontocrawler)
* [x] check uniqueness of paths when you generate graphs
* [x] test and add notes on monotonicity of relative confidence (can we have the same for the normalized confidence?)
* [o] `write to dot` should produce separate diagrams for: subgraph alone, full graph alone, superimposed subgraph and full graph
* [o] better endpoints generation, the pair of nodes should be chosen as the one that maximizes 'all_pairs_simple_paths'
* [ ] subgraph generation should take into account the ratio of nodes in the boundary interior
* [ ] partition the hypothesis graph based on the node sets for each of the partitions
* [ ] test closest confidence to the max confidence given some constraints
