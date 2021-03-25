from typing import List
from dataclasses import dataclass
from math import sqrt

from networkx import (Graph,
                      erdos_renyi_graph, laplacian_spectrum,
                      number_connected_components, connected_components,
                      draw)
import matplotlib.pyplot as plt


@dataclass
class GraphRanking:
    graph: Graph
    isolated_node: int
    distance: float
    components: int
    giant_order: int


def make_graph(
        nodes: int = 100,
        probability: int = 0.25,
        seed: int = 1616492035
) -> Graph:
    return erdos_renyi_graph(nodes, probability, seed)


def show_graph(graph: Graph) -> None:
    figure, axes = plt.subplots()
    draw(graph, ax=axes)
    figure.show()


def remove_node_edges(graph: Graph, node: int) -> Graph:
    g = graph.copy()

    node_edges = list(g.edges(node))
    g.remove_edges_from(node_edges)

    return g


def distance(graph_0: Graph, graph_1: Graph) -> float:
    spectrum_0 = laplacian_spectrum(graph_0)
    spectrum_1 = laplacian_spectrum(graph_1)

    differences = spectrum_0 - spectrum_1
    powers = differences ** 2

    return sqrt(sum(powers))


def giant_order(graph: Graph) -> Graph:
    "Return the number of nodes in the largest subgraph."
    nodes = max(connected_components(graph), key=len)
    return len(nodes)


def distance_ranking(graph: Graph) -> List[GraphRanking]:
    def make_ranking(node):
        mutilated_graph = remove_node_edges(graph, node)
        return GraphRanking(mutilated_graph,
                            node,
                            distance(graph, mutilated_graph),
                            number_connected_components(mutilated_graph),
                            giant_order(mutilated_graph))

    nodes = list(graph.nodes())
    rankings = [make_ranking(node) for node in nodes]

    return sorted(rankings,
                  key=lambda ranking: ranking.distance,
                  reverse=True)


def disruption_ranking(graph: Graph, iterations: int = 20):
    for _ in range(iterations):
        distances = distance_ranking(graph)
        best = distances[0]

        graph = best.graph
        yield best
