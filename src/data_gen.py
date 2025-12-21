from __future__ import annotations

import random
from typing import Optional


def rand_int_array(n: int, lo: int, hi: int, *, distinct: bool = False, seed: Optional[int] = None) -> list[int]:
    rng = random.Random(seed)

    if n <= 0:
        return []

    if lo > hi:
        lo, hi = hi, lo

    if distinct:
        size = hi - lo + 1
        if n > size:
            raise ValueError(f"distinct=True требует n <= (hi-lo+1). Сейчас n={n}, range={size}")
        return rng.sample(range(lo, hi + 1), k=n)

    return [rng.randint(lo, hi) for _ in range(n)]


def nearly_sorted(n: int, swaps: int, *, seed: Optional[int] = None) -> list[int]:
    rng = random.Random(seed)
    a = list(range(n))
    if n <= 1 or swaps <= 0:
        return a

    for _ in range(swaps):
        i = rng.randrange(n)
        j = rng.randrange(n)
        a[i], a[j] = a[j], a[i]
    return a


def many_duplicates(n: int, k_unique: int = 5, *, seed: Optional[int] = None) -> list[int]:
    rng = random.Random(seed)

    if n <= 0:
        return []
    if k_unique <= 0:
        raise ValueError("k_unique должен быть > 0")

    unique_vals = rng.sample(range(-10_000, 10_001), k=min(k_unique, 20_001))
    return [rng.choice(unique_vals) for _ in range(n)]


def reverse_sorted(n: int) -> list[int]:
    if n <= 0:
        return []
    return list(range(n - 1, -1, -1))


def rand_float_array(n: int, lo: float = 0.0, hi: float = 1.0, *, seed: Optional[int] = None) -> list[float]:
    rng = random.Random(seed)
    if n <= 0:
        return []

    if lo > hi:
        lo, hi = hi, lo

    return [rng.uniform(lo, hi) for _ in range(n)]
