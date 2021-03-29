from typing import List
from dataclasses import dataclass, field
from math import sqrt
from networkx import Graph, number_connected_components
from network_destruction.distance import (laplacian_distance,
                                          normalized_laplacian_distance)
from network_destruction.graph import remove_node_edges, giant_order


@dataclass
class GraphRanking:
    graph: Graph = field(repr=False)
    isolated_node: int
    laplacian_distance: float
    normalized_laplacian_distance: float
    components: int
    giant_order: int


def distance_ranking(graph: Graph) -> List[GraphRanking]:
    def make_ranking(node):
        mutilated_graph = remove_node_edges(graph, node)
        return GraphRanking(mutilated_graph,
                            node,
                            laplacian_distance(graph, mutilated_graph),
                            normalized_laplacian_distance(graph, mutilated_graph),
                            number_connected_components(mutilated_graph),
                            giant_order(mutilated_graph))

    nodes = list(graph.nodes())
    rankings = [make_ranking(node) for node in nodes]

    return sorted(rankings,
                  key=lambda ranking: ranking.normalized_laplacian_distance,
                  reverse=True)


def disruption_ranking(graph: Graph, iterations: int = 20):
    for _ in range(iterations):
        distances = distance_ranking(graph)
        best = distances[0]

        graph = best.graph
        yield best
