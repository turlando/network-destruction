from typing import Sequence
from dataclasses import dataclass
from networkx import Graph, number_connected_components
from network_destruction.utils import pairwise
from network_destruction.graph import giant_order
from network_destruction.disruption import Disruption
from network_destruction.distance import (
    Distance, laplacian_distance, normalized_laplacian_distance,
    giant_order_distance
)


@dataclass
class Analysis:
    disruption: Disruption
    components: int
    giant_order: int
    laplacian_distance: Distance
    normalized_laplacian_distance: Distance
    giant_order_distance: Distance


def analyze_disruption(
        graph: Graph,
        disruption: Sequence[Disruption]
) -> Sequence[Analysis]:

    first_iteration = disruption[0]

    first_result = Analysis(
        first_iteration,
        number_connected_components(first_iteration.graph),
        giant_order(first_iteration.graph),
        laplacian_distance(graph, first_iteration.graph),
        normalized_laplacian_distance(graph, first_iteration.graph),
        giant_order_distance(graph, first_iteration.graph)
    )

    rest_results = [
        Analysis(
            d1,
            number_connected_components(d1.graph),
            giant_order(d1.graph),
            laplacian_distance(d0.graph, d1.graph),
            normalized_laplacian_distance(d0.graph, d1.graph),
            giant_order_distance(graph, d1.graph)
        )
        for d0, d1 in pairwise(disruption)
    ]

    return [first_result, *rest_results]
