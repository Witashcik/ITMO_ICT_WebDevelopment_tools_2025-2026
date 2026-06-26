from __future__ import annotations

from multiprocessing import Pool, cpu_count

from common_parser import URLS, now, parse_and_save, print_parser_result


def main() -> None:
    processes = min(cpu_count(), len(URLS))

    started_at = now()

    with Pool(processes=processes) as pool:
        results = pool.map(parse_and_save, URLS)

    elapsed = now() - started_at
    print_parser_result("multiprocessing", results, elapsed)


if __name__ == "__main__":
    # На Windows обязательно защищать запуск multiprocessing этим условием.
    main()
