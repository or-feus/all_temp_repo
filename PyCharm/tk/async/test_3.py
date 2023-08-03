from typing import overload


@overload
def test(num):
    return num


@overload
def test(num, num2):
    return num + num2


print(test(1))
