# Hypothesis testing

Prototype implementation of confidence propagation and study planning

So we start off with an ontology which models a certain hypothesis of causality
relationships among the factors.  This library, takes on input a DIGRAPH
(networkx format) as output of the ontology to graph transformation from
Grontocrawler.  In this piece of code we update the graph with computed
parameters, such as importance metrics. Then, the augmented graph with mete
data is sent to the backend. The backend code of `hypotest` then, serves the
augmented graph with computed parameters to the frontend. And the frontend is
responsible for the visualization of the network, and for the treatment of the
user input that are transformed into the `http` queries.
