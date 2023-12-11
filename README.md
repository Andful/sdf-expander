# SDF Expander

Synchronous Dataflow Graph (SDF) is a model of computation. An SDF is represented as a directed graph where tokens are produced and consumed between the nodes through its arches, with a fixed production and consumption rate of tokens.

A very useful routine applied to SDFs is the conversion of an arbitrary SDF to an equivalent singlerate SDF, where a singlerate SDF is an SDF with production/consumption rates equal to 1.

The sole purpose of this library is to implements this conversion routine.

An example of this conversion is present at [Example.ipynb](./examples/Example.ipynb)