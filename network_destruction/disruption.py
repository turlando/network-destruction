from typing import Callable, Iterator, Tuple
from dataclasses import dataclass
from networkx import Graph
from network_destruction.graph import Node, isolate_node
from network_destruction.distance import (
    SpectralDistance, laplacian_distance, normalized_laplacian_distance
)


DisruptionMetric = Callable[[Graph], Node]


@dataclass
class Disruption:
    graph: Graph
    isolated_node: Node


@dataclass
class Score:
    node: Node
    score: float


def disrupt(graph: Graph, metric: DisruptionMetric) -> Iterator[Disruption]:
    current_graph = graph

    for _ in range(graph.number_of_nodes()):
        node_to_isolate = metric(current_graph)
        current_graph = isolate_node(current_graph, node_to_isolate)

        yield Disruption(current_graph, node_to_isolate)


def spectral_distance_disruption(
        graph: Graph,
        spectral_distance: SpectralDistance
):
    def metric(graph: Graph) -> Node:
        nodes = list(graph.nodes())
        ranking = (score(graph, node) for node in nodes)
        best = max(ranking, key=lambda r: r.score)
        return best.node

    def score(graph: Graph, node: Node) -> Score:
        mutilated_graph = isolate_node(graph, node)
        distance = spectral_distance(graph, mutilated_graph)
        return Score(node, distance)

    return disrupt(graph, metric)


def laplacian_distance_disruption(graph: Graph):
    return spectral_distance_disruption(graph, laplacian_distance)


def normalized_laplacian_distance_disruption(graph: Graph):
    return spectral_distance_disruption(graph, normalized_laplacian_distance)
