from itertools import chain

import pytest

from batch import batches


@pytest.fixture
def dependency_as_generator():
    yield "fixture value"

@pytest.mark.parametrize(
    "batch_size, expected", [
        [1, [[1], [2], [3], [4], [5], [6]]],
        [2, [[1, 2], [3, 4], [5, 6]]],
        [3, [[1, 2, 3], [4, 5, 6]]],
        [4, [[1, 2, 3, 4], [5, 6]]],
    ]
)
def test_batch_with_loop(batch_size, expected):
    iterable = [1, 2, 3, 4, 5, 6]

    assert list(batches(iterable, batch_size)) == expected


def test_batch_on_lists():
    assert list(batches([1, 2, 3, 4, 5, 6], 1)) == [[1], [2], [3], [4], [5], [6]]
    assert list(batches([1, 2, 3, 4, 5, 6], 2)) == [[1, 2], [3, 4], [5, 6]]
    assert list(batches([1, 2, 3, 4, 5, 6], 3)) == [[1, 2, 3], [4, 5, 6]]
    assert list(batches([1, 2, 3, 4, 5, 6], 4)) == [[1, 2, 3, 4], [5, 6]]


def test_batch_order():
    iterable = range(100)
    batch_size = 2

    output = batches(iterable, batch_size)

    assert list(chain.from_iterable(output)) == list(iterable)


def test_batch_sizes():
    iterable = range(100)
    batch_size = 2

    output = list(batches(iterable, batch_size))

    for batch in output[:-1]:
        assert len(batch) == batch_size
    assert len(output[-1]) <= batch_size
