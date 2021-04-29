from typing import Callable, Sequence
from itertools import islice
from dataclasses import dataclass
from networkx import Graph
from network_destruction.graph import (
    make_erdos_renyi_graph, make_barabasi_albert_graph
)
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


def show_analyses(
        title_prefix: str,
        laplacian_disruption_analysis: Sequence[Analysis],
        normalized_laplacian_disruption_analysis: Sequence[Analysis],
        degree_centrality_disruption_analysis: Sequence[Analysis]
):
    show_analysis(
        f"{title_prefix}. Laplacian distance.",
        lambda a: a.laplacian_distance,
        Result("Disruption driven by Laplacian distance",
               laplacian_disruption_analysis),
        Result("Disruption driven by normalized Laplacian disatance",
               normalized_laplacian_disruption_analysis),
        Result("Disruption driven by degree centrality",
               degree_centrality_disruption_analysis)
    )

    show_analysis(
        f"{title_prefix}. Normalized laplacian distance.",
        lambda a: a.normalized_laplacian_distance,
        Result("Disruption driven by Laplacian distance",
               laplacian_disruption_analysis),
        Result("Disruption driven by normalized Laplacian disatance",
               normalized_laplacian_disruption_analysis),
        Result("Disruption driven by degree centrality",
               degree_centrality_disruption_analysis)
    )

    show_analysis(
        f"{title_prefix}. Giant order distance",
        lambda a: a.giant_order_distance,
        Result("Disruption driven by Laplacian distance",
               laplacian_disruption_analysis),
        Result("Disruption driven by normalized Laplacian disatance",
               normalized_laplacian_disruption_analysis),
        Result("Disruption driven by degree centrality",
               degree_centrality_disruption_analysis)
    )


def save_analysis(g: Graph, iterations: int, file_prefix: str):
    print("Computing laplacian distance disruption...", end=' ')
    d_l = tuple(islice(laplacian_distance_disruption(g), iterations))
    save_object(d_l, f"{file_prefix}_disruption_laplacian_.pickle")
    print("Done")

    print("Analyzing laplacian distance disruption...", end=' ')
    a_l = analyze_disruption(g, d_l)
    save_object(a_l, f"{file_prefix}_analysis_laplacian.pickle")
    print("Done")

    print("Computing normalized laplacian distance disruption...", end=' ')
    d_nl = tuple(islice(normalized_laplacian_distance_disruption(g), iterations))
    save_object(d_nl, f"{file_prefix}_disruption_normalized_laplacian_.pickle")
    print("Done")

    print("Analyzing normalized laplacian distance disruption...", end=' ')
    a_nl = analyze_disruption(g, d_nl)
    save_object(a_nl, f"{file_prefix}_analysis_normalized_laplacian.pickle")
    print("Done")

    print("Computing degree centrality disruption...", end=' ')
    d_dc = tuple(islice(degree_centrality_disruption(g), iterations))
    save_object(d_dc, f"{file_prefix}_disruption_degree_centrality.pickle")
    print("Done")

    print("Analyzing degree centrality disruption...", end=' ')
    a_dc = analyze_disruption(g, d_dc)
    save_object(a_dc, f"{file_prefix}_analysis_degree_centrality.pickle")
    print("Done")

    print()


def load_analysis(title_prefix: str, file_prefix: str):
    a_l = load_object(f"{file_prefix}_analysis_laplacian.pickle")
    a_nl = load_object(f"{file_prefix}_analysis_normalized_laplacian.pickle")
    a_dc = load_object(f"{file_prefix}_analysis_degree_centrality.pickle")

    show_analyses(title_prefix, a_l, a_nl, a_dc)


def save_erdos_renyi_analysis(probability: float, iterations: int):
    print(f"Generating Erdős-Rényi graph with p={probability}...", end=' ')
    g = make_erdos_renyi_graph(probability=probability)
    print("Done")

    save_analysis(g, iterations, f"erdos_renyi_{probability}_{iterations}")


def load_erdos_renyi_analysis(probability: float, iterations: int):
    load_analysis(f"Erdős-Rényi graph with p={probability}",
                  f"erdos_renyi_{probability}_{iterations}")


def save_barabasi_albert_analysis(edges: int, iterations: int):
    print(f"Generating Barabasi-Albert graph with m={edges}...", end=' ')
    g = make_barabasi_albert_graph(edges=edges)
    print("Done")

    save_analysis(g, iterations, f"barabasi_albert_{edges}_{iterations}")


def load_barabasi_albert_analysis(edges: float, iterations: int):
    load_analysis(f"Barabasi-Albert graph with m={edges}",
                  f"barabasi_albert_{edges}_{iterations}")


if __name__ == '__main__':
    save_erdos_renyi_analysis(0.25, 70)
    save_erdos_renyi_analysis(0.10, 70)
    save_erdos_renyi_analysis(0.02, 70)

    load_erdos_renyi_analysis(0.25, 70)
    load_erdos_renyi_analysis(0.10, 70)
    load_erdos_renyi_analysis(0.02, 70)

    # ---

    save_barabasi_albert_analysis(5, 70)
    save_barabasi_albert_analysis(10, 70)
    save_barabasi_albert_analysis(20, 70)

    load_barabasi_albert_analysis(5, 70)
    load_barabasi_albert_analysis(10, 70)
    load_barabasi_albert_analysis(20, 70)
