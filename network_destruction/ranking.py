from typing import List, Callable

from dataclasses import dataclass, field
from math import sqrt

from networkx import Graph, number_connected_components
from network_destruction.distance import (laplacian_distance,
                                          normalized_laplacian_distance)

from network_destruction.graph import remove_node_edges, giant_order


@dataclass
class Ranking:
    graph: Graph = field(repr=False)
    isolated_node: int
    laplacian_distance: float
    normalized_laplacian_distance: float
    components: int
    giant_order: int


def distance_ranking(
        metric: Callable[[Ranking], float]
) -> Callable[[Graph], List[Ranking]]:

    def make_ranking(graph: Graph, node: int) -> Ranking:
        mutilated_graph = remove_node_edges(graph, node)
        return Ranking(
            mutilated_graph,
            node,
            laplacian_distance(graph, mutilated_graph),
            normalized_laplacian_distance(graph, mutilated_graph),
            number_connected_components(mutilated_graph),
            giant_order(mutilated_graph)
        )

    def ranking(graph: Graph) -> List[Ranking]:
        nodes = list(graph.nodes())
        rankings = [make_ranking(graph, node) for node in nodes]

        return sorted(rankings, key=metric, reverse=True)

    return ranking


laplacian_distance_ranking = distance_ranking(
    lambda ranking: ranking.laplacian_distance
)

normalized_laplacian_distance_ranking = distance_ranking(
    lambda ranking: ranking.normalized_laplacian_distance
)


def disruption_ranking(distance_ranking: Callable[[Graph], List[Ranking]]):
    def ranking(graph: Graph, iterations: int = 20):
        for _ in range(iterations):
            distances = distance_ranking(graph)
            best = distances[0]

            graph = best.graph
            yield best

    return ranking


laplacian_disruption_ranking = disruption_ranking(laplacian_distance_ranking)

normalized_laplacian_disruption_ranking = disruption_ranking(
    normalized_laplacian_distance_ranking
)
