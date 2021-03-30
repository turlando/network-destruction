from typing import Callable
from math import sqrt

from numpy import ndarray
from networkx import Graph, laplacian_spectrum, normalized_laplacian_spectrum

from network_destruction.graph import giant_order


def spectrum_distance(
        spectrum: Callable[[Graph], ndarray]
) -> Callable[[Graph, Graph], float]:
    """
    Return a function that computes the distance between two graphs
    using a given spectrum function.
    """
    def distance(graph_0: Graph, graph_1: Graph) -> float:
        spectrum_0 = spectrum(graph_0)
        spectrum_1 = spectrum(graph_1)

        differences = spectrum_0 - spectrum_1
        powers = differences ** 2

        return sqrt(sum(powers))

    return distance


laplacian_distance = spectrum_distance(laplacian_spectrum)
normalized_laplacian_distance = spectrum_distance(normalized_laplacian_spectrum)


def giant_order_distance(graph_0: Graph, graph_1: Graph):
    giant_order_0 = giant_order(graph_0)
    giant_order_1 = giant_order(graph_1)

    return abs((giant_order_1 - giant_order_0) / giant_order_0)
