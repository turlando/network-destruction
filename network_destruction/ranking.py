from typing import List
from math import sqrt
from dataclasses import dataclass
from networkx import (Graph, erdos_renyi_graph,
                      laplacian_spectrum, number_connected_components)


RANDOM_SEED = 1616492035
GRAPH_NODES = 100
GRAPH_EDGE_PROBABILITY = 0.25


@dataclass
class GraphRanking:
    removed_node: int
    distance: float
    components: int


def make_graph() -> Graph:
    return erdos_renyi_graph(GRAPH_NODES, GRAPH_EDGE_PROBABILITY, RANDOM_SEED)


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


def distance_ranking(graph: Graph) -> List[GraphRanking]:
    def make_ranking(node):
        mutilated_graph = remove_node_edges(graph, node)
        return GraphRanking(node,
                            distance(graph, mutilated_graph),
                            number_connected_components(mutilated_graph))

    nodes = list(graph.nodes())
    rankings = [make_ranking(node) for node in nodes]

    return sorted(rankings,
                  key=lambda ranking: ranking.distance,
                  reverse=True)
