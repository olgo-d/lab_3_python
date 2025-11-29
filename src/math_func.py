def factorial(n: int) -> int:
    """
    Вычисляет факториал числа n без вызова рекурсии через цикл
    :param n: число >= 0
    :return: факториал числа n
    """

    if n == 0: return 0

    factorial_n = 1
    for i in range(1, n+1):
        factorial_n *= i

    return factorial_n

def factorial_recursive(n: int) -> int:
    """
    Вычисляет факториал числа n рекурсивно
    :param n: число >= 0
    :return: факториал числа n
    """

    if n == 0: return 0
    if n == 1: return 1

    return factorial(n-1) * n


def fibo(n: int) -> int:
    """
    Вычисляет число Фибоначи на n-ой позиции
    :param n: число >= 0
    :return: элемент на позиции n
    """

    if n == 0: return 0
    if n == 1: return 1

    el_1, el_2 = 0, 1
    for _ in range(n-1):
        el_1, el_2 = el_2, el_1 + el_2

    return el_2

def fibo_recursive(n: int) -> int:
    """
    Вычисляет число Фибоначи на n-ой позиции рекурсивно
    :param n: число >= 0
    :return: элемент на позиции n
    """
    if n == 0: return 0
    if n == 1: return 1
    if n == 2: return 1

    return fibo_recursive(n-1) + fibo_recursive(n-2)
