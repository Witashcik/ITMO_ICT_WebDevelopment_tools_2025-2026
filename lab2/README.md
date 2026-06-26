# Лабораторная работа 2. Потоки. Процессы. Асинхронность

Тема: сравнение `threading`, `multiprocessing` и `asyncio` в Python.

В проекте две части:

1. `task1_sum` — вычисление суммы чисел от 1 до 10 000 000 000 000.
2. `task2_parser` — параллельный парсинг страниц и сохранение заголовков в БД из ЛР1.

## Структура проекта

```text
lab2-concurrency-async/
├── task1_sum/
│   ├── common_sum.py
│   ├── sum_threading.py
│   ├── sum_multiprocessing.py
│   ├── sum_async.py
│   └── run_all_sum.py
│
├── task2_parser/
│   ├── common_parser.py
│   ├── parse_threading.py
│   ├── parse_multiprocessing.py
│   ├── parse_async.py
│   └── run_all_parser.py
│
├── report/
│   └── report.md
│
├── .env.example
├── requirements.txt
└── run_all_lab2.py
```


