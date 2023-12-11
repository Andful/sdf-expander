# SDF Expander

Synchronous Dataflow Graph (SDF) is a model of computation. An SDF is represented as a directed graph where tokens are produced and consumed between the nodes through the arches, with a fixed production and consumption rate of tokens.

A very useful routine in SDF is the conversion of an arbitrary SDF to an equivalent singlerate SDF, where singlerate SDF is an SDF with production/consumption rates equal to 1.

This library just implements the routine for converting an arbitrary SDF to a singlerate SDF.