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

## Подготовка на Windows / VS Code

Открой папку `lab2-concurrency-async` в VS Code.

Создай виртуальное окружение:

```powershell
py -3.12 -m venv .venv
```

Активируй его:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установи зависимости:

```powershell
pip install -r requirements.txt
```

Скопируй пример переменных окружения:

```powershell
copy .env.example .env
```

## Важно про базу данных

Для задачи 2 используется база данных из ЛР1.

Перед запуском парсинга нужно, чтобы PostgreSQL из первой лабораторной был запущен.
Если ты делал ЛР1 по нашему варианту, зайди в папку первой лабораторной:

```powershell
cd "D:\Проекты VS COD\web\Lab1\time-manager-lab\practice_1_3"
```

Запусти контейнер:

```powershell
docker compose up -d
```

Проверь, что контейнер работает на порту `5433`:

```powershell
docker ps
```

В `.env` второй лабораторной должна быть строка:

```env
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/time_manager_db
```

## Запуск задачи 1

Из папки `lab2-concurrency-async`:

```powershell
python .\task1_sum\sum_threading.py
python .\task1_sum\sum_multiprocessing.py
python .\task1_sum\sum_async.py
```

Или сразу все три варианта:

```powershell
python .\task1_sum\run_all_sum.py
```

## Запуск задачи 2

Сначала убедись, что база из ЛР1 запущена.

Потом из папки `lab2-concurrency-async`:

```powershell
python .\task2_parser\parse_threading.py
python .\task2_parser\parse_multiprocessing.py
python .\task2_parser\parse_async.py
```

Или сразу все три варианта:

```powershell
python .\task2_parser\run_all_parser.py
```

## Запуск всей лабораторной

```powershell
python .\run_all_lab2.py
```

## Что сохраняется в БД

В ЛР1 у нас тема — тайм-менеджер. Поэтому заголовки страниц сохраняются в таблицу `tag` как теги пользователя `parser_bot`.

Это позволяет использовать уже существующую структуру БД из первой лабораторной и не создавать новые таблицы.

## Почему сумма считается через формулу

По условию нужно посчитать сумму от 1 до 10 000 000 000 000. Перебирать такое количество чисел циклом практически невозможно за разумное время. Поэтому каждая подзадача считает сумму своего диапазона по формуле арифметической прогрессии:

```text
sum = (start + end) * count / 2
```

При этом задача всё равно разбивается на несколько параллельных частей, как требуется в задании.

## Краткий вывод для защиты

- `threading` удобен для I/O-задач, например загрузки страниц.
- `multiprocessing` лучше подходит для CPU-bound задач, потому что запускает отдельные процессы.
- `asyncio` хорошо подходит для большого количества сетевых запросов, потому что не блокирует выполнение во время ожидания ответа.
- Для вычисления суммы через формулу все варианты работают быстро.
- Для парсинга обычно быстрее `threading` или `asyncio`, потому что задача в основном ждёт сеть.
