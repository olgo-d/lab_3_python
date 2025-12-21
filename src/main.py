from typing import Any, Callable, Optional
import builtins
import ast

import typer
from typer import Typer, Context

from src.container import Container, build_container
from src.parse import positive_number, detect_array_kind

app = Typer(help="Сортировка массивов и функции Фибоначчи и факториала")


def get_container(ctx: Context) -> Container:
    container = ctx.obj
    if not isinstance(container, Container):
        raise RuntimeError("Контейнер DI не инициализирован")
    return container


@app.callback()
def main(ctx: Context):
    ctx.obj = build_container()


def parse_py_list(tokens: list[str]) -> list[Any]:
    s = " ".join(tokens).strip()

    if not (s.startswith("[") and s.endswith("]")):
        raise typer.BadParameter(
            'Список должен быть в квадратных скобках, например: [] или [1, 2, 3] или [1, 2, "pop"]'
        )

    try:
        value = ast.literal_eval(s)
    except (SyntaxError, ValueError) as e:
        raise typer.BadParameter(f"Некорректный список: {s}. Ошибка: {e}")

    if not isinstance(value, list):
        raise typer.BadParameter(
            "Список должен быть в квадратных скобках, например: [] или [1, 2, 3] или [1, 2, 'pop']"
        )

    return value



def build_key(
    key_name: Optional[str],
    arr: list[Any],
) -> Optional[Callable[[Any], Any]]:
    """
    определяет ключ для сортировки
    :param key_name: ключ заданный пользователем
    :param arr: сортируемый массив
    :return: ключ
    """
    if key_name is None:
        return None

    name = key_name.lower()
    if name in ("none", ""):
        return None

    correct_key = getattr(builtins, name, None)
    if correct_key is None or not callable(correct_key):
        raise typer.BadParameter(f"Некорректный key: {key_name}")

    for x in arr:
        try:
            _ = correct_key(x)
        except Exception as e:
            raise typer.BadParameter(f'Нельзя применить key={key_name} к элементу {x}: {e}')

    return correct_key


def build_cmp(
    cmp_name: Optional[str],
    key: Optional[Callable[[Any], Any]],
) -> Optional[Callable[[Any, Any], int]]:
    """
    определяет cmp для сортировки
    :param cmp_name: cmp заданный пользователем
    :param key: ключ заданный пользователем
    :return: cmp
    """
    if cmp_name is None:
        return None

    name = cmp_name.lower()
    if name in ("none", ""):
        return None

    if name == "desc":
        def cmp_desc(x: Any, y: Any) -> int:
            v1 = key(x) if key is not None else x
            v2 = key(y) if key is not None else y
            if v1 > v2:
                return -1
            if v1 < v2:
                return 1
            return 0

        return cmp_desc

    raise typer.BadParameter(
        f"Неизвестный cmp: {cmp_name}. Разрешены: none, desc."
    )


