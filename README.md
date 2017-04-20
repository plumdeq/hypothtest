# Hypothesis testing

Evidence-based hypothesis testing in the biomedical research is a crucial part
for the validation of any study. In our [prototype (link)][hypothtest] for
evidence-based hypothesis testing, we focus on causal hypotheses among the
factors (e.g., biological processes) which participate in a pathogenesis of a
musculoskeletal disease.  The prototype has been used for the validation from
the domain experts of the methodology presented in the paper. In particular, it
allows the experts to extract the causality information from the biomedical
ontologies and represent causal hypotheses as directed graphs, where nodes are
participating factors and arcs are directed causality relationships.
Furthermore, it allows to asses the confidence in a causal hypothesis, which
depends on the provided evidence for the factors and on the amount of causality
information.

## Prototype

So we start off with an ontology which models a certain hypothesis of causality
relationships among the factors. This library, takes on input a DIGRAPH
(networkx format) as output of the ontology to graph transformation from
[Grontocrawler (dependency of this prototype)][grontocrawler].  In this piece
of code we update the graph with computed parameters, such as importance
metrics. Then, the augmented graph with meta data is sent to the backend. The
backend code of `hypotest` then, serves the augmented graph with computed
parameters to the frontend. And the frontend is responsible for the
visualization of the network, and for the treatment of the user input that are
transformed into the `http` queries.

* [prototype (link)][hypothtest]

## Related publications

* Agibetov, Asan, E. Jiménez-Ruiz, A. Solimando, G. Guerrini, G. Patanè, and M. Spagnuolo. 2015. “Towards Shared Hypothesis Testing in the Biomedical Domain.” In *Proceedings of SWAT4LS International Conference 2015*, 1546:33–37. Cambridge, UK: CEUR-WS.org. <http://ceur-ws.org/Vol-1546/paper_16.pdf>.
* Agibetov, Asan, E. Jiménez-Ruiz, M. Ondresik, A. Solimando, G. Guerrini, C-E. Catalano, J-M. Oliveira, Giuseppe Patanè, R-L. Reis and Michela Spagnuolo. June 2016. “Supporting Shared Hypothesis Testing in the Biomedical Domain.” Submitted to Journal of Biomedical Semantics.

## Reproducibility of experiments

Experiments presented in the `Agibetov, Asan, E. Jiménez-Ruiz, M. Ondresik, A.
Solimando, G. Guerrini, C-E. Catalano, J-M. Oliveira, Giuseppe Patanè, R-L.
Reis and Michela Spagnuolo. June 2016. “Supporting Shared Hypothesis Testing in
the Biomedical Domain.” Submitted to Journal of Biomedical Semantics.` are
reproducible with [Jupyter Notebooks][jupyter] located in the `notebooks` folder.

## Online presentations

* [Intertnational conference on Semantic Web Application and Tools for Life Sciences (SWAT4LS) 2015 presentation][swat4ls2015]
* [Invited seminar on Knowledge-driven and Evidence-based Hypothesis Testing in the Biomedical Domain at the University of Oslo][oslo_seminar2017]

## Applicability to other contexts

* The framework's input is general:
    * OWL 2 ontologies (graph transformation is a lifted version of Grontocrawler, see seminar slides)
* Confidence assessment uses standard Graph Theory algorithms (based on
  weighted path computation)
* Can be applied to any complex domain where the *causal information* is
  important (see last slide of the Oslo seminar)

[hypothtest]: http://hypothtest.plumdeq.xyz/test/
[swat4ls2015]: http://asan.agibetov.me/talks/swat4ls2015
[oslo_seminar2017]: http://asan.agibetov.me/talks/oslo2017
[grontocrawler]: https://github.com/plumdeq/grontocrawler
[jupyter]: http://jupyter.org


## CHANGELOG

* v1.2.0 : Adds sample hypothesis, converted from Grontocrawler
* v1.3.0 : Major relase of hypothtest-conf-prop. Confidence computation (normalized to the maximum possible), relative confidence computation.  Sub hypothesis graph generation and dot graph file generation.
* v1.3.1 : adds functionality for a more interesting subgraph generation and the script to generate three diagrams for a subgraph, full graph and a super imposed graph
* v1.3.2 : Normalization rules for the hypothesis graph
* v1.3.3 : Public release to GitHub

## LICENSE

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
