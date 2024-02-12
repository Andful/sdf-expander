from dataclasses import dataclass
from typing import Iterator, Hashable
from sympy import Matrix
from math import lcm, gcd

@dataclass
class Channel:
    source: int
    target: int
    source_production_rate: int
    target_consumption_rate: int
    initial_tokens: int

    def topological_matrix_column(self, n_actors: int) -> list[int]:
        result = [0] * n_actors
        result[self.source] = self.source_production_rate
        result[self.target] -= self.target_consumption_rate
        return result

@dataclass
class Sdf:
    actors: tuple[Hashable, ...]
    channels: tuple[Channel, ...]

    def __init__(self, actors = (), channels = ()) -> None:
        self.actors = actors
        self.channels = channels

    def add_actor(self, actor: Hashable):
        self.actors = self.actors + (actor,)

    def add_channel(self, source, source_production_rate, target, target_consumption_rate, initial_tokens=0):
        if source not in self.actors:
            raise ValueError(f'"{source}" is not an actor')
        if target not in self.actors:
            raise ValueError(f'"{target}" is not an actor')
        self.channels = self.channels + (Channel(self.actors.index(source), self.actors.index(target), source_production_rate, target_consumption_rate, initial_tokens),)
	
    def topology_matrix(self):
        return [c.topological_matrix_column(len(self.actors)) for c in self.channels]
        
    def repetitions_vector(self) -> tuple[int, ...]:
        topology_matrix = Matrix(self.topology_matrix())
        assert topology_matrix.rank() == len(self.actors) - 1
        [result] = topology_matrix.nullspace()

        m = lcm(*(e.denominator for e in result))
        result = m * result
        m = gcd(*result)
        result = result/m

        return tuple(result)
    
    def _repr_svg_(self):
        import graphviz

        dot = graphviz.Digraph()
        for (i, e) in enumerate(self.actors):
            dot.node(str(i), f"{e}")

        for c in self.channels:
            dot.edge(str(c.source), str(c.target), label=str(c.initial_tokens), taillabel=str(c.source_production_rate), headlabel=str(c.target_consumption_rate))

        return dot._repr_image_svg_xml()

    def to_hsdf(self):
        return Hsdf(self, self.repetitions_vector())

@dataclass
class Hsdf:
    sdf: Sdf
    repetitions_vector: tuple[int]

    def actors(self) -> Iterator[tuple[Hashable, int]]:
        for i, a in enumerate(self.sdf.actors):
            for j in range(self.repetitions_vector[i]):
                yield (a, j)

    def channels(self) -> Iterator[tuple[tuple[Hashable, int], tuple[Hashable, int], int]]:
        for c in self.sdf.channels:
            source = self.sdf.actors[c.source]
            target = self.sdf.actors[c.target]
            for i in range(self.repetitions_vector[c.source]):
                for k in range(c.source_production_rate):
                    j = (((c.initial_tokens + i*c.source_production_rate + k) % (c.target_consumption_rate*self.repetitions_vector[c.target])))//c.target_consumption_rate
                    d = (c.initial_tokens + i*c.source_production_rate + k)//(c.target_consumption_rate * self.repetitions_vector[c.target])
                    yield ((source, i), (target, j), d)

    def _repr_svg_(self):
        import graphviz

        dot = graphviz.Digraph()
        for (e, k) in self.actors():
            dot.node(f"{e}-{k}", f"{e}({k})")

        for (source, source_k), (target, target_k), tokens in self.channels():
            dot.edge(f"{source}-{source_k}", f"{target}-{target_k}", label=str(tokens))

        return dot._repr_image_svg_xml()

