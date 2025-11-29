from typing import Any


class Stack:
    def __init__(self, key=None) -> None:
        self._data: list = []
        self._mins: list = []
        self._key: Any = key

    def push(self, x: int) -> None:
        # кладет элемент в стек
        self._data.append(x)

        # если стек минимальных значений пуст или x <= последнему элементу
        if len(self._mins) == 0 or x <= self._mins[-1]:
            self._mins.append(x)

    def pop(self) -> Any:
        # удаление последнего минимума если он был последним в стеке
        if self._data[-1] == self._mins[-1]:
            self._mins.pop()

        # возвращение последний элемент и удаление его
        return self._data.pop()

    def peek(self) -> Any:
        # возвращает последний элемент не удаляя его
        return self._data[-1]

    def is_empty(self) -> bool:
        # True, если стек пуст, иначе False
        return len(self._data) == 0

    def __len__(self) -> int:
        # количество элементов в стеке
        return len(self._data)

    def min(self) -> Any:
        # возвращает минимальный элемент стека
        return self._mins[-1]
