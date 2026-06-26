from __future__ import annotations

import threading

from common_sum import calculate_sum, now, print_result, split_ranges


def worker(start: int, end: int, results: list[int], index: int) -> None:
    results[index] = calculate_sum(start, end)


def main() -> None:
    ranges = split_ranges()
    results = [0] * len(ranges)
    threads: list[threading.Thread] = []

    started_at = now()

    for index, (start, end) in enumerate(ranges):
        thread = threading.Thread(target=worker, args=(start, end, results, index))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = sum(results)
    elapsed = now() - started_at
    print_result("threading", total, elapsed)


if __name__ == "__main__":
    main()
