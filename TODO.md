# TODO

We collect all the items (e.g., features, bug fixes) that need to be done here

## Sample hypothesis ontologies

* [x] define manually a good subgraph (molecular)
* [x] in the universal hypothesis graph check `cartilage degeneration` it has duplicate definitions

## Semantic rules for hypothesis graph normalization

* [x] application of simplest graph patterns `occ_1 -- neg regulation -> occ_2 => occ_1 -- results in -> negative regulation of occ_2`
* [x] in the previous example, you also have to change `occ_2 - results -> occ_3`
* [ ] conversion of axioms of type *occurrent* `reduces levels of` some *molecule*
* [ ] double relations of type *occurrent* `negatively o positively = negatively` *occurrent*

## Graph generation

* [x] check that hypothgraph has annotations (e.g., 'evidenced': yes | no, 'btwin_centrality': [0, 1])
* [x] more graph mutation refactoring (assignment of boundary nodes, of evidences etc.)
* [x] add boundary functions, as, nodes within boundary (all accessible via simple paths) and outside
* [x] generate a sub hypothesis graph for given source and target (update generation function with the percentage of nodes in the boundary interior)
* [x] write subgraph to a dot language (based on grontocrawler)
* [x] check uniqueness of paths when you generate graphs
* [x] better endpoints generation, the pair of nodes should be chosen as the one that maximizes 'all_pairs_simple_paths'
* [x] `write to dot` should produce separate diagrams for: subgraph alone, full graph alone, superimposed subgraph and full graph
* [ ] partition the hypothesis graph based on the node sets for each of the partitions

## Confidence function

* [x] test relative confidence sub hypothesis to full hypothesis on a simple graph
* [x] test and refactor confidence propagation code for path graphs (simplest cases)
* [x] test confidence with more complex graphs
* [x] test relative confidence sub to full on a sample hypothesis graph
* [x] test and add notes on monotonicity of relative confidence (can we have the same for the normalized confidence?)
* [ ] test closest confidence to the max confidence given some constraints
* [o] compute confidence measure function as a mean value for the increasing number of evidenced nodes

## Results for the paper

* [ ] Relative confidence for subgraph on molecular level and the full graph
* [ ] Custom weighting scheme
* [ ] Local importance
* [ ] Inference procedures
