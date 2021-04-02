from typing import List

from network_destruction.graph import make_graph
from network_destruction.plot import Plot, show_plot
from network_destruction.ranking import (
    Ranking,
    laplacian_disruption_ranking,
    normalized_laplacian_disruption_ranking,
    giant_order_disruption_ranking
)


def show_laplacian_distance_comparison(
        laplacian_rankings: List[Ranking],
        normalized_laplacian_rankings: List[Ranking],
        giant_order_rankings: List[Ranking],
        probability: float
):
    show_plot(
        f"Laplacian distance with p={probability}",
        Plot("Disruption driven by laplacian distance",
             range(len(laplacian_rankings)),
             [r.laplacian_distance for r in laplacian_rankings],
             [r.isolated_node for r in laplacian_rankings]),
        Plot("Disruption driven by normalized laplacian distance",
             range(len(normalized_laplacian_rankings)),
             [r.laplacian_distance for r in normalized_laplacian_rankings],
             [r.isolated_node for r in normalized_laplacian_rankings]),
        Plot("Disruption driven by giant order distance",
             range(len(giant_order_rankings)),
             [r.laplacian_distance for r in giant_order_rankings],
             [r.isolated_node for r in giant_order_rankings])
    )


def show_normalized_laplacian_distance_comparison(
        laplacian_rankings: List[Ranking],
        normalized_laplacian_rankings: List[Ranking],
        giant_order_rankings: List[Ranking],
        probability: float
):
    show_plot(
        f"Normalized laplacian distance with p={probability}",
        Plot("Disruption driven by laplacian distance",
             range(len(laplacian_rankings)),
             [r.normalized_laplacian_distance for r in laplacian_rankings],
             [r.isolated_node for r in laplacian_rankings]),
        Plot("Disruption driven by normalized laplacian distance",
             range(len(normalized_laplacian_rankings)),
             [r.normalized_laplacian_distance for r in normalized_laplacian_rankings],
             [r.isolated_node for r in normalized_laplacian_rankings]),
        Plot("Disruption driven by giant order distance",
             range(len(giant_order_rankings)),
             [r.normalized_laplacian_distance for r in giant_order_rankings],
             [r.isolated_node for r in giant_order_rankings])
    )


def show_giant_order_distance_comparison(
        laplacian_rankings: List[Ranking],
        normalized_laplacian_rankings: List[Ranking],
        giant_order_rankings: List[Ranking],
        probability: float
):
    show_plot(
        f"Giant order distance with p={probability}",
        Plot("Disruption driven by laplacian distance",
             range(len(laplacian_rankings)),
             [r.giant_order_distance for r in laplacian_rankings],
             [r.isolated_node for r in laplacian_rankings]),
        Plot("Disruption driven by normalized laplacian distance",
             range(len(normalized_laplacian_rankings)),
             [r.giant_order_distance for r in normalized_laplacian_rankings],
             [r.isolated_node for r in normalized_laplacian_rankings]),
        Plot("Disruption driven by giant order distance",
             range(len(giant_order_rankings)),
             [r.giant_order_distance for r in giant_order_rankings],
             [r.isolated_node for r in giant_order_rankings])
    )


def make_comparison(probability: float, iterations: float):
    print(f"Generating graph with probability={probability}...", end=' ')
    g = make_graph(probability=probability)
    print("Done")

    print("Computing laplacian disruption rankings...", end=' ')
    d_l = list(laplacian_disruption_ranking(g, iterations))
    print("Done")

    print("Computing normalized laplacian disruption rankings...", end=' ')
    d_nl = list(normalized_laplacian_disruption_ranking(g, iterations))
    print("Done")

    print("Computing giant order disruption rankings...", end=' ')
    d_go = list(giant_order_disruption_ranking(g, iterations))
    print("Done")

    print("Showing results...", end=' ')
    show_laplacian_distance_comparison(d_l, d_nl, d_go, probability)
    show_normalized_laplacian_distance_comparison(d_l, d_nl, d_go, probability)
    show_giant_order_distance_comparison(d_l, d_nl, d_go, probability)
    print("Done")

    print()


if __name__ == '__main__':
    make_comparison(0.25, 70)
    make_comparison(0.10, 70)
    make_comparison(0.02, 70)
