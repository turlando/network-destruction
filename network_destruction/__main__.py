from typing import Callable, Sequence, Tuple
from itertools import islice
from dataclasses import dataclass
from network_destruction.graph import make_graph
from network_destruction.plot import Plot, show_plot
from network_destruction.disruption import (
    laplacian_distance_disruption, normalized_laplacian_distance_disruption,
    degree_centrality_disruption
)
from network_destruction.analysis import Analysis, analyze_disruption
from network_destruction.utils import save_object, load_object


@dataclass
class Result:
    name: str
    results: Sequence[Analysis]


def show_analysis(
        title: str,
        feature: Callable[[Analysis], float],
        *analyses: Result
):
    show_plot(
        title,
        *[Plot(analysis.name,
               range(len(analysis.results)),
               [feature(a) for a in analysis.results],
               [a.disruption.isolated_node for a in analysis.results])
          for analysis in analyses]
    )


def show_analyses(probability, a_l, a_nl, a_dc):
    show_analysis(
        f"Laplacian distance. p={probability}",
        lambda a: a.laplacian_distance,
        Result("Disruption driven by Laplacian distance", a_l),
        Result("Disruption driven by normalized Laplacian disatance", a_nl),
        Result("Disruption driven by degree centrality", a_dc)
    )

    show_analysis(
        f"Normalized laplacian distance. p={probability}",
        lambda a: a.normalized_laplacian_distance,
        Result("Disruption driven by Laplacian distance", a_l),
        Result("Disruption driven by normalized Laplacian disatance", a_nl),
        Result("Disruption driven by degree centrality", a_dc)
    )

    show_analysis(
        f"Giant order distance. p={probability}",
        lambda a: a.giant_order_distance,
        Result("Disruption driven by Laplacian distance", a_l),
        Result("Disruption driven by normalized Laplacian disatance", a_nl),
        Result("Disruption driven by degree centrality", a_dc)
    )


def load_analyses(probability: float):
    a_l = load_object(f"a_l_{probability}.pickle")
    a_nl = load_object(f"a_nl_{probability}.pickle")
    a_dc = load_object(f"a_dc_{probability}.pickle")

    show_analyses(probability, a_l, a_nl, a_dc)


def make_analysis(probability: float, iterations: int):
    print(f"Generating graph with probability={probability}...", end=' ')
    g = make_graph(probability=probability)
    print("Done")

    print("Computing laplacian distance disruption...", end=' ')
    d_l = tuple(islice(laplacian_distance_disruption(g), iterations))
    save_object(d_l, f"d_l_{probability}.pickle")
    print("Done")

    print("Analyzing laplacian distance disruption...", end=' ')
    a_l = analyze_disruption(g, d_l)
    save_object(a_l, f"a_l_{probability}.pickle")
    print("Done")

    print("Computing normalized laplacian distance disruption...", end=' ')
    d_nl = tuple(islice(normalized_laplacian_distance_disruption(g), iterations))
    save_object(d_nl, f"d_nl_{probability}.pickle")
    print("Done")

    print("Analyzing normalized laplacian distance disruption...", end=' ')
    a_nl = analyze_disruption(g, d_nl)
    save_object(a_nl, f"a_nl_{probability}.pickle")
    print("Done")

    print("Computing degree centrality disruption...", end=' ')
    d_dc = tuple(islice(degree_centrality_disruption(g), iterations))
    save_object(d_dc, f"d_dc_{probability}.pickle")
    print("Done")

    print("Analyzing degree centrality disruption...", end=' ')
    a_dc = analyze_disruption(g, d_dc)
    save_object(a_dc, f"a_dc_{probability}.pickle")
    print("Done")

    print("Showing results...", end=' ')
    show_analyses(probability, a_l, a_nl, a_dc)
    print("Done")

    print()


if __name__ == '__main__':
    make_analysis(0.25, 70)
    make_analysis(0.10, 70)
    make_analysis(0.02, 70)
