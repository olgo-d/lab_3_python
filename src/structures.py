from typing import Any


class Stack:
    def __init__(self, key=None) -> None:
        self._data: list = []
        self._mins: list = []
        self._key: Any = key

    # кладет элемент в стек
    def push(self, x: int) -> None:

        self._data.append(x)

        # если стек минимальных значений пуст или x <= последнему элементу
        if len(self._mins) == 0 or x <= self._mins[-1]:
            self._mins.append(x)

    # возвращение последний элемент и удаление его
    def pop(self) -> Any:

        # удаление последнего минимума если он был последним в стеке
        if self._data[-1] == self._mins[-1]:
            self._mins.pop()

        return self._data.pop()

    # возвращает последний элемент не удаляя его
    def peek(self) -> Any:
        return self._data[-1]

    # True, если стек пуст, иначе False
    def is_empty(self) -> bool:
        return len(self._data) == 0

    # количество элементов в стеке
    def __len__(self) -> int:
        return len(self._data)

    # возвращает минимальный элемент стека
    def min(self) -> Any:
        return self._mins[-1]
