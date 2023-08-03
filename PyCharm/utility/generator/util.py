arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 10]


def generator_arr(arr):
    for a in arr:
        yield a


def gen_filter(iter):
    for a in iter:
        if a % 2:
            yield a


def gen_take(iter):
    result = []

    for a in iter:
        result.append(a)
        if len(result) == 2:
            return result

    return result


gen = generator_arr(arr)
zz = gen_filter(gen)

print(gen_take(zz))