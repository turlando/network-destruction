import matplotlib as plt
from networkx import Graph, erdos_renyi_graph, connected_components, draw


def make_graph(
        nodes: int = 100,
        probability: float = 0.25,
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


def giant_order(graph: Graph) -> Graph:
    "Return the number of nodes in the largest subgraph."
    nodes = max(connected_components(graph), key=len)
    return len(nodes)
