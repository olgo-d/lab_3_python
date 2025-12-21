import pytest
from src.math_func import MathFunc


@pytest.mark.parametrize("n, expected", [(0, 1), (1, 1), (5, 120), (8, 40320)])
def test_factorial_iter(n: int, expected: int) -> None:
    assert MathFunc.factorial(n) == expected


@pytest.mark.parametrize("n, expected", [(0, 1), (1, 1), (6, 720)])
def test_factorial_recursive(n: int, expected: int) -> None:
    assert MathFunc.factorial_recursive(n) == expected


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (3, 2), (10, 55)])
def test_fibo_iter(n: int, expected: int) -> None:
    assert MathFunc.fibo(n) == expected


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (6, 8)])
def test_fibo_recursive(n: int, expected: int) -> None:
    assert MathFunc.fibo_recursive(n) == expected
