from __future__ import annotations

import threading

from common_parser import URLS, now, parse_and_save, print_parser_result


def worker(url: str, results: list, index: int) -> None:
    results[index] = parse_and_save(url)


def main() -> None:
    results = [None] * len(URLS)
    threads: list[threading.Thread] = []

    started_at = now()

    for index, url in enumerate(URLS):
        thread = threading.Thread(target=worker, args=(url, results, index))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    elapsed = now() - started_at
    print_parser_result("threading", results, elapsed)


if __name__ == "__main__":
    main()
