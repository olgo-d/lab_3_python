import pytest
from src.parse import detect_array_kind, positive_number


def test_positive_number_ok() -> None:
    positive_number(0, "fibo")
    positive_number(10, "factorial")


def test_positive_number_negative_raises() -> None:
    with pytest.raises(TypeError):
        positive_number(-1, "fibo")


def test_detect_array_kind_empty_raises() -> None:
    with pytest.raises(ValueError):
        detect_array_kind([])


@pytest.mark.parametrize(
    "arr, expected",
    [
        ([1, 2, 3], "int"),
        ([1.0, 2, 3], "float"),
        (["a", "bb"], "str"),
        ([1, "a"], "mixed"),
        ([True, False], "mixed"),
    ],
)
def test_detect_array_kind(arr, expected: str) -> None:
    assert detect_array_kind(arr) == expected
