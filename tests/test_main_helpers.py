import builtins
import pytest
import typer

from src.main import build_cmp, build_key, parse_py_list


def test_parse_py_list_ok() -> None:
    assert parse_py_list(["[1, 2, 3]"]) == [1, 2, 3]
    assert parse_py_list(["['a', 'bb']"]) == ["a", "bb"]


def test_parse_py_list_invalid_format_raises() -> None:
    with pytest.raises(typer.BadParameter):
        parse_py_list(["1, 2, 3"])


def test_parse_py_list_syntax_error_raises() -> None:
    with pytest.raises(typer.BadParameter):
        parse_py_list(["[1, 2,, 3]"])


def test_build_key_none() -> None:
    assert build_key(None, [1, 2, 3]) is None
    assert build_key("none", [1, 2, 3]) is None


def test_build_key_valid() -> None:
    k = build_key("len", ["a", "bb"])
    assert k is builtins.len


def test_build_key_invalid_name_raises() -> None:
    with pytest.raises(typer.BadParameter):
        build_key("notakey", [1, 2, 3])


def test_build_key_not_applicable_raises() -> None:
    with pytest.raises(typer.BadParameter):
        build_key("len", [1, 2, 3])


def test_build_cmp_desc() -> None:
    cmp_func = build_cmp("desc", key=None)
    assert cmp_func(5, 1) == -1
    assert cmp_func(1, 5) == 1
    assert cmp_func(2, 2) == 0


def test_build_cmp_invalid_raises() -> None:
    with pytest.raises(typer.BadParameter):
        build_cmp("unknown", key=None)
