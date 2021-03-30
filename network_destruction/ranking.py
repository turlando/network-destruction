from typing import List, Callable

from dataclasses import dataclass, field

from networkx import Graph, number_connected_components
from network_destruction.distance import (laplacian_distance,
                                          normalized_laplacian_distance,
                                          giant_order_distance)

from network_destruction.graph import remove_node_edges, giant_order


@dataclass
class Ranking:
    graph: Graph = field(repr=False)
    isolated_node: int
    components: int
    giant_order: int

    laplacian_distance: float
    normalized_laplacian_distance: float
    giant_order_distance: float


def distance_ranking(
        metric: Callable[[Ranking], float]
) -> Callable[[Graph, Graph], List[Ranking]]:

    def make_ranking(
            original_graph: Graph,
            previous_graph,
            node: int
    ) -> Ranking:

        mutilated_graph = remove_node_edges(previous_graph, node)
        return Ranking(
            mutilated_graph,
            node,
            number_connected_components(mutilated_graph),
            giant_order(mutilated_graph),

            laplacian_distance(previous_graph, mutilated_graph),
            normalized_laplacian_distance(previous_graph, mutilated_graph),
            giant_order_distance(original_graph, mutilated_graph),
        )

    def ranking(
            original_graph: Graph,
            previous_graph: Graph
    ) -> List[Ranking]:

        nodes = list(previous_graph.nodes())
        rankings = [make_ranking(original_graph, previous_graph, node)
                    for node in nodes]

        return sorted(rankings, key=metric, reverse=True)

    return ranking


laplacian_distance_ranking = distance_ranking(
    lambda ranking: ranking.laplacian_distance
)

normalized_laplacian_distance_ranking = distance_ranking(
    lambda ranking: ranking.normalized_laplacian_distance
)

giant_order_distance_ranking = distance_ranking(
    lambda ranking: ranking.giant_order_distance
)


def disruption_ranking(
        distance_ranking: Callable[[Graph, Graph], List[Ranking]]
):

    def ranking(graph: Graph, iterations: int = 20):
        previous_graph = graph

        for _ in range(iterations):
            distances = distance_ranking(graph, previous_graph)
            best = distances[0]

            previous_graph = best.graph
            yield best

    return ranking


laplacian_disruption_ranking = disruption_ranking(
    laplacian_distance_ranking
)

normalized_laplacian_disruption_ranking = disruption_ranking(
    normalized_laplacian_distance_ranking
)

giant_order_disruption_ranking = disruption_ranking(
    giant_order_distance_ranking
)
