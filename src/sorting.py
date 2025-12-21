from typing import Any, Callable, Optional, TypeVar, Protocol

class Comparable(Protocol):
    def __lt__(self, other: "Comparable", /) -> bool: ...
    def __gt__(self, other: "Comparable", /) -> bool: ...

T = TypeVar("T", bound=Comparable)


class SortFunc():

    @staticmethod
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

    @staticmethod
    def bubble_sort(
            a: list[T],
            key: Optional[Callable[[T], Any]] = None,
            cmp: Optional[Callable[[T, T], int]] = None,
    ) -> list[T]:
        b = a.copy()
        n = len(b)
        if n < 2:
            return b

        compare = SortFunc._compare_func(key, cmp)

        end = n - 1
        while end > 0:
            swapped_flag = False
            last_swap = 0

            for j in range(end):
                if compare(b[j], b[j + 1]) > 0:
                    b[j], b[j + 1] = b[j + 1], b[j]
                    swapped_flag = True
                    last_swap = j

            if not swapped_flag:
                break

            end = last_swap

        return b

    @staticmethod
    def _median_of_three(lst: list[Any], compare: Callable[[T, T], int]) -> Any:
        if len(lst) < 3:
            return lst[len(lst) // 2]

        x = lst[0]
        y = lst[len(lst) // 2]
        z = lst[-1]

        if compare(x, y) > 0:
            x, y = y, x
        if compare(y, z) > 0:
            y, z = z, y
        if compare(x, y) > 0:
            x, y = y, x

        return y

    @staticmethod
    def quick_sort(
            a: list[Any],
            key: Optional[Callable[[T], Any]] = None,
            cmp: Optional[Callable[[T, T], int]] = None,
    ) -> list[Any]:

        if len(a) <= 1:
            return a

        compare = SortFunc._compare_func(key, cmp)

        piv = SortFunc._median_of_three(a, compare)

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

        left = SortFunc.quick_sort(less_piv, key=key, cmp=cmp)
        right = SortFunc.quick_sort(more_piv, key=key, cmp=cmp)

        left.extend(equal_piv)
        left.extend(right)
        return left

    @staticmethod
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

    @staticmethod
    def radix_sort(arr: list[int], base: int = 10) -> list[int]:

        if base < 2:
            raise ValueError("Основание base должно быть >= 2")

        n = len(arr)
        if n < 2:
            return arr

        mn = mx = arr[0]

        for x in arr[1:]:
            if x < mn:
                mn = x
            elif x > mx:
                mx = x

        offset = -mn if mn < 0 else 0
        if offset:
            for i in range(n):
                arr[i] += offset
            mx += offset

        arr = arr
        src = arr
        dst = [0] * n
        count = [0] * base

        exp = 1
        while mx // exp > 0:
            for i in range(base):
                count[i] = 0

            for v in src:
                count[(v // exp) % base] += 1

            total = 0
            for i in range(base):
                total += count[i]
                count[i] = total

            for i in range(n - 1, -1, -1):
                v = src[i]
                d = (v // exp) % base
                count[d] -= 1
                dst[count[d]] = v

            src, dst = dst, src
            exp *= base

        if src is not arr:
            arr[:] = src

        if offset:
            for i in range(n):
                arr[i] -= offset

        return arr

    @staticmethod
    def bucket_sort(arr: list[float], buckets_kol: int | None = None) -> list[float]:
        """
        Bucket sort только для float.
        возвращает новый отсортированный список.
        сложность:
        """

        if not arr:
            return []

        n = buckets_kol if buckets_kol is not None else len(arr)
        if n <= 0:
            raise ValueError("buckets_kol должно быть > 0")

        mn = min(arr)
        mx = max(arr)

        if mn == mx:
            return arr.copy()

        span = mx - mn
        buckets: list[list[float]] = [[] for _ in range(n)]

        for x in arr:
            bi = int((x - mn) / span * (n - 1))
            buckets[bi].append(x)

        out: list[float] = []
        for b in buckets:
            if b:
                out.extend(SortFunc.quick_sort(b))
        return out

    @staticmethod
    def _heapify(
            arr: list[T],
            n: int,
            i: int,
            f_comp: Callable[[T, T], int],
    ) -> None:

        while True:
            largest = i
            left = 2 * i + 1
            right = left + 1

            if left < n and f_comp(arr[left], arr[largest]) > 0:
                largest = left

            if right < n and f_comp(arr[right], arr[largest]) > 0:
                largest = right

            if largest == i:
                break

            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest

    @staticmethod
    def heap_sort(
        a: list[Any],
        key: Optional[Callable[[T], Any]] = None,
        cmp: Optional[Callable[[T, T], int]] = None,
    ) -> list[Any]:

        n = len(a)
        compare = SortFunc._compare_func(key, cmp)

        for i in range(n // 2 - 1, -1, -1):
            SortFunc._heapify(a, n, i, compare)

        for i in range(n - 1, 0, -1):
            a[i], a[0] = a[0], a[i]
            SortFunc._heapify(a, i, 0, compare)

        return a
