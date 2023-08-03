import time

import tracemalloc


def result(iterator, iter):
    res = []
    for i, v in enumerate(iterator):
        if i < iter:
            res.append(v)
        else:
            break

    return res


# start = time.time()
# lazy_div = (i for i in arr if i % 2)
# lazy_mul = (i for i in lazy_div if i * 3)
# lazy_add_string = (f'{i}=kiki' for i in lazy_mul)
# z = result(lazy_add_string, 100)
# print(z)
# end = time.time()

def main():
    tracemalloc.start()

    start = time.time()

    arr = range(100000)

    '''----------------------------------------------
    strict_div: i % 2가 1인 것들만 솎아내기
    strict_mul: i에 3을 곱하고 저장
    strict_add_string: i 뒤에 문자열 추가
    res: strict_add_string에 저장된 배열을 100개만 가져오기
    ----------------------------------------------'''

    strict_div = (i for i in arr if i % 2)
    strict_mul = (i * 3 for i in strict_div)
    strict_add_string = (f'{i}=kiki' for i in strict_mul)
    res = result(strict_add_string, 100)
    print(res)
    end = time.time()

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)

    print(f'{end - start}ms')


if __name__ == '__main__':
    main()
