import matplotlib.pyplot as plt

from typing import List

from network_destruction.graph import make_graph
from network_destruction.ranking import (
    Ranking,
    laplacian_disruption_ranking,
    normalized_laplacian_disruption_ranking,
    giant_order_disruption_ranking
)


def show_ranking_metrics_comparison(
        laplacian_rankings: List[Ranking],
        normalized_laplacian_rankings: List[Ranking],
        giant_order_rankings: List[Ranking],
        probability: float
):
    xs = range(len(laplacian_rankings))

    ##########################################################################

    laplacian_figure, laplacian_axes = plt.subplots()
    laplacian_axes.set_title(f"Laplacian distance with p={probability}")

    laplacian_axes.plot(
        xs,
        [r.laplacian_distance for r in laplacian_rankings],
        "o-",
        label="Disruption driven by laplacian distance"
    )

    for x, ranking in zip(xs, laplacian_rankings):
        laplacian_axes.annotate(xy=(x, ranking.laplacian_distance),
                                text=ranking.isolated_node)

    laplacian_axes.plot(
        xs,
        [r.laplacian_distance for r in normalized_laplacian_rankings],
        "o-",
        label="Disruption driven by normalized laplacian distance"
    )

    for x, ranking in zip(xs, normalized_laplacian_rankings):
        laplacian_axes.annotate(xy=(x, ranking.laplacian_distance),
                                text=ranking.isolated_node)

    laplacian_axes.plot(
        xs,
        [r.laplacian_distance for r in giant_order_rankings],
        "o-",
        label="Disruption driven by giant order distance"
    )

    for x, ranking in zip(xs, giant_order_rankings):
        laplacian_axes.annotate(xy=(x, ranking.laplacian_distance),
                                text=ranking.isolated_node)

    laplacian_axes.set_xticks(xs)
    laplacian_axes.legend()

    ##########################################################################

    normalized_laplacian_figure, normalized_laplacian_axes = plt.subplots()
    normalized_laplacian_axes.set_title("Normalized laplacian distance "
                                        f"with p={probability}")

    normalized_laplacian_axes.plot(
        xs,
        [r.normalized_laplacian_distance for r in laplacian_rankings],
        "o-",
        label="Disruption driven by laplacian distance"
    )

    for x, ranking in zip(xs, laplacian_rankings):
        normalized_laplacian_axes.annotate(
            xy=(x, ranking.normalized_laplacian_distance),
            text=ranking.isolated_node
        )

    normalized_laplacian_axes.plot(
        xs,
        [r.normalized_laplacian_distance for r in normalized_laplacian_rankings],
        "o-",
        label="Disruption driven by normalized laplacian distance"
    )

    for x, ranking in zip(xs, normalized_laplacian_rankings):
        normalized_laplacian_axes.annotate(
            xy=(x, ranking.normalized_laplacian_distance),
            text=ranking.isolated_node
        )

    normalized_laplacian_axes.plot(
        xs,
        [r.normalized_laplacian_distance for r in giant_order_rankings],
        "o-",
        label="Disruption driven by giant order distance"
    )

    for x, ranking in zip(xs, giant_order_rankings):
        normalized_laplacian_axes.annotate(
            xy=(x, ranking.normalized_laplacian_distance),
            text=ranking.isolated_node
        )

    normalized_laplacian_axes.set_xticks(xs)
    normalized_laplacian_axes.legend()

    ##########################################################################

    giant_order_figure, giant_order_axes = plt.subplots()
    giant_order_axes.set_title(f"Giant order distance with p={probability}")

    giant_order_axes.plot(
        xs,
        [r.giant_order_distance for r in laplacian_rankings],
        "o-",
        label="Disruption driven by laplacian distance"
    )

    for x, ranking in zip(xs, laplacian_rankings):
        giant_order_axes.annotate(
            xy=(x, ranking.giant_order_distance),
            text=ranking.isolated_node
        )

    giant_order_axes.plot(
        xs,
        [r.giant_order_distance for r in normalized_laplacian_rankings],
        "o-",
        label="Disruption driven by normalized laplacian distance"
    )

    for x, ranking in zip(xs, normalized_laplacian_rankings):
        giant_order_axes.annotate(
            xy=(x, ranking.giant_order_distance),
            text=ranking.isolated_node
        )

    giant_order_axes.plot(
        xs,
        [r.giant_order_distance for r in giant_order_rankings],
        "o-",
        label="Disruption driven by giant order distance"
    )

    for x, ranking in zip(xs, giant_order_rankings):
        giant_order_axes.annotate(
            xy=(x, ranking.giant_order_distance),
            text=ranking.isolated_node
        )

    giant_order_axes.set_xticks(xs)
    giant_order_axes.legend()

    ##########################################################################

    laplacian_figure.show()
    normalized_laplacian_figure.show()
    giant_order_figure.show()


def make_comparison(probability: float):
    print(f"Generating graph with probability={probability}")
    g = make_graph(probability=probability)

    print("Computing disruption rankings")
    d_l = list(laplacian_disruption_ranking(g))
    d_nl = list(normalized_laplacian_disruption_ranking(g))
    d_go = list(giant_order_disruption_ranking(g))

    show_ranking_metrics_comparison(d_l, d_nl, d_go, probability)

    print("Done")
    print()
