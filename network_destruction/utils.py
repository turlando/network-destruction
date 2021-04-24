from typing import TypeVar, Sequence, Iterator, Tuple
from pickle import dump, load


T = TypeVar('T')


def pairwise(xs: Sequence[T]) -> Iterator[Tuple[T, T]]:
    # [0, 1, 2, 3] -> [[0, 1], [1, 2], [2, 3]]
    return zip(xs, xs[1:])


def save_object(obj, path):
    with open(path, 'wb') as f:
        dump(obj, f)


def load_object(path):
    with open(path, 'rb') as f:
        return load(f)
