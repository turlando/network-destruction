from typing import TypeVar, Callable
from network_destruction.graph import make_erdos_renyi_graph
from networkx import number_connected_components


T = TypeVar('T')
V = TypeVar('V')


def bisect(
        function: Callable[[V], T],
        compare: Callable[[T], bool],
        bisect_value: Callable[[V], V],
        value: V
) -> V:
    result = function(value)

    if compare(result):
        return value
    else:
        new_value = bisect_value(value)
        return bisect(function, compare, bisect_value, new_value)


def find_probability(components: int):
    return bisect(
        lambda probability: make_erdos_renyi_graph(probability=probability),
        lambda graph: number_connected_components(graph) >= components,
        lambda value: value - value / 100,
        0.25
    )
