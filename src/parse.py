from typing import Any


def positive_number(n: int, func: str):
    if n < 0:
        raise TypeError(f'аргумент {n} для функции {func} должен быть >= 0')

def detect_array_kind(arr: list[Any]) -> str:

    if not arr:
        raise ValueError("Список пустой")

    all_int = True
    all_num = True
    any_float = False
    all_str = True

    for x in arr:
        is_int = isinstance(x, int) and not isinstance(x, bool)
        is_float = isinstance(x, float)
        is_num = is_int or is_float
        is_str = isinstance(x, str)

        all_int = all_int and is_int
        all_num = all_num and is_num
        all_str = all_str and is_str
        any_float = any_float or is_float

    if all_int:
        return "int"
    if all_str:
        return "str"
    if all_num:
        return "float" if any_float else "int"
    return "mixed"
