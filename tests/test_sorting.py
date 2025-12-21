import pytest

from src.data_gen import (
    rand_int_array,
    nearly_sorted,
    many_duplicates,
    reverse_sorted,
    rand_float_array,
)
from src.sorting import SortFunc


def _datasets_int() -> list[list[int]]:
    return [
        rand_int_array(200, -50, 50, seed=1),
        rand_int_array(100, -50, 50, distinct=True, seed=2),
        nearly_sorted(200, swaps=10, seed=3),
        many_duplicates(200, k_unique=5, seed=4),
        reverse_sorted(200),
        [],
        [1],
        [2, 1],
    ]


def _datasets_float() -> list[list[float]]:
    return [
        rand_float_array(200, 0.0, 1.0, seed=10),
        rand_float_array(50, 0.0, 1.0, seed=11),
        [],
        [0.5],
        [0.2, 0.1],
    ]


@pytest.mark.parametrize("arr", _datasets_int())
def test_bubble_sort_correct(arr: list[int]) -> None:
    out = SortFunc.bubble_sort(arr)
    assert out == sorted(arr)


@pytest.mark.parametrize("arr", _datasets_int())
def test_heap_sort_correct(arr: list[int]) -> None:
    a = arr.copy()
    out = SortFunc.heap_sort(a)
    assert out == sorted(arr)


@pytest.mark.parametrize("arr", _datasets_int())
def test_quick_sort_correct(arr: list[int]) -> None:
    out = SortFunc.quick_sort(arr)
    assert out == sorted(arr)


def test_quick_sort_with_cmp_desc() -> None:
    def cmp_desc(x: int, y: int) -> int:
        return (y > x) - (y < x)

    arr = rand_int_array(50, -100, 100, seed=20)
    out = SortFunc.quick_sort(arr, cmp=cmp_desc)
    assert out == sorted(arr, reverse=True)


@pytest.mark.parametrize("arr", _datasets_int())
def test_counting_sort_correct(arr: list[int]) -> None:
    out = SortFunc.counting_sort(arr)
    assert out == sorted(arr)


@pytest.mark.parametrize("arr", _datasets_int())
def test_radix_sort_correct(arr: list[int]) -> None:
    a = arr.copy()
    out = SortFunc.radix_sort(a, base=10)
    assert out == sorted(arr)


def test_radix_sort_base_validation() -> None:
    with pytest.raises(ValueError):
        SortFunc.radix_sort([1, 2, 3], base=1)


@pytest.mark.parametrize("arr", _datasets_float())
def test_bucket_sort_correct(arr: list[float]) -> None:
    out = SortFunc.bucket_sort(arr, buckets_kol=10)
    assert out == sorted(arr)


def test_compare_func_priority_cmp_over_key() -> None:
    def cmp_always_equal(x, y) -> int:
        return 0
    comp = SortFunc._compare_func(key=len, cmp=cmp_always_equal)
    assert comp("aaa", "b") == 0
