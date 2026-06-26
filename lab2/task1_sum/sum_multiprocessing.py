from __future__ import annotations

from multiprocessing import Pool, cpu_count

from common_sum import WORKERS, calculate_sum, now, print_result, split_ranges


def main() -> None:
    ranges = split_ranges(workers=min(WORKERS, cpu_count()))

    started_at = now()

    with Pool(processes=len(ranges)) as pool:
        results = pool.starmap(calculate_sum, ranges)

    total = sum(results)
    elapsed = now() - started_at
    print_result("multiprocessing", total, elapsed)


if __name__ == "__main__":
    # На Windows обязательно защищать запуск multiprocessing этим условием.
    main()
