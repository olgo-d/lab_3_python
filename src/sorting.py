import random
from typing import Any, Callable, Optional, TypeVar, Protocol

class Comparable(Protocol):
    def __lt__(self, other: "Comparable", /) -> bool: ...
    def __gt__(self, other: "Comparable", /) -> bool: ...

T = TypeVar("T", bound=Comparable)


def _compare_func(
        key: Optional[Callable[[T], Any]],
        cmp: Optional[Callable[[T, T], int]],
) -> Callable[[T, T], int]:
    """
    создает функцию compare() для сравнения двух элементов
    :param key: параметр сравнения
    :param cmp: параметр сравнения (выше по приоритету чем key)
    :return: функция compare()
    """
    if cmp is not None:

        def compare(x: T, y: T) -> int:
            return cmp(x, y)

    elif key is not None:
        def compare(x: T, y: T) -> int:
            key_x = key(x)
            key_y = key(y)

            if key_x > key_y:
                return 1
            if key_x < key_y:
                return -1
            return 0

    else:
        def compare(x: T, y: T) -> int:
            if x > y:
                return 1
            if x < y:
                return -1
            return 0

    return compare



def bubble_sort(
    a: list[Any],
    key: Optional[Callable[[T], Any]],
    cmp: Optional[Callable[[T, T], int]],
) -> list[Any]:

    n = len(a)
    b = a.copy()
    compare = _compare_func(key, cmp)

    for i in range(n-1):
        for j in range(n-1):
            if compare(b[j], b[j+1]) > 0:
                b[j], b[j+1] = b[j+1], b[j]

    return b


def quick_sort(
    a: list[Any],
    key: Optional[Callable[[T], Any]],
    cmp: Optional[Callable[[T, T], int]],
) -> list[Any]:

    if len(a) <= 1:
        return a

    compare = _compare_func(key, cmp)

    piv = random.choice(a)
    less_piv = []
    more_piv = []
    equal_piv = []
    for el in a:
        if compare(el, piv) < 0:
            less_piv.append(el)
        elif compare(el, piv) > 0:
            more_piv.append(el)
        else:
            equal_piv.append(el)

    return quick_sort(less_piv, key=key, cmp=cmp) + equal_piv + quick_sort(more_piv, key=key, cmp=cmp)


def counting_sort(a: list[int]) -> list[int]:

    if not a:
        return []

    min_val = min(a)
    max_val = max(a)

    count = [0] * (max_val - min_val + 1)

    for el in a:
        count[el - min_val] += 1

    res = []
    for i, x in enumerate(count):
        val = i + min_val
        res.extend([val] * x)

    return res


def radix_sort(a: list[int]) -> list[int]:
    max_num = max(a)
    exp = 1

    while max_num // exp > 0:
        n = len(a)
        output = [0] * n
        count = [0] * 10

        for num in a:
            index = (num // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = (a[i] // exp) % 10
            output[count[index] - 1] = a[i]
            count[index] -= 1

        for i in range(n):
            a[i] = output[i]

        exp *= 10

    return a


def bucket_sort(
    a: list[float | int],
    buckets_kol: int | None = None
) -> list[float]:

    if buckets_kol is not None:
        n = buckets_kol
    else:
        n = len(a)

    buckets: list[list[int | float]] = [[] for _ in range(n)]

    for el in a:
        bi = int(el*10) % n
        buckets[bi].append(el)

    for bucket in buckets:
        quick_sort(bucket, key=None, cmp=None)

    index = 0
    for bucket in buckets:
        for el in bucket:
            a[index] = el
            index += 1

    return a


def heapify(arr, n, i, f_comp):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and f_comp(arr[left], arr[largest]) > 0:
        largest = left

    if right < n and f_comp(arr[right], arr[largest]) > 0:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, f_comp)

def heap_sort(
    a: list[Any],
    key: Optional[Callable[[T], Any]],
    cmp: Optional[Callable[[T, T], int]],
) -> list[Any]:

    n = len(a)
    compare = _compare_func(key, cmp)

    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i, compare)

    for i in range(n - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        heapify(a, i, 0, compare)

    return a
