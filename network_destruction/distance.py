from typing import Callable
from math import sqrt
from numpy import ndarray
from networkx import Graph, laplacian_spectrum, normalized_laplacian_spectrum
from network_destruction.graph import giant_order


Distance = float
GraphSpectrum = Callable[[Graph], ndarray]
SpectralDistance = Callable[[Graph, Graph], float]


def spectral_distance(
        graph_0: Graph,
        graph_1: Graph,
        spectrum: Callable[[Graph], ndarray]
) -> Distance:
    spectrum_0 = spectrum(graph_0)
    spectrum_1 = spectrum(graph_1)

    differences = spectrum_0 - spectrum_1
    powers = differences ** 2

    return sqrt(sum(powers))


def laplacian_distance(graph_0: Graph, graph_1: Graph):
    return spectral_distance(graph_0, graph_1, laplacian_spectrum)


def normalized_laplacian_distance(graph_0: Graph, graph_1: Graph):
    return spectral_distance(graph_0, graph_1, normalized_laplacian_spectrum)


def giant_order_distance(graph_0: Graph, graph_1: Graph):
    giant_order_0 = giant_order(graph_0)
    giant_order_1 = giant_order(graph_1)

    return abs((giant_order_1 - giant_order_0) / giant_order_0)