@app.command()
def sort(
    ctx: Context,
    name_sort: str = typer.Argument(
        "",
        help="Название сортировки: bubble, quick, counting, radix, bucket, heap",
    ),
    iter: list[str] = typer.Argument(
        ...,
        help="Список в квадратных скобках, например: [] или [1, 2, 3,] или [1, 2, 'pop']",
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key", "-K",
        help="Опциональный key (например len, abs, str, int...)",
    ),
    cmp_name: Optional[str] = typer.Option(
        None, "--cmp", "-C",
        help="Опциональный cmp: none, desc (descending)",
    ),
    base: int = typer.Option(
        10, "--base", "-b",
        help="Основание для radix_sort (>= 2)",
    ),
    buckets: Optional[int] = typer.Option(
        None, "--buckets", "-k",
        help="Количество корзин для bucket_sort (> 0)",
    ),
) -> None:

    """
    сортировка массива выбранным методом
    :param ctx: объект контекста typer для имитации контейнера di
    :param name_sort: Название сортировки: bubble, quick, counting, radix, bucket, heap
    :param iter: Список элементов массива, например: [1, 2, 3]
    :param key_name: Опциональный key
    :param cmp_name: Опциональный cmp: none, desc
    :param base: основание для сортировки
    :param buckets: количество корзин для сортировки
    :return: отсортированный массив
    """
    container = get_container(ctx)
    sorter = container.sort_function

    algo = name_sort.lower()
    arr = parse_py_list(iter)

    original_arr = arr.copy()

    if not arr:
        typer.echo("Исходный список: []")
        typer.echo("Отсортированный: []")
        return

    type_of_el = detect_array_kind(arr)

    key_provided = key_name is not None and key_name.lower() not in ("none", "")
    cmp_provided = cmp_name is not None and cmp_name.lower() not in ("none", "")

    if algo in ("counting", "radix", "bucket") and (key_provided or cmp_provided):
        raise typer.BadParameter(f"{algo}_sort не поддерживает key/cmp")

    key = build_key(key_name, arr)
    cmp = build_cmp(cmp_name, key)

    # если типы смешаны и нет key/cmp — сортировки сравнением могут упасть
    if type_of_el == "mixed" and key is None and cmp is None:
        raise typer.BadParameter(
            "Список содержит смешанные типы. Укажи key (например len для строк) "
        )

    if algo == "bubble":
        result = sorter.bubble_sort(arr, key=key, cmp=cmp)

    elif algo == "quick":
        result = sorter.quick_sort(arr, key=key, cmp=cmp)

    elif algo == "counting":
        if not arr:
            result = []
        elif type_of_el == "int":
            result = sorter.counting_sort(arr)
        else:
            raise typer.BadParameter("counting_sort работает только с целыми числами")

    elif algo == "radix":
        if not arr:
            result = []
        elif type_of_el == "int":
            result = sorter.radix_sort(arr.copy(), base=base)
        else:
            raise typer.BadParameter("radix_sort работает только с целыми числами")

    elif algo == "bucket":
        if type_of_el in ("int", "float"):
            num_list = [float(x) for x in arr]
            result = sorter.bucket_sort(num_list, buckets_kol=buckets)
        else:
            raise typer.BadParameter("bucket_sort работает только с числами")

    elif algo == "heap":
        result = sorter.heap_sort(arr.copy(), key=key, cmp=cmp)

    else:
        raise typer.BadParameter(
            f"Неизвестный алгоритм сортировки: {name_sort}. "
            f"Разрешены: bubble, quick, counting, radix, bucket, heap"
        )

    typer.echo(f"Исходный список: {original_arr}")
    typer.echo(f"Отсортированный: {result}")


@app.command()
def math(
    ctx: Context,
    func_name: str = typer.Argument(..., help="Тип функции: fibo или factorial"),
    n: int = typer.Argument(..., help="Аргумент n >= 0"),
    mode: str = typer.Argument(None, help="Режим: rec или iter"),
) -> None:
    """
    Вычисляет значение (result) от функций fibo или factorial для n
    :param ctx: объект контекста typer для имитации контейнера di
    :param func_name: Тип функции: fibo или factorial
    :param n: Аргумент n >= 0
    :param mode: Режим: rec или iter
    :return: result
    """
    container = get_container(ctx)
    m = container.math_function

    func_name = func_name.lower()
    if mode is not None:
        mode = mode.lower()

    try:
        # проверка, что аргумент >= 0
        positive_number(n, func_name)

        if func_name == 'fibo':

            if mode == 'iter' or mode is None:
                result = m.fibo(n)
            elif mode == 'rec':
                result = m.fibo_recursive(n)
            else:
                raise typer.BadParameter("mode должен быть 'rec' или 'iter'")
        elif func_name == 'factorial':
            if mode == 'iter' or mode is None:
                result = m.factorial(n)
            elif mode == 'rec':
                result = m.factorial_recursive(n)
            else:
                raise typer.BadParameter("mode должен быть 'rec' или 'iter'")
        else:
            raise typer.BadParameter("func_name должен быть 'fibo' или 'factorial'")

        typer.echo(f"Результат: {result}")

    except ValueError as e:
        raise typer.BadParameter(str(e))


if __name__ == "__main__":
    app()
