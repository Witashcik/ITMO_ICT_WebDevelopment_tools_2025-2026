# Инструкция запуска

## Подготовка окружения для отчёта

Отчёт сделан на MkDocs. MkDocs использует Markdown-файлы из папки `docs` и конфигурационный файл `mkdocs.yml`.

## Локальный запуск отчёта

Открыть папку с отчётом в VS Code и выполнить:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

После запуска открыть:

```text
http://127.0.0.1:8000/
```

Если порт `8000` занят, можно запустить на другом порту:

```powershell
mkdocs serve -a 127.0.0.1:8080
```

## Сборка статического сайта

```powershell
mkdocs build
```

После этого появится папка `site` с HTML-версией отчёта.

## Публикация на GitHub Pages

1. Создать репозиторий на GitHub.
2. Загрузить туда папку с отчётом.
3. В `mkdocs.yml` заменить:

```yaml
repo_url: https://github.com/USERNAME/REPOSITORY
```

на ссылку своего репозитория.

4. Выполнить:

```powershell
mkdocs gh-deploy
```

MkDocs соберёт сайт и отправит его в ветку `gh-pages`.

## Запуск ЛР1

```powershell
cd "D:\Проекты VS COD\web\Lab1	ime-manager-lab\practice_1_3"
.\.venv\Scripts\Activate.ps1
docker compose up -d
alembic upgrade head
uvicorn app.main:app --reload
```

Проверка:

```text
http://127.0.0.1:8000/docs
```

## Запуск ЛР2

Перед задачей 2 должна быть запущена база из ЛР1.

```powershell
cd "D:\Проекты VS COD\web\Lab2\lab2-concurrency-async"
.\.venv\Scripts\Activate.ps1
python .un_all_lab2.py
```

Отдельно задача 1:

```powershell
python .	ask1_sumun_all_sum.py
```

Отдельно задача 2:

```powershell
python .	ask2_parserun_all_parser.py
```

## Запуск ЛР3

Перед запуском ЛР3 лучше остановить контейнер БД из ЛР1, чтобы не было конфликта порта `5433`.

```powershell
docker rm -f time_manager_postgres
```

Запуск ЛР3:

```powershell
cd "D:\Проекты VS COD\web\Lab3\lab3-docker-queue"
docker compose up --build
```

Проверка:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8001/docs
```

Остановка:

```powershell
docker compose down
```
