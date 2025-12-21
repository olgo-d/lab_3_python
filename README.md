# Лабораторная работа №3 — алгоритмический мини‑пакет
Проект содержит набор **алгоритмов** (факториал/Фибоначчи, сортировки) и **структуру данных** (Stack) в виде модулей в папке `src/`.

## Требования

- Python **3.10+**.

Зависимости:

```bash
python -m pip install -r requirements.txt
```

## Структура

````
lab_3_python
├── src
│   ├── __init__.py
│   ├── benchmark.py
│   ├── container.py
│   ├── data_gen.py
│   ├── main.py
│   ├── math_func.py
│   ├── parse.py
│   ├── sorting.py
│   └── structures.py
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_cli.py
│   ├── test_main_helpers.py
│   ├── test_math_func.py
│   ├── test_parse.py
│   ├── test_sorting.py
│   └── test_structures.py
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
└── requirements.txt
````

- `src/math_func.py` — факториал и числа Фибоначчи.
- `src/sorting.py` — реализации сортировок.
- `src/structures.py` — структура данных `Stack`.
- `tests/` - папка с тестами
- `src/main.py` — CLI (Typer), объявления команд
- `src/parse.py` — проверки для аргументов для вычисления или сортировки
- `src/data_gen.py` — генерация данных для тестов

## Запуск

```bash
python -m src.main --help
python -m src.main sort --help
python -m src.main math --help
````

## Реализованные функции и сортировки

### `src/math_func.py`

#### Математические функции

- `factorial(n)`

  - итеративный факториал (умножение `1..n` в цикле)
  - сложность: O(n) по времени, O(1) по памяти

    ##### Запуск:
    ```bash
    python -m src.main math factorial 6
    ```

- `factorial_recursive(n)`

  - рекурсивный факториал: `factorial(n-1) * n`
  - глубина рекурсии: O(n)
  - сложность: O(n) по времени, O(n) по памяти

    ##### Запуск:
    ```bash
    python -m src.main math factorial 6 rec
    ```

- `fibo(n)`

  - итеративное n-е число Фибоначчи (две переменные, без рекурсии)
  - сложность: O(n) по времени, O(1) по памяти

    ##### Запуск:
    ```bash
    python -m src.main math fibo 10
    ```

- `fibo_recursive(n)`

  - «наивная» рекурсия: `F(n)=F(n-1)+F(n-2)`
  - глубина рекурсии: O(n)
  - сложность: O(2^n) по времени (экспоненциально), O(n) по памяти

    ##### Запуск:
    ```bash
    python -m src.main math fibo 10 rec
    ```


### `src/sorting.py`

В модуле есть поддержка сравнения через для bubble sort, quick sort, heap sort:
- `key: Callable[[T], Any] | None`
- `cmp: Callable[[T, T], int] | None` (имеет приоритет над `key`)

Вспомогательная функция:
- `_compare_func(key, cmp) -> compare(x,y)` - определяет функцию сравнения для сортировки

#### Сортировки

- `bubble_sort "[arr]" {--key} {--cmp}`

  - сортирует массивы для int, float, str и mixed(если задан key или cmp)
  - сложность: O(n^2)

    ##### Запуск:
    ```bash
    python -m src.main sort bubble "[3, 1, 2]"
    python -m src.main sort bubble "['aa', 'b', 'cccc']" --key len
    ```
- `quick_sort "[arr]" {--key} {--cmp}`

  - сортирует массивы для int, float, str и mixed (если задан key или cmp)
  - опорный элемент выбирается как median-of-three
  - сложность: в среднем O(n log n), в худшем O(n^2)

    ##### Запуск:
    ```bash
    python -m src.main sort quick "[3, 1, 2]"
    python -m src.main sort quick "['aa', 'b', 'cccc']" --key len
    python -m src.main sort quick "[3, 1, 2]" --cmp desc
    ```

- `counting_sort "[arr]"`

  - сортирует только int (включая отрицательные)
  - не поддерживает key/cmp
  - сложность: O(n + k), где k = max(a) - min(a) + 1

    ##### Запуск:
    ```bash
    python -m src.main sort counting "[3, -1, 2, 2, 0]"
    ```

- `radix_sort "[arr]" {--base}`

  - сортирует только int (включая отрицательные)
  - не поддерживает key/cmp
  - параметр `--base` задаёт основание системы счисления (>= 2)
  - сложность: O(d · (n + base)), где d — число разрядов

    ##### Запуск:
    ```bash
    python -m src.main sort radix "[170, 45, 75, 90, 802, 24, 2, 66]" --base 10
    python -m src.main sort radix "[-10, 0, 5, -3, 2]" --base 10
    ```

- `bucket_sort "[arr]" {--buckets}`

  - сортирует числа int/float (в CLI все элементы приводятся к float)
  - не поддерживает key/cmp
  - параметр `--buckets` задаёт количество корзин (> 0)
  - внутри корзины сортируются через quick_sort
  - сложность: в среднем близко к O(n), в худшем O(n^2)

    ##### Запуск:
    ```bash
    python -m src.main sort bucket "[0.2, 0.1, 0.9, 0.4]" --buckets 5
    python -m src.main sort bucket "[3, 1, 2]" --buckets 3
    ```

- `heap_sort "[arr]" {--key} {--cmp}`

  - сортирует массивы для int, float, str и mixed (если задан key или cmp)
  - использует двоичную кучу (heap), heapify реализован итеративно
  - сложность: O(n log n)

    ##### Запуск:
    ```bash
    python -m src.main sort heap "[3, 1, 2]"
    python -m src.main sort heap "['aa', 'b', 'cccc']" --key len
    python -m src.main sort heap "[3, 1, 2]" --cmp desc
    ```

#### Детали реализации алгоритмов

**Единая логика сравнения (`key`/`cmp`)**

В `sorting.py` есть вспомогательная функция `_compare_func(key, cmp)`, которая возвращает `compare(x, y) -> {-1,0,1}`:

- если передан `cmp`, он имеет приоритет (полный контроль над порядком);
- иначе, если передан `key`, сравниваются значения `key(x)` и `key(y)`;
- иначе используется обычное сравнение `x < y / x > y`.

Эта схема используется в `bubble_sort`, `quick_sort` и `heap_sort`, поэтому эти сортировки могут работать не только с `int`, но и с другими сравнимыми объектами (или через `key`/`cmp`).
`counting_sort`, `radix_sort` и `bucket_sort` — специализированные варианты и `key/cmp` не поддерживают.


### Тесты

В проекте есть набор тестов на `pytest`:

```bash
pytest -q
```
