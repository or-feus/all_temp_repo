from typing import Any, Iterable, List


def batches(iterable: Iterable[Any], batch_size: int) -> Iterable[List[Any]]:

    results = []
    batch = []

    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch



def batches_hey():
    return "A"