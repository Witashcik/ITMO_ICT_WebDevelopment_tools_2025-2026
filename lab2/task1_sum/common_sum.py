from __future__ import annotations

import os
from time import perf_counter

# По условию нужно посчитать сумму от 1 до 10_000_000_000_000.
# Перебирать эти числа циклом практически нереально, поэтому для каждой части
# используется формула суммы арифметической прогрессии.
LIMIT = int(os.getenv("SUM_LIMIT", "10000000000000"))
WORKERS = int(os.getenv("WORKERS", "8"))


def split_ranges(limit: int = LIMIT, workers: int = WORKERS) -> list[tuple[int, int]]:
    """Разбивает диапазон 1..limit на workers примерно равных отрезков."""
    chunk_size = limit // workers
    ranges: list[tuple[int, int]] = []

    start = 1
    for i in range(workers):
        end = start + chunk_size - 1
        if i == workers - 1:
            end = limit
        ranges.append((start, end))
        start = end + 1

    return ranges


def calculate_sum(start: int, end: int) -> int:
    """Считает сумму чисел от start до end включительно."""
    count = end - start + 1
    return (start + end) * count // 2


def expected_sum(limit: int = LIMIT) -> int:
    """Контрольная сумма от 1 до limit."""
    return limit * (limit + 1) // 2


def print_result(approach: str, result: int, elapsed: float) -> None:
    print(f"Подход: {approach}")
    print(f"Диапазон: 1..{LIMIT}")
    print(f"Количество задач: {WORKERS}")
    print(f"Результат: {result}")
    print(f"Результат корректный: {result == expected_sum()}")
    print(f"Время выполнения: {elapsed:.6f} сек.")


def now() -> float:
    return perf_counter()
