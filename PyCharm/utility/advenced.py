from typing import Callable, Iterable, List


def _curry(func):
    def _(a, *_):
        if len(_):
            return func(a, *_)
        else:
            return lambda *_: func(a, *_)


def L_reduce(func: Callable, acc, iterator: Iterable):
    if iterator is None:
        iterator = acc.__iter__()
        acc = iterator.__next__()

    for a in iterator:
        acc = func(acc, a)


def L_filter(iterator: Iterable, func: Callable) -> List:
    result = []
    for a in iterator:
        if func(a):
            result.append(a)

    return result


arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

res = L_filter(arr, lambda x: x > 3)

print(res)
