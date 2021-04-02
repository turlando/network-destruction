from typing import Iterable, Any
from dataclasses import dataclass

import matplotlib.pyplot as plt


DEFAULT_FMT = 'o-'


# Invariant: len(xs) == len(ys) == len(names)
@dataclass
class Plot:
    label: str
    xs: Iterable[float]
    ys: Iterable[float]
    names: Iterable[Any]


def show_plot(title: str, *plots: Plot):
    figure, axes = plt.subplots()
    axes.set_title(title)

    for plot in plots:
        axes.plot(plot.xs, plot.ys, DEFAULT_FMT, label=plot.label)

        for x, y, name in zip(plot.xs, plot.ys, plot.names):
            axes.annotate(xy=(x, y), text=name)

    axes.legend()
    figure.show()
