from __future__ import annotations

import asyncio

from common_sum import calculate_sum, now, print_result, split_ranges


async def async_calculate_sum(start: int, end: int) -> int:
    # Передаём управление циклу событий. Важно понимать: async не делает
    # CPU-вычисления реально параллельными, но демонстрирует подход async/await.
    await asyncio.sleep(0)
    return calculate_sum(start, end)


async def main_async() -> None:
    ranges = split_ranges()

    started_at = now()

    tasks = [asyncio.create_task(async_calculate_sum(start, end)) for start, end in ranges]
    results = await asyncio.gather(*tasks)

    total = sum(results)
    elapsed = now() - started_at
    print_result("asyncio", total, elapsed)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
