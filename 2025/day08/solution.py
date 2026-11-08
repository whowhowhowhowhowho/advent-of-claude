from dataclasses import dataclass
from functools import total_ordering
import itertools
import networkx as nx


def parse(text: str):
    return [JunctionBox(*map(int, line.split(','))) for line in text.splitlines()]


@dataclass(frozen=True)
@total_ordering
class JunctionBox:
    x: int
    y: int
    z: int

    def dist(self, other) -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    def vec_len(self) -> int:
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def __lt__(self, other):
        return self.vec_len() < other.vec_len()

    def __repr__(self):
        return f'{self.x:3d} {self.y:3d} {self.z:3d}'


def build_graph(boxes):
    g = nx.Graph()
    g.add_nodes_from(boxes)

    edges = sorted(list(itertools.combinations(boxes, 2)),
                   key=lambda e: e[0].dist(e[1]))

    return g, edges


def part1(text: str) -> int:
    boxes = parse(text)
    # the example (20 boxes) makes 10 connections, the real input (1000 boxes) 1000
    n_connections = 10 if len(boxes) < 100 else 1000

    g, edges = build_graph(boxes)

    while g.number_of_edges() < n_connections:
        g.add_edge(*edges[0])
        del edges[0]

    result = 1
    for i in sorted(map(len, nx.connected_components(g)), reverse=True)[:3]:
        result *= i

    return result


def part2(text: str) -> int:
    boxes = parse(text)

    g, edges = build_graph(boxes)
    last_edge = (0, 0)

    while not nx.is_connected(g):
        last_edge = edges[0]
        g.add_edge(*last_edge)
        del edges[0]

    return last_edge[0].x * last_edge[1].x
